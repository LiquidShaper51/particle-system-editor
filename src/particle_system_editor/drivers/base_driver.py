"""Abstract output driver contract."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from particle_system_editor.models.particle_graph import ParticleGraph


class ExportError(Exception):
    """Raised when a graph cannot be serialized to a target format."""


class BaseDriver(ABC):
    extensions: tuple[str, ...] = ()
    format_name: str = "unknown"

    @abstractmethod
    def write(self, graph: ParticleGraph, path: Path) -> None:
        """Serialize ``graph`` to ``path`` or raise ExportError."""