"""LangGraph node functions for the lawyer agent.

Nodes:
- router_node   : classifies the user's question into a law category
- civil_node    : handles civil law (민사) questions
- criminal_node : handles criminal law (형사) questions
- admin_node    : handles administrative law (행정) questions
- family_node   : handles family law (가사) questions
"""

from __future__ import annotations

from typing import cast

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from state import AgentState, LawCategory
from tools import search_case_law

# ---------------------------------------------------------------------------
# Shared LLM instance  (model can be overridden via env var OPENAI_MODEL)
# ---------------------------------------------------------------------------
import os

_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
_llm = ChatOpenAI(model=_MODEL, temperature=0)
_llm_with_tools = _llm.bind_tools([search_case_law])

# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------
_ROUTER_PROMPT = SystemMessage(
    content=(
        "당신은 법률 상담 분류 전문가입니다.\n"
        "사용자의 질문을 읽고 가장 적합한 법률 카테고리를 아래 중 하나로만 답하세요:\n"
        "civil (민사), criminal (형사), administrative (행정), family (가사), unknown\n"
        "반드시 영문 소문자 한 단어만 출력하세요."
    )
)

_CATEGORY_PROMPTS: dict[str, str] = {
    "civil": (
        "당신은 민사법 전문 변호사입니다. 계약, 손해배상, 부동산, 채권·채무 등 "
        "민사 분야 질문에 답합니다. 필요하면 search_case_law 도구로 관련 판례를 검색하세요."
    ),
    "criminal": (
        "당신은 형사법 전문 변호사입니다. 사기, 폭행, 횡령 등 형사 사건 관련 "
        "질문에 답합니다. 필요하면 search_case_law 도구로 관련 판례를 검색하세요."
    ),
    "administrative": (
        "당신은 행정법 전문 변호사입니다. 행정처분, 허가, 세금 부과 등 행정 분야 "
        "질문에 답합니다. 필요하면 search_case_law 도구로 관련 판례를 검색하세요."
    ),
    "family": (
        "당신은 가사법 전문 변호사입니다. 이혼, 상속, 양육권 등 가사 분야 질문에 "
        "답합니다. 필요하면 search_case_law 도구로 관련 판례를 검색하세요."
    ),
}

# ---------------------------------------------------------------------------
# Node functions
# ---------------------------------------------------------------------------


def router_node(state: AgentState) -> dict:
    """Classify the latest user message into a law category."""
    messages = [_ROUTER_PROMPT] + list(state["messages"])
    response = _llm.invoke(messages)
    raw = response.content.strip().lower()

    valid: list[LawCategory] = ["civil", "criminal", "administrative", "family"]
    category: LawCategory = cast(LawCategory, raw) if raw in valid else "unknown"
    return {"category": category, "messages": [response]}


def _category_node(state: AgentState, category: str) -> dict:
    """Generic node for a specific law category."""
    system = SystemMessage(content=_CATEGORY_PROMPTS[category])
    messages = [system] + list(state["messages"])
    response = _llm_with_tools.invoke(messages)
    return {"messages": [response]}


def civil_node(state: AgentState) -> dict:
    return _category_node(state, "civil")


def criminal_node(state: AgentState) -> dict:
    return _category_node(state, "criminal")


def admin_node(state: AgentState) -> dict:
    return _category_node(state, "administrative")


def family_node(state: AgentState) -> dict:
    return _category_node(state, "family")


def unknown_node(state: AgentState) -> dict:
    """Fallback node for unclassified questions."""
    system = SystemMessage(
        content=(
            "당신은 법률 상담 도우미입니다. 질문이 민사/형사/행정/가사 중 어디에 "
            "해당하는지 명확하지 않습니다. 사용자에게 질문을 명확히 해달라고 안내하세요."
        )
    )
    messages = [system] + list(state["messages"])
    response = _llm.invoke(messages)
    return {"messages": [response]}
