"""Native .psys output driver — round-trips with PsysHandler."""
from __future__ import annotations

from pathlib import Path

import yaml

from particle_system_editor.drivers.base_driver import BaseDriver, ExportError
from particle_system_editor.models.particle_graph import ParticleGraph

_SCHEMA_VERSION = 2


class PsysDriver(BaseDriver):
    extensions = (".psys",)
    format_name = "psys"

    def write(self, graph: ParticleGraph, path: Path) -> None:
        payload = {
            "schema": _SCHEMA_VERSION,
            "name": graph.name,
            "gravity": list(graph.gravity),
            "max_particles": graph.max_particles,
            "emitters": [
                {
                    "name": e.name,
                    "shape": e.shape.value,
                    "rate": e.rate,
                    "lifetime": e.lifetime,
                    "velocity": list(e.initial_velocity),
                    "size_start": e.size_start,
                    "size_end": e.size_end,
                    "blend": e.blend.value,
                }
                for e in graph.emitters
            ],
        }
        try:
            path.write_text(
                yaml.safe_dump(payload, sort_keys=False),
                encoding="utf-8",
            )
        except OSError as exc:
            raise ExportError(f"cannot write {path}: {exc}") from exc