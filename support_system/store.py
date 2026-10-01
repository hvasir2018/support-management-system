"""In-memory repositories. A real deployment swaps these for a database."""
from __future__ import annotations

from typing import Any


class Repository:
    """A tiny keyed collection with the handful of operations the modules need."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._items: dict[str, Any] = {}

    def put(self, key: str, value: Any) -> Any:
        self._items[key] = value
        return value

    def get(self, key: str) -> Any | None:
        return self._items.get(key)

    def exists(self, key: str) -> bool:
        return key in self._items

    def all(self) -> list[Any]:
        return list(self._items.values())

    def delete(self, key: str) -> bool:
        return self._items.pop(key, None) is not None

    def __len__(self) -> int:
        return len(self._items)


customers = Repository("customers")
contacts = Repository("contacts")
cases = Repository("cases")
articles = Repository("articles")
policies = Repository("sla_policies")

comments: list = []
worklog: list = []
attachments: list = []
audit_entries: list = []
notifications_sent: list = []
surveys: list = []
