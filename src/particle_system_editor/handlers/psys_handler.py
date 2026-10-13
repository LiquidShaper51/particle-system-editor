"""Native .psys ingest handler.

The .psys format is this editor's own YAML-based particle description.
Schema is versioned via a top-level ``schema`` key.
"""
from __future__ import annotations

from pathlib import Path

import yaml

from particle_system_editor.handlers.base_handler import BaseHandler, IngestError
from particle_system_editor.models.particle_graph import (
    BlendMode,
    Emitter,
    EmitterShape,
    ParticleGraph,
)

_SUPPORTED_SCHEMA = {1, 2}


class PsysHandler(BaseHandler):
    extensions = (".psys",)
    format_name = "psys"

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions

    def ingest(self, path: Path) -> ParticleGraph:
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise IngestError(f"cannot read {path}: {exc}") from exc

        if not isinstance(raw, dict):
            raise IngestError("psys root must be a mapping")
        schema = raw.get("schema", 1)
        if schema not in _SUPPORTED_SCHEMA:
            raise IngestError(f"unsupported psys schema {schema!r}")

        graph = ParticleGraph(
            name=raw.get("name", path.stem),
            gravity=tuple(raw.get("gravity", (0.0, -9.81, 0.0))),
            max_particles=int(raw.get("max_particles", 1_000_000)),
        )
        for i, e in enumerate(raw.get("emitters", [])):
            try:
                graph.emitters.append(
                    Emitter(
                        name=e.get("name", f"emitter_{i}"),
                        shape=EmitterShape(e.get("shape", "point")),
                        rate=float(e.get("rate", 100.0)),
                        lifetime=float(e.get("lifetime", 1.0)),
                        initial_velocity=tuple(e.get("velocity", (0.0, 0.0, 0.0))),
                        size_start=float(e.get("size_start", 1.0)),
                        size_end=float(e.get("size_end", 0.0)),
                        blend=BlendMode(e.get("blend", "additive")),
                    )
                )
            except (ValueError, TypeError) as exc:
                raise IngestError(f"emitter {i} invalid: {exc}") from exc
        return graph