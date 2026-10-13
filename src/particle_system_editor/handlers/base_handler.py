"""Abstract ingest handler contract.

A handler reads a source file (or bytes) and returns a normalized
ParticleGraph. Handlers must not mutate global state and must raise
IngestError on malformed input rather than returning partial graphs.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from particle_system_editor.models.particle_graph import ParticleGraph


class IngestError(Exception):
    """Raised when a source file cannot be parsed into a ParticleGraph."""


class BaseHandler(ABC):
    #: File extensions this handler claims, lowercase, with leading dot.
    extensions: tuple[str, ...] = ()
    #: Short identifier used in logs and the format picker.
    format_name: str = "unknown"

    @abstractmethod
    def can_handle(self, path: Path) -> bool:
        """Return True if this handler should ingest ``path``."""

    @abstractmethod
    def ingest(self, path: Path) -> ParticleGraph:
        """Parse ``path`` into a ParticleGraph or raise IngestError."""