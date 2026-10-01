"""CD-105 - Notify customers and agents on case events."""
from __future__ import annotations

from dataclasses import dataclass

from support_system import store
from support_system.models import Case, now

TEMPLATES: dict[str, str] = {
    "case_created": "Your case {reference} has been logged: {subject}",
    "case_assigned": "Case {reference} has been assigned to {assignee}",
    "case_resolved": "Case {reference} is resolved: {resolution_summary}",
    "case_closed": "Case {reference} is now closed. Thank you.",
    "customer_replied": "The customer has replied on case {reference}",
    "sla_breach": "Case {reference} has breached its service level target",
}


@dataclass
class Notification:
    to: str
    event: str
    body: str
    sent_at: object


def render(event: str, case: Case) -> str:
    """Templates are per event and rendered from the case itself, so a change of
    wording never means touching the code that triggers it."""
    template = TEMPLATES.get(event)
    if template is None:
        raise KeyError(f"no template for event {event!r}")
    return template.format(reference=case.reference, subject=case.subject,
                           assignee=case.assignee or "the team",
                           resolution_summary=case.resolution_summary or "")


def notify(case: Case, event: str, to: str) -> Notification:
    note = Notification(to=to, event=event, body=render(event, case), sent_at=now())
    store.notifications_sent.append(note)
    return note


def sent_for(reference: str) -> list[Notification]:
    return [n for n in store.notifications_sent if reference in n.body]
