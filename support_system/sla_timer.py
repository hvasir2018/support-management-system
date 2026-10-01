"""CD-103 - SLA timers with pause."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from support_system import cases, sla_policy
from support_system.models import now


@dataclass
class Timer:
    reference: str
    started_at: datetime
    paused_at: datetime | None = None
    paused_total: timedelta = field(default_factory=timedelta)


_timers: dict[str, Timer] = {}


def start(reference: str) -> Timer:
    """The clock starts when the case is created, not when somebody picks it up."""
    case = cases.require_case(reference)
    timer = Timer(reference=reference, started_at=case.created_at)
    _timers[reference] = timer
    return timer


def pause(reference: str) -> Timer:
    """Waiting on the customer is not our delay, so the clock stops."""
    timer = _require(reference)
    if timer.paused_at is None:
        timer.paused_at = now()
    return timer


def resume(reference: str) -> Timer:
    timer = _require(reference)
    if timer.paused_at is not None:
        timer.paused_total += now() - timer.paused_at
        timer.paused_at = None
    return timer


def elapsed_minutes(reference: str, at: datetime | None = None) -> int:
    """Wall-clock time minus every paused period."""
    timer = _require(reference)
    at = at or now()
    paused = timer.paused_total
    if timer.paused_at is not None:
        paused += at - timer.paused_at
    return int(((at - timer.started_at) - paused).total_seconds() // 60)


def remaining_minutes(reference: str) -> int | None:
    case = cases.require_case(reference)
    target = sla_policy.resolution_target(case.priority)
    return None if target is None else target - elapsed_minutes(reference)


def _require(reference: str) -> Timer:
    timer = _timers.get(reference)
    if timer is None:
        raise KeyError(f"no timer running for {reference}")
    return timer
