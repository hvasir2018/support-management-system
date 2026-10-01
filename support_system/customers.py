"""CD-90 - Maintain customer records."""
from __future__ import annotations

from support_system import store
from support_system.models import Customer


class DuplicateAccountRef(ValueError):
    """Raised when an account reference is already taken."""


class InactiveCustomer(ValueError):
    """Raised when work is attempted against a deactivated customer."""


def create_customer(account_ref: str, name: str) -> Customer:
    """Register a customer. The account reference is the natural key, so it must
    be unique - a duplicate is a caller error rather than a silent overwrite."""
    account_ref = (account_ref or "").strip()
    name = (name or "").strip()
    if not account_ref or not name:
        raise ValueError("account_ref and name are required")
    if store.customers.exists(account_ref):
        raise DuplicateAccountRef(f"account {account_ref} already exists")
    return store.customers.put(account_ref, Customer(account_ref=account_ref, name=name))


def update_customer(account_ref: str, name: str | None = None, active: bool | None = None) -> Customer:
    customer = require_customer(account_ref)
    if name is not None:
        customer.name = name.strip() or customer.name
    if active is not None:
        customer.active = bool(active)
    return customer


def require_customer(account_ref: str) -> Customer:
    """Fetch a customer or explain why it cannot be used."""
    customer = store.customers.get(account_ref)
    if customer is None:
        raise KeyError(f"no customer {account_ref}")
    return customer


def require_active_customer(account_ref: str) -> Customer:
    """Used by case intake: an inactive customer may not raise new cases."""
    customer = require_customer(account_ref)
    if not customer.active:
        raise InactiveCustomer(f"customer {account_ref} is inactive")
    return customer


def list_customers(include_inactive: bool = True) -> list[Customer]:
    rows = store.customers.all()
    return rows if include_inactive else [c for c in rows if c.active]
