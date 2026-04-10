from __future__ import annotations

import os
from typing import Literal, TypedDict
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
from langchain_openai import ChatOpenAI  # pyright: ignore[reportMissingImports]
from langchain_groq import ChatGroq  # pyright: ignore[reportMissingImports]

load_dotenv()


def _build_llm():
	if os.getenv("OPENAI_API_KEY"):
		return ChatOpenAI(model="gpt-5-mini", temperature=0)
	return ChatGroq(model="openai/gpt-oss-20b", temperature=0)


llm = _build_llm()

LegalCategory = Literal["criminal", "civil", "administrative", "family", "unknown"]


class LegalSupportState(TypedDict, total=False):
	user_query: str
	query_category: LegalCategory
	confidence: float
	reasoning: str
	answer: str




def classify_legal_query(state: LegalSupportState) -> LegalSupportState:
	"""사용자 질문을 형사/민사/행정/가정(가사)으로 분류하는 노드."""
	query = state.get("user_query", "").strip()

	if not query:
		return {
			"query_category": "unknown",
			"confidence": 0.0,
			"reasoning": "입력 질문이 비어 있습니다.",
		}

	prompt = f"""
            너는 한국 최고의 변호사이다.
            아래 사용자 질문을 다음 4개 중 하나로만 분류해라:
            - criminal: 형사
            - civil: 민사
            - administrative: 행정
            - family: 가정/가사


            출력 형식:
            category|confidence|reasoning

            confidence는 0~1 숫자.

            질문: {query}
        """
	raw = llm.invoke(prompt).content.strip()

	parts = [p.strip() for p in raw.split("|", maxsplit=2)]
	if len(parts) != 3:
		return {
			"query_category": "unknown",
			"confidence": 0.0,
			"reasoning": "출력 형식이 올바르지 않습니다. expected: category|confidence|reasoning",
		}

	category_raw, confidence_raw, reasoning = parts
	category = category_raw.lower()
	if category not in {"criminal", "civil", "administrative", "family"}:
		category = "unknown"

	confidence = float(confidence_raw)
	confidence = max(0.0, min(1.0, confidence))

	return {
		"query_category": category,
		"confidence": round(confidence, 2),
		"reasoning": reasoning,
	}


def route_by_legal_category(state: LegalSupportState) -> str:
	"""LangGraph conditional edge에서 사용할 라우팅 함수."""
	category = state.get("query_category", "unknown")

	route_map = {
		"criminal": "criminal_node",
		"civil": "civil_node",
		"administrative": "administrative_node",
		"family": "family_node",
		"unknown": "unknown_node",
	}
	return route_map.get(category, "unknown_node")

