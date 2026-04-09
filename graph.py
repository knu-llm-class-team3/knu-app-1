"""
형사재판 LangGraph 그래프 정의

단일 형사재판노드로 구성된 간단한 그래프입니다.
전체 앱에서는 카테고리 라우터 노드와 함께 통합됩니다.
"""

from langgraph.graph import StateGraph, END

from state import AgentState
from nodes import criminal_trial_node


def build_criminal_trial_graph() -> StateGraph:
    """형사재판 처리 그래프를 빌드하여 반환합니다."""
    graph = StateGraph(AgentState)

    # 형사재판노드 등록
    graph.add_node("criminal_trial", criminal_trial_node)

    # 엔트리포인트 → 형사재판노드 → END
    graph.set_entry_point("criminal_trial")
    graph.add_edge("criminal_trial", END)

    return graph.compile()


# 그래프 인스턴스 (모듈 임포트 시 생성)
criminal_trial_graph = build_criminal_trial_graph()
