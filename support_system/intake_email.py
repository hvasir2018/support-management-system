"""CD-94 - Create a case from inbound email."""
from __future__ import annotations

import re

from support_system import cases, contacts, store
from support_system.models import Case, Comment

REF_IN_SUBJECT = re.compile(r"\b(CASE-\d{6})\b")


def handle_inbound(from_email: str, subject: str, body: str) -> Case:
    """A reply on an existing thread appends to that case; anything else opens a
    new one. Nothing a customer sends in is ever dropped."""
    existing = REF_IN_SUBJECT.search(subject or "")
    if existing:
        reference = existing.group(1)
        if store.cases.exists(reference):
            store.comments.append(Comment(reference=reference, author=from_email,
                                          body=body, internal=False))
            return cases.require_case(reference)
    contact = contacts.find_by_email(from_email)
    if contact is None:
        raise LookupError(f"no contact matches {from_email}; agent must triage manually")
    return cases.open_case(account_ref=contact.account_ref, contact_id=contact.contact_id,
                           subject=(subject or "(no subject)").strip(), description=body,
                           channel="email")


def reply_subject(reference: str, subject: str) -> str:
    """Outbound replies carry the reference so the next message threads correctly."""
    return subject if reference in subject else f"[{reference}] {subject}"
