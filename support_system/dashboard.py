"""CD-109 - Support dashboard metrics."""
from __future__ import annotations

from statistics import mean, median

from support_system import escalation, store
from support_system.models import Case

OPEN_STATES = ("New", "Assigned", "In Progress", "Pending Customer")


def open_cases() -> list[Case]:
    return [c for c in store.cases.all() if c.status in OPEN_STATES]


def by_queue() -> dict[str, int]:
    counts: dict[str, int] = {}
    for case in open_cases():
        counts[case.queue or "unassigned"] = counts.get(case.queue or "unassigned", 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: kv[1], reverse=True))


def by_priority() -> dict[str, int]:
    counts: dict[str, int] = {}
    for case in open_cases():
        counts[case.priority] = counts.get(case.priority, 0) + 1
    return counts


def resolution_times_minutes() -> list[int]:
    out = []
    for case in store.cases.all():
        if case.closed_at:
            out.append(int((case.closed_at - case.created_at).total_seconds() // 60))
    return out


def sla_compliance() -> float:
    """The headline number: share of open cases still inside their target."""
    rows = open_cases()
    if not rows:
        return 100.0
    breached = sum(1 for c in rows if _safe_breached(c.reference))
    return round(100.0 * (len(rows) - breached) / len(rows), 1)


def _safe_breached(reference: str) -> bool:
    try:
        return escalation.evaluate(reference).breached
    except KeyError:
        return False


def summary() -> dict:
    times = resolution_times_minutes()
    return {"open_total": len(open_cases()), "by_queue": by_queue(), "by_priority": by_priority(),
            "sla_compliance_pct": sla_compliance(),
            "mean_resolution_minutes": round(mean(times), 1) if times else None,
            "median_resolution_minutes": round(median(times), 1) if times else None}
