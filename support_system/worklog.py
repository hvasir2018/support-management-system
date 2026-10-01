"""CD-100 - Comments and work log."""
from __future__ import annotations

from support_system import cases, store
from support_system.models import Comment, WorkLogEntry


def add_comment(reference: str, author: str, body: str, internal: bool = False) -> Comment:
    """Internal notes are flagged here and filtered on the way out - the customer
    never sees them."""
    cases.require_case(reference)
    if not (body or "").strip():
        raise ValueError("a comment needs a body")
    entry = Comment(reference=reference, author=author, body=body.strip(), internal=internal)
    store.comments.append(entry)
    return entry


def comments_for(reference: str, include_internal: bool = True) -> list[Comment]:
    rows = [c for c in store.comments if c.reference == reference]
    return rows if include_internal else [c for c in rows if not c.internal]


def customer_visible(reference: str) -> list[Comment]:
    """What the customer portal is allowed to render."""
    return comments_for(reference, include_internal=False)


def log_time(reference: str, author: str, minutes: int, note: str = "") -> WorkLogEntry:
    cases.require_case(reference)
    if minutes <= 0:
        raise ValueError("logged time must be positive")
    entry = WorkLogEntry(reference=reference, author=author, minutes=int(minutes), note=note)
    store.worklog.append(entry)
    return entry


def total_minutes(reference: str) -> int:
    return sum(e.minutes for e in store.worklog if e.reference == reference)
