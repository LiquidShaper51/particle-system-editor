"""JSON output driver for tooling interop and diff-friendly exports."""
from __future__ import annotations

import json
from pathlib import Path

from particle_system_editor.drivers.base_driver import BaseDriver, ExportError
from particle_system_editor.models.particle_graph import ParticleGraph


class JsonDriver(BaseDriver):
    extensions = (".json",)
    format_name = "json"

    def write(self, graph: ParticleGraph, path: Path) -> None:
        payload = {
            "name": graph.name,
            "gravity": list(graph.gravity),
            "max_particles": graph.max_particles,
            "emitters": [
                {
                    "name": e.name,
                    "shape": e.shape.value,
                    "rate": e.rate,
                    "lifetime": e.lifetime,
                    "blend": e.blend.value,
                }
                for e in graph.emitters
            ],
        }
        try:
            path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except OSError as exc:
            raise ExportError(f"cannot write {path}: {exc}") from exc