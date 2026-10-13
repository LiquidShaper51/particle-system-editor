"""Shared application context passed to UI, services, and workers.

Holds the loaded settings, the job runner, and the active project so that
handlers/processors/drivers never reach for globals.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from particle_system_editor.config.settings import Settings
from particle_system_editor.models.particle_graph import ParticleGraph
from particle_system_editor.services.job_runner import JobRunner


@dataclass(slots=True)
class AppContext:
    settings: Settings
    runner: JobRunner
    project_path: Path | None = None
    graph: ParticleGraph | None = None
    _dirty: bool = field(default=False, repr=False)

    def mark_dirty(self) -> None:
        self._dirty = True

    def mark_saved(self) -> None:
        self._dirty = False

    @property
    def is_dirty(self) -> bool:
        return self._dirty