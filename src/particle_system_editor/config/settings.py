"""User settings for the particle system editor.

Reads ``%APPDATA%/particle-system-editor/settings.toml`` on Windows, falling
back to ``particle_editor.toml`` in the working directory, then to defaults.
"""
from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, replace
from pathlib import Path

_DEFAULTS = {
    "max_workers": 4,
    "preview_fps": 60,
    "max_particles_preview": 250_000,
    "native_emitter": True,
}


@dataclass(frozen=True, slots=True)
class Settings:
    max_workers: int = 4
    preview_fps: int = 60
    max_particles_preview: int = 250_000
    native_emitter: bool = True

    def with_overrides(self, **kw: object) -> "Settings":
        return replace(self, **{k: v for k, v in kw.items() if v is not None})


def _config_path() -> Path:
    appdata = os.environ.get("APPDATA")
    if appdata:
        return Path(appdata) / "particle-system-editor" / "settings.toml"
    return Path.cwd() / "particle_editor.toml"


def load_settings() -> Settings:
    path = _config_path()
    if not path.is_file():
        return Settings()
    with path.open("rb") as fh:
        raw = tomllib.load(fh)
    merged = {**_DEFAULTS, **raw.get("editor", {})}
    return Settings(**merged)