"""Clamp a graph to a particle budget.

Keeps the editor responsive when a source file asks for more particles
than the preview or the target hardware can handle. Scales emitter rates
proportionally so the *shape* of the effect survives the clamp.
"""
from __future__ import annotations

import logging

from particle_system_editor.models.particle_graph import ParticleGraph
from particle_system_editor.processors.base_processor import BaseProcessor

log = logging.getLogger(__name__)


class BudgetProcessor(BaseProcessor):
    order = 500
    name = "budget"

    def __init__(self, max_particles: int = 1_000_000) -> None:
        self.max_particles = max_particles

    def process(self, graph: ParticleGraph) -> ParticleGraph:
        peak = graph.estimated_peak()
        if peak <= self.max_particles or peak == 0:
            return graph
        scale = self.max_particles / peak
        for emitter in graph.emitters:
            emitter.rate *= scale
        log.info(
            "budget clamp: %d -> %d particles (scale %.3f)",
            peak,
            self.max_particles,
            scale,
        )
        graph.max_particles = self.max_particles
        return graph