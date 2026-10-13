"""Sanity-normalize a freshly ingested graph.

Fixes values that are technically parseable but nonsensical: negative
rates, zero lifetimes, inverted size ramps. Always runs first (order=100).
"""
from __future__ import annotations

from particle_system_editor.models.particle_graph import ParticleGraph
from particle_system_editor.processors.base_processor import BaseProcessor


class NormalizeProcessor(BaseProcessor):
    order = 100
    name = "normalize"

    def process(self, graph: ParticleGraph) -> ParticleGraph:
        for emitter in graph.emitters:
            if emitter.rate < 0:
                emitter.rate = abs(emitter.rate)
            if emitter.lifetime <= 0:
                emitter.lifetime = 1.0
            if emitter.size_start < 0:
                emitter.size_start = 0.0
            if emitter.size_end < 0:
                emitter.size_end = 0.0
        return graph