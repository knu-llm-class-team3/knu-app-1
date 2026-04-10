from __future__ import annotations

import os
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
from langchain_openai import ChatOpenAI  # pyright: ignore[reportMissingImports]
from langchain_groq import ChatGroq  # pyright: ignore[reportMissingImports]

from vector_store import retrieve_relevant_docs
from classify_query_node import LegalSupportState

load_dotenv()


def _build_model():
    if os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(model="gpt-5-mini", temperature=0)
    return ChatGroq(model="openai/gpt-oss-20b", temperature=0)


model = _build_model()


def handle_administrative(state: LegalSupportState) -> LegalSupportState:
    print("🏛️ 행정 사건 문제를 처리합니다. 관련 판례를 검색 중입니다...")
    user_query = state.get("user_query", "")

    if not user_query:
        return {
            "answer": "[행정 노드] 질문이 비어 있어 분석을 진행할 수 없습니다.",
        }

    matched_docs = retrieve_relevant_docs(category="행정", query=user_query)
    print("🔍 검색된 판례 데이터를 기반으로 답변을 생성합니다.")

    prompt = f"""
    당신은 20년 경력의 행정 사건 전문 대표 변호사입니다.
    아래 의뢰인의 행정 분쟁 상황을 분석하고, 검색된 [유사 판례]를 엄격히 근거로 삼아 전문적인 법률 상담을 제공해 주세요.

    [의뢰인 질문]
    {user_query}

    [검색된 유사 판례 (답변의 핵심 근거)]
    {matched_docs}

    반드시 다음 내용을 포함하여 단계별로 답변하세요:

    - [공감과 상황 이해] 행정기관의 처분(과태료, 영업정지, 허가 취소 등)으로 인해 겪고 계신 불이익과 혼란에 공감합니다. 행정 절차는 일반인에게 복잡하고 어렵기 때문에 정확한 대응이 매우 중요함을 안내합니다.
    
    - [판례 기반 사안 분석] 제공된 [유사 판례]의 핵심 요지를 쉽게 설명하고, 해당 판례의 법리가 의뢰인의 상황(처분의 적법성, 재량권 일탈·남용 여부, 절차적 위법 여부 등)에 어떻게 적용되는지 객관적으로 분석합니다.
    
    - [대응 전략 및 행동 지침] 행정심판 또는 행정소송 가능 여부를 판단하고, 가장 현실적인 대응 전략을 제시합니다.
      (예: 행정심판 제기 가능성, 소 제기 기간(제소기간), 집행정지 신청 필요성, 증거자료 준비 방법 등)
    
    - [주의사항] 본 답변은 AI에 의한 참고용 법률 상담으로, 실제 행정심판 또는 행정소송 진행 시에는 반드시 변호사와 상담이 필요함을 명시합니다.

    어려운 법률 용어(행정처분, 재량권 일탈·남용, 집행정지, 제소기간 등)는 일반인이 이해하기 쉽게 풀어서 설명하고, 전체적인 어조는 신뢰감을 주면서도 차분하고 명확하게 작성하세요.
    """

    response = model.invoke(prompt).content

    return {
        "answer": response,
        "matched_docs": matched_docs,
    }