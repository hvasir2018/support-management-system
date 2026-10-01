"""CD-106 - Author knowledge base articles."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from support_system import store
from support_system.models import now

DRAFT, PUBLISHED, RETIRED = "draft", "published", "retired"


@dataclass
class Article:
    article_id: str
    title: str
    body: str
    tags: list[str] = field(default_factory=list)
    status: str = DRAFT
    uses: int = 0
    updated_at: object = None


def create_article(title: str, body: str, tags: list[str] | None = None) -> Article:
    article = Article(article_id=uuid.uuid4().hex[:8], title=title.strip(), body=body,
                      tags=[t.lower().strip() for t in (tags or [])], updated_at=now())
    return store.articles.put(article.article_id, article)


def edit_article(article_id: str, title: str | None = None, body: str | None = None,
                 tags: list[str] | None = None) -> Article:
    article = require_article(article_id)
    if title is not None:
        article.title = title.strip()
    if body is not None:
        article.body = body
    if tags is not None:
        article.tags = [t.lower().strip() for t in tags]
    article.updated_at = now()
    return article


def publish(article_id: str) -> Article:
    article = require_article(article_id)
    article.status = PUBLISHED
    return article


def retire(article_id: str) -> Article:
    """Retiring hides an article from agents but keeps it, because a case resolved
    with it last year must still make sense."""
    article = require_article(article_id)
    article.status = RETIRED
    return article


def require_article(article_id: str) -> Article:
    article = store.articles.get(article_id)
    if article is None:
        raise KeyError(f"no article {article_id}")
    return article


def visible_articles() -> list[Article]:
    return [a for a in store.articles.all() if a.status == PUBLISHED]


def search(text: str) -> list[Article]:
    """Title, body and tag - the three places an agent expects a match."""
    needle = (text or "").lower().strip()
    if not needle:
        return []
    return [a for a in visible_articles()
            if needle in a.title.lower() or needle in a.body.lower()
            or any(needle in t for t in a.tags)]
