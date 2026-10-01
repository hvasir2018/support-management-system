"""CD-102 - Define SLA policies."""
from __future__ import annotations

from dataclasses import dataclass, field

from support_system import store


@dataclass
class SlaPolicy:
    name: str
    response_minutes: dict[str, int] = field(default_factory=dict)
    resolution_minutes: dict[str, int] = field(default_factory=dict)
    active: bool = False


PRIORITIES = ("Critical", "High", "Medium", "Low")


def create_policy(name: str, response: dict[str, int], resolution: dict[str, int]) -> SlaPolicy:
    """Targets are per priority and must be positive - a zero or negative target
    would make every case instantly breached."""
    for table, label in ((response, "response"), (resolution, "resolution")):
        missing = [p for p in PRIORITIES if p not in table]
        if missing:
            raise ValueError(f"{label} target missing for {', '.join(missing)}")
        for p, minutes in table.items():
            if minutes <= 0:
                raise ValueError(f"{label} target for {p} must be positive")
    policy = SlaPolicy(name=name, response_minutes=dict(response),
                       resolution_minutes=dict(resolution))
    return store.policies.put(name, policy)


def activate(name: str) -> SlaPolicy:
    """Exactly one policy is active, so there is never ambiguity about the target."""
    policy = store.policies.get(name)
    if policy is None:
        raise KeyError(f"no policy {name}")
    for other in store.policies.all():
        other.active = False
    policy.active = True
    return policy


def active_policy() -> SlaPolicy | None:
    return next((p for p in store.policies.all() if p.active), None)


def resolution_target(priority: str) -> int | None:
    policy = active_policy()
    return policy.resolution_minutes.get(priority) if policy else None
