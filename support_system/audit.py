"""CD-111 - Immutable case audit trail."""
from __future__ import annotations

from dataclasses import dataclass

from support_system import store
from support_system.models import now


@dataclass(frozen=True)
class AuditEntry:
    """Frozen on purpose: an audit entry that can be edited is not an audit trail."""
    reference: str
    actor: str
    field: str
    before: str
    after: str
    at: object


def record(reference: str, actor: str, field: str, before, after) -> AuditEntry:
    entry = AuditEntry(reference=reference, actor=actor, field=field,
                       before="" if before is None else str(before),
                       after="" if after is None else str(after), at=now())
    store.audit_entries.append(entry)
    return entry


def trail(reference: str) -> list[AuditEntry]:
    """Queryable per case, oldest first - the order you want when reconstructing
    what happened."""
    rows = [e for e in store.audit_entries if e.reference == reference]
    return sorted(rows, key=lambda e: e.at)


def changes_by(actor: str) -> list[AuditEntry]:
    return [e for e in store.audit_entries if e.actor == actor]


def field_history(reference: str, field: str) -> list[AuditEntry]:
    return [e for e in trail(reference) if e.field == field]
