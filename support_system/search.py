"""CD-108 - Search and filter cases."""
from __future__ import annotations

from datetime import datetime

from support_system import store
from support_system.models import Case


def matches(case: Case, status=None, priority=None, queue=None, assignee=None,
            text=None, created_from=None, created_to=None) -> bool:
    """Every supplied filter must hold - they combine with AND, which is what an
    agent narrowing a list actually expects."""
    if status and case.status != status:
        return False
    if priority and case.priority != priority:
        return False
    if queue and case.queue != queue:
        return False
    if assignee and case.assignee != assignee:
        return False
    if created_from and case.created_at < created_from:
        return False
    if created_to and case.created_at > created_to:
        return False
    if text:
        needle = text.lower()
        if needle not in case.subject.lower() and needle not in (case.description or "").lower():
            return False
    return True


def find(**filters) -> list[Case]:
    rows = [c for c in store.cases.all() if matches(c, **filters)]
    return sorted(rows, key=lambda c: c.created_at, reverse=True)


def my_open_cases(agent: str) -> list[Case]:
    return [c for c in find(assignee=agent) if c.status not in ("Resolved", "Closed")]


def queue_backlog(queue: str) -> list[Case]:
    from support_system.priority import ORDER
    rows = [c for c in find(queue=queue) if c.status not in ("Resolved", "Closed")]
    return sorted(rows, key=lambda c: ORDER.index(c.priority), reverse=True)
