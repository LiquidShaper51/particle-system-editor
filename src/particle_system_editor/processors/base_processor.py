"""Abstract processor contract.

Processors run in a fixed order after ingest and before export. They may
mutate the graph but must leave it valid (see ParticleGraph invariants).
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from particle_system_editor.models.particle_graph import ParticleGraph


class BaseProcessor(ABC):
    #: Lower runs first. Convention: 100 = normalize, 500 = optimize.
    order: int = 100
    name: str = "processor"

    @abstractmethod
    def process(self, graph: ParticleGraph) -> ParticleGraph:
        """Return the (possibly mutated) graph."""