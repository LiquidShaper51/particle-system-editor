"""Handler registry and legacy emitter ingest tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from particle_system_editor.handlers.base_handler import IngestError
from particle_system_editor.handlers.emitter_handler import EmitterHandler
from particle_system_editor.handlers.registry import HandlerRegistry


def test_registry_picks_psys(tmp_path: Path) -> None:
    p = tmp_path / "a.psys"
    p.write_text("schema: 1\nname: x\n", encoding="utf-8")
    handler = HandlerRegistry().for_path(p)
    assert handler.format_name == "psys"


def test_registry_unknown_ext(tmp_path: Path) -> None:
    p = tmp_path / "a.fbx"
    with pytest.raises(IngestError):
        HandlerRegistry().for_path(p)


def test_legacy_emitter_defaults(tmp_path: Path) -> None:
    p = tmp_path / "legacy.emitter"
    p.write_text("name: old\nrate: 10\n", encoding="utf-8")
    graph = EmitterHandler().ingest(p)
    assert graph.emitter_count == 1
    assert graph.emitters[0].rate == 10.0
</final>