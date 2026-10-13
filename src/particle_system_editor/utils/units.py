"""Unit conversions and formatting used by the editor UI."""
from __future__ import annotations


def format_rate(rate: float) -> str:
    """Human-readable emitter rate, e.g. 1500 -> '1.5k p/s'."""
    if rate >= 1000:
        return f"{rate / 1000:.1f}k p/s"
    return f"{rate:.0f} p/s"


def format_duration(seconds: float) -> str:
    if seconds < 1.0:
        return f"{seconds * 1000:.0f} ms"
    return f"{seconds:.2f} s"