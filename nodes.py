"""
형사재판노드 (Criminal Trial Node)

형사재판 관련 사용자 질문을 처리하는 LangGraph 노드입니다.
관련 판례를 검색하고 LLM을 통해 법률 정보를 제공합니다.
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from state import AgentState
from tools import search_criminal_cases


SYSTEM_PROMPT = """당신은 형사재판 전문 법률 보조 AI입니다.
사용자의 형사 법률 질문에 대해 다음 원칙에 따라 답변하세요.

1. 검색된 관련 판례를 참고하여 답변합니다.
2. 형사소송법, 형법 등 관련 법령을 명시합니다.
3. 전문 용어는 쉽게 풀어서 설명합니다.
4. 법률 조언이 아닌 법률 정보 제공임을 명심하세요.
5. 필요시 변호사 상담을 권유합니다.
6. 답변은 반드시 한국어로 작성합니다.
"""


def format_cases(cases: list) -> str:
    """검색된 판례를 프롬프트에 삽입할 문자열로 변환합니다."""
    if not cases:
        return "관련 판례를 찾지 못했습니다."

    lines = []
    for i, case in enumerate(cases, 1):
        lines.append(
            f"[판례 {i}] {case['title']}\n"
            f"  - 요약: {case['summary']}\n"
            f"  - 적용 법령: {case['law']}\n"
            f"  - 판결: {case['verdict']} / {case['sentence']}"
        )
    return "\n\n".join(lines)


def criminal_trial_node(state: AgentState) -> AgentState:
    """
    형사재판노드: 형사 관련 법률 질문에 답변합니다.

    처리 흐름:
      1. 사용자 질문에서 관련 형사 판례 검색
      2. 판례와 함께 LLM에 답변 요청
      3. 결과를 state 에 저장하고 반환

    Args:
        state: 현재 LangGraph 에이전트 상태

    Returns:
        final_answer 및 retrieved_cases 가 업데이트된 상태
    """
    user_query = state.get("user_query", "")
    if not user_query and state.get("messages"):
        last_msg = state["messages"][-1]
        user_query = (
            last_msg.content if hasattr(last_msg, "content") else str(last_msg)
        )

    # 1. 판례 검색
    retrieved_cases = search_criminal_cases(user_query, top_k=3)
    cases_text = format_cases(retrieved_cases)

    # 2. LLM 호출
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    user_message = (
        f"[사용자 질문]\n{user_query}\n\n"
        f"[관련 판례]\n{cases_text}\n\n"
        "위 정보를 바탕으로 형사재판 관련 법률 정보를 제공해 주세요."
    )

    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ]
    )

    final_answer = response.content

    return {
        **state,
        "category": "형사",
        "retrieved_cases": retrieved_cases,
        "final_answer": final_answer,
        "messages": state.get("messages", []) + [response],
    }
