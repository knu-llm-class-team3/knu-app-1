"""Tools available to the lawyer agent nodes.

Currently provides:
- search_case_law: keyword-based similarity search over mocked case law data.
"""

from __future__ import annotations

import json
import os
from typing import Optional

from langchain_core.tools import tool


# ---------------------------------------------------------------------------
# Load mocked case law data once at import time
# ---------------------------------------------------------------------------
_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "case_law.json")

with open(_DATA_PATH, encoding="utf-8") as _f:
    _CASE_LAW: list[dict] = json.load(_f)


def _score(case: dict, query: str) -> int:
    """Simple keyword overlap scoring between a query and a case entry."""
    query_tokens = set(query.lower().split())
    case_tokens = set(" ".join(case["keywords"] + [case["title"], case["summary"]]).lower().split())
    return len(query_tokens & case_tokens)


@tool
def search_case_law(query: str, category: Optional[str] = None, top_k: int = 3) -> str:
    """Search mocked Korean case law data for cases relevant to the user's question.

    Args:
        query: A natural-language description of the legal issue.
        category: Optional law category filter.
                  One of 'civil', 'criminal', 'administrative', 'family'.
        top_k: Number of top results to return (default 3).

    Returns:
        A formatted string listing the most relevant cases.
    """
    candidates = _CASE_LAW
    if category:
        candidates = [c for c in candidates if c["category"] == category]

    scored = sorted(candidates, key=lambda c: _score(c, query), reverse=True)
    top = scored[:top_k]

    if not top:
        return "관련 판례를 찾을 수 없습니다."

    lines = []
    for case in top:
        lines.append(
            f"[{case['id']}] {case['title']}\n"
            f"  카테고리: {case['category']}\n"
            f"  요약: {case['summary']}\n"
            f"  키워드: {', '.join(case['keywords'])}"
        )
    return "\n\n".join(lines)
