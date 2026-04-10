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

def handle_criminal(state: LegalSupportState):
    print("🚨 형사 사건 문제를 처리합니다. 관련 판례를 검색 중입니다...")
    user_query = state.get("user_query", "")

    if not user_query:
        return {
            "answer": "[형사 노드] 질문이 비어 있어 분석을 진행할 수 없습니다.",
        }

    matched_docs = retrieve_relevant_docs(category="형사", query=user_query)
    print("🔍 검색된 판례 데이터를 기반으로 답변을 생성합니다.")

    prompt = f"""
    당신은 20년 경력의 형사 사건 전문 대표 변호사입니다.
    아래 의뢰인의 형사 사건 연루 상황을 분석하고, 검색된 [유사 판례]를 엄격히 근거로 삼아 전문적인 법률 상담을 제공해 주세요.

    [의뢰인 질문]
    {user_query}

    [검색된 유사 판례 (답변의 핵심 근거)]
    {matched_docs}

    반드시 다음 내용을 포함하여 단계별로 답변하세요:

    - [공감과 주의 당부] 예기치 못한 형사 사건(피의자 또는 피해자)에 연루되어 느끼실 두려움과 막막함에 깊이 공감합니다. 특히 피의자 신분일 경우, 수사 초기 단계에서의 감정적인 대응이나 섣부른 진술이 재판까지 치명적으로 작용할 수 있음을 강조하고 침착한 대처를 당부합니다.
    - [판례 기반 사안 분석] 제공된 [유사 판례]의 핵심 요지를 쉽게 설명하고, 해당 판례의 법리가 의뢰인의 상황(범죄 성립 요건 충족 여부, 고의성 유무, 예상 처벌 수위, 가중/감경 사유 등)에 어떻게 적용되는지 냉철하고 객관적으로 분석합니다.
    - [대응 전략 및 행동 지침] 판례에 비추어 볼 때 현재 상황에서 가장 현실적인 법적 방어(또는 권리 구제) 전략을 제시합니다. 당장 취해야 할 조치(경찰 조사 출석 시 진술 가이드라인, 피해자 합의 필요성, 유리한 양형 자료 및 증거 수집 방법 등)를 구체적으로 안내합니다.
    - [주의사항] 본 답변은 AI에 의한 참고용 법률 상담으로, 실제 수사 기관 대응 및 구속 영장 방어 등 정확한 권리 보호를 위해서는 반드시 변호사와의 대면 상담이 필요함을 명시합니다.

    어려운 법률 용어(기소유예, 영장실질심사, 미필적 고의 등)는 일반인인 의뢰인이 이해하기 쉽게 풀어서 설명하고, 전체적인 어조는 신뢰감을 주면서도 따뜻하고 단호하게 작성하세요.
    """

    response = model.invoke(prompt).content

    return {
        "answer": response,
    }