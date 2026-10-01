"""CD-107 - Suggest and link articles to a case."""
from __future__ import annotations

import re

from support_system import cases, kb_articles, workflow
from support_system.kb_articles import Article

STOPWORDS = {"the", "a", "an", "is", "are", "to", "for", "of", "and", "or", "on", "in",
             "with", "my", "our", "not", "no", "it", "this", "that", "cannot", "cant"}


def _tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]{3,}", (text or "").lower()) if w not in STOPWORDS}


def score(article: Article, subject: str) -> float:
    """Overlap on the subject words, with a tag match counted double because a tag
    was chosen deliberately by an author."""
    words = _tokens(subject)
    if not words:
        return 0.0
    title_hits = len(words & _tokens(article.title))
    tag_hits = len(words & set(article.tags))
    return (title_hits + 2 * tag_hits) / len(words)


def suggest(reference: str, limit: int = 3) -> list[tuple[Article, float]]:
    case = cases.require_case(reference)
    scored = [(a, score(a, case.subject)) for a in kb_articles.visible_articles()]
    return sorted([s for s in scored if s[1] > 0], key=lambda s: s[1], reverse=True)[:limit]


def link_as_resolution(reference: str, article_id: str, actor: str) -> str:
    """Resolving from an article records which one, and counts the use - that is
    how we learn which articles are actually earning their keep."""
    article = kb_articles.require_article(article_id)
    workflow.move(reference, "Resolved", actor=actor, resolution_code="kb-article",
                  resolution_summary=f"Resolved using article {article.article_id}: {article.title}")
    article.uses += 1
    return article.article_id
