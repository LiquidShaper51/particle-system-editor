"""Handler registry: picks the right ingest handler for a path."""
from __future__ import annotations

from pathlib import Path

from particle_system_editor.handlers.base_handler import BaseHandler, IngestError
from particle_system_editor.handlers.emitter_handler import EmitterHandler
from particle_system_editor.handlers.psys_handler import PsysHandler


class HandlerRegistry:
    def __init__(self, handlers: list[BaseHandler] | None = None) -> None:
        self._handlers: list[BaseHandler] = handlers or [
            PsysHandler(),
            EmitterHandler(),
        ]

    def register(self, handler: BaseHandler) -> None:
        self._handlers.append(handler)

    def for_path(self, path: Path) -> BaseHandler:
        for handler in self._handlers:
            if handler.can_handle(path):
                return handler
        raise IngestError(f"no handler for {path.suffix or path.name}")

    @property
    def known_extensions(self) -> tuple[str, ...]:
        return tuple(ext for h in self._handlers for ext in h.extensions)