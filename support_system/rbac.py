"""CD-110 - Role-based access control."""
from __future__ import annotations

from support_system import cases

AGENT, LEAD, AUTHOR, ADMIN, CUSTOMER = "agent", "lead", "author", "administrator", "customer"

PERMISSIONS: dict[str, set[str]] = {
    AGENT: {"case:read", "case:comment", "case:resolve", "kb:read"},
    LEAD: {"case:read", "case:comment", "case:resolve", "case:assign", "case:reroute",
           "kb:read", "report:read"},
    AUTHOR: {"kb:read", "kb:write", "kb:publish", "case:read"},
    ADMIN: {"case:read", "case:comment", "case:resolve", "case:assign", "case:reroute",
            "kb:read", "kb:write", "kb:publish", "report:read", "admin:users", "admin:sla"},
    CUSTOMER: {"case:read_own"},
}


class AccessDenied(PermissionError):
    """Carries which role lacked which permission, so the message is actionable."""


def has_permission(role: str, permission: str) -> bool:
    return permission in PERMISSIONS.get(role, set())


def require(role: str, permission: str) -> None:
    if not has_permission(role, permission):
        raise AccessDenied(f"role {role!r} may not {permission}")


def can_view_case(role: str, actor_account_ref: str, reference: str) -> bool:
    """A customer sees only their own cases - enforced here rather than trusted to
    every caller remembering to filter."""
    case = cases.require_case(reference)
    if role == CUSTOMER:
        return case.account_ref == actor_account_ref
    return has_permission(role, "case:read")


def require_view(role: str, actor_account_ref: str, reference: str) -> None:
    if not can_view_case(role, actor_account_ref, reference):
        raise AccessDenied(f"role {role!r} may not view {reference}")
