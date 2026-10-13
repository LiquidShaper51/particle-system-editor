"""Normalized in-memory representation of a particle system.

Every ingest handler produces one of these; every processor mutates it;
every output driver consumes it. This is the single schema the whole
pipeline agrees on.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EmitterShape(str, Enum):
    POINT = "point"
    SPHERE = "sphere"
    CONE = "cone"
    BOX = "box"
    MESH = "mesh"


class BlendMode(str, Enum):
    ADDITIVE = "additive"
    ALPHA = "alpha"
    MULTIPLY = "multiply"


@dataclass(slots=True)
class Emitter:
    name: str
    shape: EmitterShape = EmitterShape.POINT
    rate: float = 100.0          # particles/sec
    lifetime: float = 1.0        # seconds
    initial_velocity: tuple[float, float, float] = (0.0, 0.0, 0.0)
    size_start: float = 1.0
    size_end: float = 0.0
    color_start: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    color_end: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 0.0)
    blend: BlendMode = BlendMode.ADDITIVE


@dataclass(slots=True)
class ParticleGraph:
    """A full particle system: named emitters plus global sim params."""
    name: str = "untitled"
    gravity: tuple[float, float, float] = (0.0, -9.81, 0.0)
    max_particles: int = 1_000_000
    emitters: list[Emitter] = field(default_factory=list)

    @property
    def emitter_count(self) -> int:
        return len(self.emitters)

    def estimated_peak(self) -> int:
        """Rough upper bound on live particles for the current config."""
        return int(sum(e.rate * e.lifetime for e in self.emitters))