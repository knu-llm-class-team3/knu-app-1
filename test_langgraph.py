
from __future__ import annotations
from pprint import pprint
from langgraph.graph import END, START, StateGraph
from classify_query_node import LegalSupportState, classify_legal_query, route_by_legal_category
from handle_criminal import handle_criminal
from handle_administrative import handle_administrative


def criminal_node(state: LegalSupportState) -> LegalSupportState:
    result = handle_criminal(state)
    return {
        "answer": result.get("answer", "[형사 노드] 답변 생성에 실패했습니다."),
        "matched_docs": result.get("matched_docs", ""),
    }


def civil_node(state: LegalSupportState) -> LegalSupportState:
    return {
        "answer": f"[민사 노드] 질문 접수: {state.get('user_query', '')}",
    }


def administrative_node(state: LegalSupportState) -> LegalSupportState:
    return {
        "answer": f"[행정 노드] 질문 접수: {state.get('user_query', '')}",
    }


def family_node(state: LegalSupportState) -> LegalSupportState:
    return {
        "answer": f"[가정/가사 노드] 질문 접수: {state.get('user_query', '')}",
    }


def unknown_node(state: LegalSupportState) -> LegalSupportState:
    return {
        "answer": "[unknown 노드] 질문을 분류하지 못했습니다. 질문을 더 구체적으로 입력해 주세요.",
    }


def build_graph():
    builder = StateGraph(LegalSupportState)

    builder.add_node("classify", classify_legal_query)
    builder.add_node("criminal_node", criminal_node)
    builder.add_node("civil_node", civil_node)
    builder.add_node("administrative_node", administrative_node)
    builder.add_node("family_node", family_node)
    builder.add_node("unknown_node", unknown_node)

    builder.add_edge(START, "classify")
    builder.add_conditional_edges(
        "classify",
        route_by_legal_category,
        {
            "criminal_node": "criminal_node",
            "civil_node": "civil_node",
            "administrative_node": "administrative_node",
            "family_node": "family_node",
            "unknown_node": "unknown_node",
        },
    )

    builder.add_edge("criminal_node", END)
    builder.add_edge("civil_node", END)
    builder.add_edge("administrative_node", END)
    builder.add_edge("family_node", END)
    builder.add_edge("unknown_node", END)

    return builder.compile()


def run_test(query: str) -> LegalSupportState:
    graph = build_graph()
    return graph.invoke({"user_query": query})


if __name__ == "__main__":
    samples = [
        "사기로 돈을 빌려주고 못 받았는데 고소 가능한가요?",
        # "전세 보증금 반환 소송을 하려면 절차가 어떻게 되나요?",
        # "영업정지 처분 취소소송 가능한가요?",
        # "이혼 후 양육권과 친권은 어떻게 정해지나요?",
        # "법률 상담 받고 싶어요",
    ]

    for idx, query in enumerate(samples, start=1):
        result = run_test(query)
        print(f"\n[{idx}] 질문: {query}")
        print(f"state keys: {list(result.keys())}")
        print("state dump:")
        print(result)
        print(f"분류: {result.get('query_category')}")
        print(f"신뢰도: {result.get('confidence')}")
        print(f"근거: {result.get('reasoning')}")
        print(f"검색 판례: {result.get('matched_docs')}")
        print(f"응답: {result.get('answer')}")
