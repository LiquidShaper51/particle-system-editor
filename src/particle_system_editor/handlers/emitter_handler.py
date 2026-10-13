"""Legacy .emitter ingest handler.

Handles the pre-0.4 flat-key emitter format still found in old mod
archives. Deliberately permissive: missing keys fall back to defaults.
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


class EmitterHandler(BaseHandler):
    extensions = (".emitter",)
    format_name = "emitter-legacy"

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions

    def ingest(self, path: Path) -> ParticleGraph:
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError) as exc:
            raise IngestError(f"cannot read {path}: {exc}") from exc

        if not isinstance(raw, dict):
            raise IngestError("emitter root must be a mapping")

        try:
            shape = EmitterShape(raw.get("shape", "point"))
            blend = BlendMode(raw.get("blend", "additive"))
        except ValueError as exc:
            raise IngestError(f"bad enum in {path.name}: {exc}") from exc

        emitter = Emitter(
            name=raw.get("name", path.stem),
            shape=shape,
            rate=float(raw.get("rate", 50.0)),
            lifetime=float(raw.get("life", raw.get("lifetime", 1.0))),
            blend=blend,
        )
        return ParticleGraph(name=path.stem, emitters=[emitter])