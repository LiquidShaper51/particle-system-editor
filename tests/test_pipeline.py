"""End-to-end pipeline tests: ingest -> process -> export."""
from __future__ import annotations

from pathlib import Path

from particle_system_editor.drivers.psys_driver import PsysDriver
from particle_system_editor.handlers.psys_handler import PsysHandler
from particle_system_editor.processors.budget_processor import BudgetProcessor
from particle_system_editor.processors.normalize_processor import NormalizeProcessor

SAMPLE = """\
schema: 2
name: smoke_test
gravity: [0.0, -9.81, 0.0]
max_particles: 5000
emitters:
  - name: spark
    shape: cone
    rate: 2000
    lifetime: 2.0
    blend: additive
"""


def test_psys_roundtrip(tmp_path: Path) -> None:
    src = tmp_path / "smoke.psys"
    src.write_text(SAMPLE, encoding="utf-8")

    graph = PsysHandler().ingest(src)
    assert graph.name == "smoke_test"
    assert graph.emitter_count == 1
    assert graph.estimated_peak() == 4000

    NormalizeProcessor().process(graph)
    BudgetProcessor(max_particles=1000).process(graph)
    assert graph.estimated_peak() <= 1000

    out = tmp_path / "out.psys"
    PsysDriver().write(graph, out)
    reread = PsysHandler().ingest(out)
    assert reread.emitter_count == 1
    assert reread.emitters[0].name == "spark"


def test_budget_noop_when_under(tmp_path: Path) -> None:
    src = tmp_path / "small.psys"
    src.write_text(SAMPLE, encoding="utf-8")
    graph = PsysHandler().ingest(src)
    before = graph.estimated_peak()
    BudgetProcessor(max_particles=1_000_000).process(graph)
    assert graph.estimated_peak() == before