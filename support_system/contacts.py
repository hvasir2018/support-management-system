"""CD-91 - Maintain contacts under a customer."""
from __future__ import annotations

import re
import uuid

from support_system import customers, store
from support_system.models import Contact

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match((email or "").strip()))


def add_contact(account_ref: str, name: str, email: str, phone: str = "") -> Contact:
    """Attach a contact to a customer. A contact belongs to exactly one customer,
    so the customer must exist before the contact can."""
    customers.require_customer(account_ref)
    if not valid_email(email):
        raise ValueError(f"invalid email: {email!r}")
    contact = Contact(contact_id=uuid.uuid4().hex[:10], account_ref=account_ref,
                      name=(name or "").strip(), email=email.strip(), phone=(phone or "").strip())
    return store.contacts.put(contact.contact_id, contact)


def require_contact(contact_id: str) -> Contact:
    contact = store.contacts.get(contact_id)
    if contact is None:
        raise KeyError(f"no contact {contact_id}")
    return contact


def contacts_for(account_ref: str) -> list[Contact]:
    return [c for c in store.contacts.all() if c.account_ref == account_ref]


def find_by_email(email: str) -> Contact | None:
    """Used by email intake to attach an inbound message to a known person."""
    email = (email or "").strip().lower()
    for contact in store.contacts.all():
        if contact.email.lower() == email:
            return contact
    return None
