from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """LangGraph 에이전트 공유 상태 정의"""
    messages: Annotated[list, add_messages]
    category: str          # 재판 카테고리: 형사, 민사, 가정, 행정
    user_query: str        # 사용자 원본 질문
    retrieved_cases: List[dict]  # 검색된 판례 목록
    final_answer: str      # 최종 응답
