"""CD-98 - Case status workflow."""
from __future__ import annotations

from support_system import audit, cases
from support_system.models import Case, now

TRANSITIONS: dict[str, tuple[str, ...]] = {
    "New": ("Assigned", "In Progress", "Closed"),
    "Assigned": ("In Progress", "Pending Customer", "Closed"),
    "In Progress": ("Pending Customer", "Resolved", "Closed"),
    "Pending Customer": ("In Progress", "Resolved", "Closed"),
    "Resolved": ("Closed", "In Progress"),
    "Closed": (),
}


class InvalidTransition(ValueError):
    """Raised with the reason, so the caller can show it to the agent."""


def can_move(current: str, target: str) -> bool:
    return target in TRANSITIONS.get(current, ())


def move(reference: str, target: str, actor: str,
         resolution_code: str = "", resolution_summary: str = "") -> Case:
    """Drive the lifecycle. Resolving demands a resolution code, because a case
    closed without one tells us nothing when we look back at it."""
    case = cases.require_case(reference)
    if not can_move(case.status, target):
        raise InvalidTransition(f"cannot move {case.reference} from {case.status} to {target}")
    if target == "Resolved" and not resolution_code:
        raise InvalidTransition("a resolution code is required to resolve a case")
    previous = case.status
    case.status = target
    if target == "Resolved":
        case.resolution_code = resolution_code
        case.resolution_summary = resolution_summary
    if target == "Closed":
        case.closed_at = now()
    audit.record(reference, actor=actor, field="status", before=previous, after=target)
    return case
