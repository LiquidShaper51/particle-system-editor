"""Job runner: wires handlers -> processors -> drivers for a file.

This is the pipeline/worker core. ``run_file`` is synchronous and safe to
call from a worker thread; the GUI wraps it in a QThreadPool task.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from particle_system_editor.drivers.base_driver import BaseDriver
from particle_system_editor.drivers.psys_driver import PsysDriver
from particle_system_editor.handlers.base_handler import IngestError
from particle_system_editor.handlers.registry import HandlerRegistry
from particle_system_editor.models.particle_graph import ParticleGraph
from particle_system_editor.processors.base_processor import BaseProcessor
from particle_system_editor.processors.budget_processor import BudgetProcessor
from particle_system_editor.processors.normalize_processor import NormalizeProcessor

log = logging.getLogger(__name__)


@dataclass(slots=True)
class JobResult:
    ok: bool
    graph: ParticleGraph | None = None
    error: str | None = None
    duration_ms: float = 0.0

    def summary(self) -> str:
        if not self.ok:
            return f"FAILED: {self.error}"
        assert self.graph is not None
        return (
            f"{self.graph.name}: {self.graph.emitter_count} emitters, "
            f"peak~{self.graph.estimated_peak()} particles, "
            f"{self.duration_ms:.1f}ms"
        )


class JobRunner:
    def __init__(
        self,
        max_workers: int = 4,
        registry: HandlerRegistry | None = None,
        processors: list[BaseProcessor] | None = None,
    ) -> None:
        self.max_workers = max_workers
        self.registry = registry or HandlerRegistry()
        self.processors = sorted(
            processors or [NormalizeProcessor(), BudgetProcessor()],
            key=lambda p: p.order,
        )

    def run_file(self, path: Path, driver: BaseDriver | None = None) -> JobResult:
        import time

        t0 = time.perf_counter()
        try:
            handler = self.registry.for_path(path)
            graph = handler.ingest(path)
            for processor in self.processors:
                graph = processor.process(graph)
            if driver is not None:
                driver.write(graph, path.with_suffix(driver.extensions[0]))
            return JobResult(
                ok=True,
                graph=graph,
                duration_ms=(time.perf_counter() - t0) * 1000.0,
            )
        except (IngestError, Exception) as exc:  # noqa: BLE001 — surface all to UI
            log.exception("pipeline failed for %s", path)
            return JobResult(
                ok=False,
                error=str(exc),
                duration_ms=(time.perf_counter() - t0) * 1000.0,
            )

    def export(self, graph: ParticleGraph, out: Path) -> None:
        driver = PsysDriver()
        driver.write(graph, out)