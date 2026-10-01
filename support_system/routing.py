"""CD-97 - Queues and routing rules."""
from __future__ import annotations

from dataclasses import dataclass

from support_system import audit, cases
from support_system.models import Case

DEFAULT_QUEUE = "general-support"


@dataclass
class Rule:
    category: str | None
    channel: str | None
    queue: str

    def matches(self, case: Case) -> bool:
        if self.category and self.category != case.category:
            return False
        if self.channel and self.channel != case.channel:
            return False
        return True


RULES: list[Rule] = [
    Rule(category="billing", channel=None, queue="billing"),
    Rule(category="outage", channel=None, queue="incident"),
    Rule(category=None, channel="web", queue="web-triage"),
]


def route(reference: str) -> str:
    """First matching rule wins; anything unmatched falls to the default queue so
    no case is ever left without an owning team."""
    case = cases.require_case(reference)
    for rule in RULES:
        if rule.matches(case):
            return _apply(case, rule.queue)
    return _apply(case, DEFAULT_QUEUE)


def _apply(case: Case, queue: str) -> str:
    previous = case.queue
    case.queue = queue
    audit.record(case.reference, actor="router", field="queue", before=previous, after=queue)
    return queue
