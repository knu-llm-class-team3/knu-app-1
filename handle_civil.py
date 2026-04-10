from __future__ import annotations

import os
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
from vector_store import retrieve_relevant_docs
from classify_query_node import LegalSupportState
from config import _build_model

model = _build_model()

def handle_civil(state: LegalSupportState) -> LegalSupportState:

    print(" 민사 사건 문제를 처리합니다. 관련 판례를 검색 중입니다...")
    user_query = state.get("user_query", "")

    if not user_query:
        return {
            "answer": "[민사 노드] 질문이 비어 있어 분석을 진행할 수 없습니다.",
        }

    matched_docs = retrieve_relevant_docs(category="민사", query=user_query)
    print("🔍 검색된 판례 데이터를 기반으로 답변을 생성합니다.")

    prompt = f"""
        당신은 대한민국 최고의 민사법 전문 변호사입니다.
        사용자의 질문은 민사 사건과 관련된 내용입니다.
        당신이 참고해야 할 [관련 판례]가 아래에 제공되어 있습니다. 
        이 판례의 법리가 사용자의 상황에 어떻게 적용되는지, 혹은 적용되지 않는지 판단하여 논리적인 답변을 작성해 주세요.

        [검색된 유사 판례 (답변의 핵심 근거)]
        {matched_docs}
        [의뢰인 질문]
        {user_query}

        [답변 작성 지침]
        1. 핵심 요약: 질문에 대한 명확한 핵심 답변을 첫 문단에 짧게 제시하세요.
        2. 판례 적용 분석: 제공된 [관련 판례]를 인용하며, 해당 판례의 기준이 사용자의 사례에 충족되는지 판단 결과를 설명하세요.
        3. 대응 절차 (Action Item): 내용증명, 소송 등 향후 취할 수 있는 구체적 법적 절차를 안내해 주세요.
        4. 면책 조항: 마지막에 "본 답변은 참고용 법률 정보 제공을 목적으로 하며, 실제 법적 조치를 취할 때는 반드시 변호사와 상담하시기 바랍니다."라는 문구를 포함하세요.
        """

    result = model.invoke(prompt).content

    return {
        "answer": result,
        "matched_docs": matched_docs,
    }