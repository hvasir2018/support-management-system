"""CD-101 - Attachments on a case."""
from __future__ import annotations

from dataclasses import dataclass

from support_system import cases, store
from support_system.models import now

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".txt", ".log", ".csv", ".docx", ".xlsx"}
MAX_BYTES = 10 * 1024 * 1024


@dataclass
class Attachment:
    reference: str
    filename: str
    size_bytes: int
    uploaded_by: str
    uploaded_at: object


class RejectedUpload(ValueError):
    """Carries the reason, so the agent is told what to do about it."""


def _extension(filename: str) -> str:
    return filename[filename.rfind("."):].lower() if "." in filename else ""


def attach(reference: str, filename: str, size_bytes: int, uploaded_by: str) -> Attachment:
    """Evidence travels with the case. Rejections always explain themselves."""
    cases.require_case(reference)
    ext = _extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise RejectedUpload(f"{ext or 'files with no extension'} is not an accepted type")
    if size_bytes > MAX_BYTES:
        raise RejectedUpload(f"{filename} is {size_bytes} bytes, over the {MAX_BYTES} limit")
    item = Attachment(reference=reference, filename=filename, size_bytes=size_bytes,
                      uploaded_by=uploaded_by, uploaded_at=now())
    store.attachments.append(item)
    return item


def attachments_for(reference: str) -> list[Attachment]:
    return [a for a in store.attachments if a.reference == reference]
