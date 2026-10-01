"""CD-112 - Customer satisfaction survey."""
from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from support_system import cases, contacts, notifications, store
from support_system.models import now

MIN_SCORE, MAX_SCORE = 1, 5


@dataclass
class Survey:
    reference: str
    score: int | None = None
    comment: str = ""
    sent_at: object = None
    answered_at: object = None


def send_survey(reference: str) -> Survey:
    """Sent on closure, when the experience is still fresh."""
    case = cases.require_case(reference)
    if case.status != "Closed":
        raise ValueError("a survey is only sent once the case is closed")
    contact = contacts.require_contact(case.contact_id)
    notifications.notify(case, "case_closed", to=contact.email)
    survey = Survey(reference=reference, sent_at=now())
    store.surveys.append(survey)
    return survey


def record_response(reference: str, score: int, comment: str = "") -> Survey:
    if not MIN_SCORE <= score <= MAX_SCORE:
        raise ValueError(f"score must be {MIN_SCORE}-{MAX_SCORE}")
    survey = next((s for s in store.surveys if s.reference == reference and s.score is None), None)
    if survey is None:
        raise KeyError(f"no outstanding survey for {reference}")
    survey.score, survey.comment, survey.answered_at = int(score), comment, now()
    cases.require_case(reference).csat_score = int(score)
    return survey


def _answered() -> list[Survey]:
    return [s for s in store.surveys if s.score is not None]


def average_score() -> float | None:
    rows = _answered()
    return round(mean(s.score for s in rows), 2) if rows else None


def by_agent() -> dict[str, float]:
    """Rolls up per agent, which is what a one-to-one actually needs."""
    buckets: dict[str, list[int]] = {}
    for survey in _answered():
        agent = cases.require_case(survey.reference).assignee or "unassigned"
        buckets.setdefault(agent, []).append(survey.score)
    return {a: round(mean(v), 2) for a, v in sorted(buckets.items())}


def by_queue() -> dict[str, float]:
    buckets: dict[str, list[int]] = {}
    for survey in _answered():
        queue = cases.require_case(survey.reference).queue or "unassigned"
        buckets.setdefault(queue, []).append(survey.score)
    return {q: round(mean(v), 2) for q, v in sorted(buckets.items())}
