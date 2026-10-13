"""Path helpers for the particle system editor."""
from __future__ import annotations

import os
from pathlib import Path


def user_projects_dir() -> Path:
    """Return the per-user projects directory, creating it if needed."""
    base = os.environ.get("APPDATA")
    root = Path(base) / "particle-system-editor" / "projects" if base else Path.cwd() / "projects"
    root.mkdir(parents=True, exist_ok=True)
    return root


def is_particle_source(path: Path) -> bool:
    return path.suffix.lower() in {".psys", ".emitter"}