"""CD-92 - Case model and reference numbering."""
from __future__ import annotations

from itertools import count

from support_system import contacts, customers, store
from support_system.models import Case

_sequence = count(1)
VALID_CHANNELS = ("phone", "email", "web", "chat")


def next_reference() -> str:
    """Human-quotable and never reused: CASE-000001, CASE-000002, ..."""
    return f"CASE-{next(_sequence):06d}"


def open_case(account_ref: str, contact_id: str, subject: str, description: str = "",
              channel: str = "phone", category: str = "general") -> Case:
    """Create a case against an active customer and one of its contacts. The
    channel is fixed here because it records how the customer actually reached us."""
    if channel not in VALID_CHANNELS:
        raise ValueError(f"unknown channel {channel!r}")
    customers.require_active_customer(account_ref)
    contact = contacts.require_contact(contact_id)
    if contact.account_ref != account_ref:
        raise ValueError("contact does not belong to that customer")
    if not (subject or "").strip():
        raise ValueError("a case needs a subject")
    case = Case(reference=next_reference(), account_ref=account_ref, contact_id=contact_id,
                subject=subject.strip(), description=description, channel=channel,
                category=category)
    return store.cases.put(case.reference, case)


def require_case(reference: str) -> Case:
    case = store.cases.get(reference)
    if case is None:
        raise KeyError(f"no case {reference}")
    return case


def cases_for_customer(account_ref: str) -> list[Case]:
    return [c for c in store.cases.all() if c.account_ref == account_ref]
