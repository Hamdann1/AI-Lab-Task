"""Percept definition and scenario loading for Lab 2.

A percept is what the agent senses at one time step: room temperature and
whether the room is occupied. All values used by the lab are synthetic.
"""
import json
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Percept:
    temperature_c: float
    occupied: bool

    def __post_init__(self):
        # Reject missing / non-numeric / NaN temperatures instead of guessing.
        if isinstance(self.temperature_c, bool) or not isinstance(self.temperature_c, (int, float)):
            raise ValueError(f"temperature_c must be a number, got {self.temperature_c!r}")
        if math.isnan(self.temperature_c):
            raise ValueError("temperature_c must not be NaN")
        if not isinstance(self.occupied, bool):
            raise ValueError(f"occupied must be True/False, got {self.occupied!r}")

    def __str__(self):
        room = "occupied" if self.occupied else "empty"
        return f"{self.temperature_c:.1f} C, {room}"


def load_inputs(path):
    """Load the scenario file. Returns the parsed JSON dictionary."""
    with open(Path(path), encoding="utf-8") as f:
        return json.load(f)


def to_percept(step):
    return Percept(float(step["temperature_c"]), bool(step["occupied"]))
