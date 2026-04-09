from __future__ import annotations

from typing import Literal, TypedDict
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]


import importlib


def _get_chat_openai_class():
	"""langchain_openai가 설치된 경우 ChatOpenAI 클래스를 반환합니다."""
	try:
		lc_openai = importlib.import_module("langchain_openai")
		return getattr(lc_openai, "ChatOpenAI", None)
	except Exception:
		return None

load_dotenv()
ChatOpenAI = _get_chat_openai_class()


LegalCategory = Literal["criminal", "civil", "administrative", "family", "unknown"]


class LegalSupportState(TypedDict, total=False):
	user_query: str
	query_category: LegalCategory
	confidence: float
	reasoning: str


def _keyword_fallback_classification(query: str) -> tuple[LegalCategory, float, str]:
	"""LLM 사용이 어려울 때를 위한 간단한 키워드 분류기."""
	q = query.lower().strip()

	criminal_keywords = ["고소", "고발", "형사", "폭행", "사기", "절도", "기소", "처벌", "경찰"]
	civil_keywords = ["민사", "손해배상", "채무", "계약", "대여금", "임대차", "보증금", "소송"]
	administrative_keywords = ["행정", "처분", "과태료", "영업정지", "인허가", "취소소송", "행정심판"]
	family_keywords = ["가사", "가정", "이혼", "양육권", "친권", "재산분할", "상속"]

	scores = {
		"criminal": sum(1 for k in criminal_keywords if k in q),
		"civil": sum(1 for k in civil_keywords if k in q),
		"administrative": sum(1 for k in administrative_keywords if k in q),
		"family": sum(1 for k in family_keywords if k in q),
	}

	best_category = max(scores, key=scores.get)
	best_score = scores[best_category]

	if best_score == 0:
		return "unknown", 0.0, "매칭되는 키워드가 없어 unknown으로 분류했습니다."

	confidence = min(0.95, 0.5 + (best_score * 0.15))
	return (
		best_category,
		round(confidence, 2),
		f"키워드 매칭 기반 분류입니다. score={best_score}, details={scores}",
	)


def classify_legal_query(state: LegalSupportState) -> LegalSupportState:
	"""사용자 질문을 형사/민사/행정/가정(가사)으로 분류하는 노드."""
	query = state.get("user_query", "").strip()

	if not query:
		return {
			"query_category": "unknown",
			"confidence": 0.0,
			"reasoning": "입력 질문이 비어 있습니다.",
		}

	if ChatOpenAI is None:
		category, confidence, reasoning = _keyword_fallback_classification(query)
		return {
			"query_category": category,
			"confidence": confidence,
			"reasoning": reasoning,
		}

	try:
		llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
		prompt = f"""
너는 법률 질의 분류기다.
아래 사용자 질문을 다음 5개 중 하나로만 분류해라:
- criminal: 형사
- civil: 민사
- administrative: 행정
- family: 가정/가사
- unknown: 불명확

출력 형식:
category|confidence|reasoning

confidence는 0~1 숫자.

질문: {query}
"""
		raw = llm.invoke(prompt).content.strip()

		parts = [p.strip() for p in raw.split("|", maxsplit=2)]
		if len(parts) == 3:
			category_raw, confidence_raw, reasoning = parts
			category = category_raw.lower()
			if category not in {"criminal", "civil", "administrative", "family", "unknown"}:
				category = "unknown"
			try:
				confidence = float(confidence_raw)
			except ValueError:
				confidence = 0.6
			confidence = max(0.0, min(1.0, confidence))

			return {
				"query_category": category,  # type: ignore[typeddict-item]
				"confidence": round(confidence, 2),
				"reasoning": reasoning,
			}
	except Exception:
		pass

	category, confidence, reasoning = _keyword_fallback_classification(query)
	return {
		"query_category": category,
		"confidence": confidence,
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

