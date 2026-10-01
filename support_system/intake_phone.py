"""CD-93 - Log a phone call and raise a case."""
from __future__ import annotations

from support_system import cases, contacts, customers
from support_system.models import Case


def log_call(account_ref: str, contact_id: str, subject: str, call_notes: str,
             category: str = "general") -> Case:
    """One step from a ringing phone to an open case, so the agent can keep the
    caller talking instead of typing the same thing twice."""
    case = cases.open_case(account_ref=account_ref, contact_id=contact_id, subject=subject,
                           description=call_notes, channel="phone", category=category)
    return case


def identify_caller(phone: str) -> tuple[str, str] | None:
    """Caller line identity to (account_ref, contact_id), for the intake screen."""
    digits = "".join(ch for ch in (phone or "") if ch.isdigit())
    if not digits:
        return None
    for contact in _all_contacts():
        if "".join(ch for ch in contact.phone if ch.isdigit()).endswith(digits[-7:]):
            return contact.account_ref, contact.contact_id
    return None


def _all_contacts():
    from support_system import store
    return store.contacts.all()


def quick_create(phone: str, subject: str, call_notes: str) -> Case | None:
    """Identify the caller from CLI and open the case, or return None so the agent
    can search manually."""
    found = identify_caller(phone)
    if not found:
        return None
    account_ref, contact_id = found
    return log_call(account_ref, contact_id, subject, call_notes)
