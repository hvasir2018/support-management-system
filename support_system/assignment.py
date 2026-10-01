"""CD-96 - Assign a case to an agent."""
from __future__ import annotations

from support_system import audit, cases
from support_system.models import Case

ACTIVE_AGENTS: set[str] = {"amara", "ben", "chi", "dev", "erin"}


class UnknownAgent(ValueError):
    """Raised when assigning to somebody who cannot take work."""


def assign(reference: str, agent: str, assigned_by: str) -> Case:
    """Give the case an owner. Reassignment is allowed and keeps the history, so
    the audit trail shows every hand it passed through."""
    case = cases.require_case(reference)
    if agent not in ACTIVE_AGENTS:
        raise UnknownAgent(f"{agent} is not an active agent")
    previous = case.assignee
    case.assignee = agent
    if case.status == "New":
        case.status = "Assigned"
    audit.record(reference, actor=assigned_by, field="assignee", before=previous, after=agent)
    return case


def unassign(reference: str, actor: str) -> Case:
    case = cases.require_case(reference)
    previous = case.assignee
    case.assignee = ""
    audit.record(reference, actor=actor, field="assignee", before=previous, after="")
    return case


def workload() -> dict[str, int]:
    """Open cases per agent - the input to any fair-share routing."""
    from support_system import store
    counts = {a: 0 for a in ACTIVE_AGENTS}
    for case in store.cases.all():
        if case.assignee and case.status not in ("Resolved", "Closed"):
            counts[case.assignee] = counts.get(case.assignee, 0) + 1
    return counts
