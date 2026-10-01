"""CD-99 - Priority from impact and urgency."""
from __future__ import annotations

from support_system import audit, cases
from support_system.models import Case

LEVELS = ("low", "medium", "high")
MATRIX = {
    ("high", "high"): "Critical", ("high", "medium"): "High", ("high", "low"): "Medium",
    ("medium", "high"): "High", ("medium", "medium"): "Medium", ("medium", "low"): "Low",
    ("low", "high"): "Medium", ("low", "medium"): "Low", ("low", "low"): "Low",
}
ORDER = ["Low", "Medium", "High", "Critical"]


def derive(impact: str, urgency: str) -> str:
    """The 3x3 matrix. Keeping it a pure function makes it trivial to test and to
    show to a customer who asks why their case is a Medium."""
    if impact not in LEVELS or urgency not in LEVELS:
        raise ValueError("impact and urgency must be low, medium or high")
    return MATRIX[(impact, urgency)]


def apply_priority(reference: str, impact: str, urgency: str, actor: str) -> Case:
    case = cases.require_case(reference)
    previous = case.priority
    case.impact, case.urgency = impact, urgency
    case.priority = derive(impact, urgency)
    case.priority_override_reason = ""
    audit.record(reference, actor=actor, field="priority", before=previous, after=case.priority)
    return case


def override(reference: str, priority: str, reason: str, actor: str) -> Case:
    """A human may always disagree with the matrix - but must say why."""
    if priority not in ORDER:
        raise ValueError(f"unknown priority {priority!r}")
    if not (reason or "").strip():
        raise ValueError("an override needs a reason")
    case = cases.require_case(reference)
    previous = case.priority
    case.priority = priority
    case.priority_override_reason = reason.strip()
    audit.record(reference, actor=actor, field="priority", before=previous, after=priority)
    return case


def escalate_one_step(reference: str, actor: str) -> Case:
    case = cases.require_case(reference)
    idx = min(ORDER.index(case.priority) + 1, len(ORDER) - 1)
    return override(reference, ORDER[idx], "SLA breach escalation", actor)
