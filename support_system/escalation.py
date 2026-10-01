"""CD-104 - Breach detection and escalation."""
from __future__ import annotations

from dataclasses import dataclass

from support_system import cases, notifications, priority, sla_policy, sla_timer

WARN_AT = 0.8
TEAM_LEAD = "chi"


@dataclass
class SlaState:
    reference: str
    elapsed: int
    target: int | None
    warned: bool
    breached: bool
    overrun: int


def evaluate(reference: str) -> SlaState:
    """A warning at 80% of target gives the lead time to act before the customer
    has anything to complain about; past 100% we record the overrun."""
    case = cases.require_case(reference)
    target = sla_policy.resolution_target(case.priority)
    elapsed = sla_timer.elapsed_minutes(reference)
    if target is None:
        return SlaState(reference, elapsed, None, False, False, 0)
    return SlaState(reference=reference, elapsed=elapsed, target=target,
                    warned=elapsed >= target * WARN_AT, breached=elapsed > target,
                    overrun=max(0, elapsed - target))


def escalate_if_breached(reference: str) -> SlaState:
    """Escalation is deliberate and visible: the lead is notified and the priority
    goes up one step, which is itself written to the audit trail."""
    state = evaluate(reference)
    if state.breached:
        case = cases.require_case(reference)
        priority.escalate_one_step(reference, actor="sla-monitor")
        notifications.notify(case, "sla_breach", to=TEAM_LEAD)
    return state


def sweep(references: list[str]) -> list[SlaState]:
    return [escalate_if_breached(r) for r in references]
