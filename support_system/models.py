"""Core domain records for the support system."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Customer:
    account_ref: str
    name: str
    active: bool = True


@dataclass
class Contact:
    contact_id: str
    account_ref: str
    name: str
    email: str
    phone: str = ""


@dataclass
class Case:
    reference: str
    account_ref: str
    contact_id: str
    subject: str
    description: str = ""
    channel: str = "phone"
    status: str = "New"
    queue: str = ""
    assignee: str = ""
    category: str = "general"
    impact: str = "medium"
    urgency: str = "medium"
    priority: str = "Medium"
    priority_override_reason: str = ""
    resolution_code: str = ""
    resolution_summary: str = ""
    created_at: datetime = field(default_factory=now)
    closed_at: datetime | None = None
    csat_score: int | None = None


@dataclass
class Comment:
    reference: str
    author: str
    body: str
    internal: bool = False
    created_at: datetime = field(default_factory=now)


@dataclass
class WorkLogEntry:
    reference: str
    author: str
    minutes: int
    note: str = ""
    logged_at: datetime = field(default_factory=now)
