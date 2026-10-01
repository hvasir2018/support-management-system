"""CD-95 - Submit a case from the web form."""
from __future__ import annotations

from support_system import cases, contacts, notifications
from support_system.models import Case

REQUIRED_FIELDS = ("account_ref", "contact_id", "subject")


def validate(form: dict) -> list[str]:
    """Return the problems with a submission, empty when it is good to go."""
    problems = [f"{f} is required" for f in REQUIRED_FIELDS if not (form.get(f) or "").strip()]
    if form.get("contact_id") and not store_has_contact(form["contact_id"]):
        problems.append("unknown contact")
    return problems


def store_has_contact(contact_id: str) -> bool:
    from support_system import store
    return store.contacts.exists(contact_id)


def submit(form: dict) -> Case:
    """Self-service: the customer raises the case and is emailed the reference."""
    problems = validate(form)
    if problems:
        raise ValueError("; ".join(problems))
    case = cases.open_case(account_ref=form["account_ref"], contact_id=form["contact_id"],
                           subject=form["subject"], description=form.get("description", ""),
                           channel="web", category=form.get("category", "general"))
    contact = contacts.require_contact(case.contact_id)
    notifications.notify(case, "case_created", to=contact.email)
    return case
