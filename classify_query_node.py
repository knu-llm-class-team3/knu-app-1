from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal, TypedDict
from config import _build_model


# ── 분류 스키마 ───────────────────────────────────────────────────────────────
class QueryClassification(BaseModel):
    category: Literal["criminal", "civil", "administrative", "family"] = Field(
        description="분류된 카테고리"
    )
    reasoning: str = Field(description="해당 카테고리를 선택한 기술적 판단 근거")
    confidence: float = Field(description="분류의 신뢰도 0~1 사이의 값")

model = _build_model()

LegalCategory = Literal["criminal", "civil", "administrative", "family", "unknown"]

#-- State ─────────────────────────────────────────────────────────────────────
class LegalSupportState(TypedDict, total=False):
	user_query: str
	query_category: LegalCategory
	confidence: float
	reasoning: str
	answer: str
	matched_docs: str


#-- 노드 1: 질문 분류 ──────────────────────────────────────────────────────────
def classify_legal_query(state: LegalSupportState) -> LegalSupportState:
	"""사용자 질문을 형사/민사/행정/가정(가사)으로 분류하는 노드."""
	classifier = model.with_structured_output(QueryClassification)
	prompt = f"""
		너는 한국 최고의 변호사이다.
		아래 사용자 질문을 다음 4개 중 하나로만 분류해라:
		criminal: 형사
		- civil: 민사
		- administrative: 행정
		- family: 가정/가사

		사용자 질문:
		{state['user_query']}

		질문의 핵심 의도를 기준으로 가장 적합한 카테고리로 정확하게 분류하세요.
		"""
	result: QueryClassification = classifier.invoke(prompt)
	print(f"  → 카테고리: {result.category}  |  근거: {result.reasoning}")
	return {"query_category": result.category ,
			"confidence": result.confidence,
			"reasoning": result.reasoning}


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

