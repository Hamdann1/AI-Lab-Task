"""Reflex and stateful (memory-based) climate agents for Lab 2.

Thresholds are SYNTHETIC LAB ASSUMPTIONS. The baseline reflex rule is
reconstructed from the lab description (the original lab code was not
supplied): temperature thresholds are kept, and occupancy has priority.
"""
from lab2_percepts import Percept

COOL_ABOVE_C = 26.0   # strictly above -> COOL
HEAT_BELOW_C = 18.0   # strictly below -> HEAT
# Exactly 26.0 or exactly 18.0 therefore falls in the comfortable band (IDLE).

MODE_COOL = "COOL"
MODE_HEAT = "HEAT"
MODE_IDLE = "IDLE"   # occupied and comfortable
MODE_OFF = "OFF"     # empty room


def reflex_target(percept: Percept) -> str:
    """Pure function of the current percept. Occupancy has priority."""
    if not percept.occupied:
        return MODE_OFF
    if percept.temperature_c > COOL_ABOVE_C:
        return MODE_COOL
    if percept.temperature_c < HEAT_BELOW_C:
        return MODE_HEAT
    return MODE_IDLE


def reflex_agent(percept: Percept):
    """Original behaviour: returns (target, send_command). Always sends."""
    return reflex_target(percept), True


class StatefulAgent:
    """Remembers the previous target mode and suppresses identical commands.

    step() returns (target_mode, send_command). A command is sent only when
    the target differs from the remembered previous target. The first percept
    always sends, because nothing has been commanded yet (previous is None).

    Assumption: a sent command is delivered. If an actuator drops a command,
    the remembered mode will be wrong (see report, limitations).
    """

    def __init__(self):
        self._previous_mode = None

    @property
    def previous_mode(self):
        return self._previous_mode

    def reset(self):
        self._previous_mode = None

    def step(self, percept: Percept):
        target = reflex_target(percept)
        send_command = target != self._previous_mode
        self._previous_mode = target
        return target, send_command
