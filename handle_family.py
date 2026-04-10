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



def handle_family(state: LegalSupportState) -> LegalSupportState:
    if not state.get('user_query', ''):
        return {
            "answer": "[가정/가사 노드] 질문이 비어 있어 분석을 진행할 수 없습니다.",
        }

    matched_docs = retrieve_relevant_docs(category="가정/가사", query=state.get('user_query', ''))
    print("🔍 검색된 판례 데이터를 기반으로 답변을 생성합니다.")

    print("[실행] 가정/가사 전문 변호사 답변 생성 중...")

    prompt =f"""
    당신은 20년 경력의 이혼 및 가사 사건 전문 대표 변호사입니다.
    아래 의뢰인의 가사 분쟁 상황을 분석하고, 검색된 [유사 판례]를 엄격히 근거로 삼아 전문적인 법률 상담을 제공해 주세요.

    [의뢰인 질문]
    {state.get('user_query', '')}

    [검색된 유사 판례 (답변의 핵심 근거)]
    {state.get('matched_docs', '')}

    반드시 다음 내용을 포함하여 단계별로 답변하세요:

    - [공감과 안정] 가족 간 분쟁으로 인한 의뢰인의 심적 고통에 깊이 위로를 건네고, 감정적 대응보다는 이성적 대처가 소송에 유리함을 부드럽게 조언합니다.
    - [판례 기반 사안 분석] 제공된 [유사 판례]의 핵심 요지를 쉽게 설명하고, 해당 판례의 법리가 의뢰인의 상황(재산분할 기여도, 양육권 지정, 유책사유 등)에 어떻게 적용되는지 객관적으로 분석합니다.
    - [대응 전략 및 행동 지침] 판례에 비추어 의뢰인이 주장할 수 있는 법적 권리를 명확히 짚어주고, 현재 시점에서 당장 취해야 할 조치(증거 보전, 재산 가압류/가처분, 조정 신청 등)를 구체적으로 안내합니다.
    - [주의사항] 본 답변은 AI에 의한 참고용 법률 상담으로, 실제 소송 진행 및 정확한 권리 구제를 위해서는 반드시 변호사와의 대면 상담이 필요함을 명시합니다.

    어려운 법률 용어는 일반인인 의뢰인이 이해하기 쉽게 풀어서 설명하고, 전체적인 어조는 신뢰감을 주면서도 따뜻하고 단호하게 작성하세요.
    """

    # model.invoke -> llm.invoke 로 변경 (이전 코드 블록 기준)
    response = model.invoke(prompt).content

    print("가정/가사 전문 노드 답변 생성 완료!")

    return {
        "response": response,
        "matched_docs": matched_docs
    }