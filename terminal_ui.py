from __future__ import annotations

import time

from test_langgraph import build_graph


def print_header() -> None:
    print("=" * 68)
    print(" 법률 상담 분류 터미널 UI 프로토타입 ")
    print("=" * 68)
    print("명령어: /help, /samples, /exit")
    print("-" * 68)


def print_help() -> None:
    print("사용 방법")
    print("1) 질문을 입력하면 분야 분류 + 응답을 표시합니다.")
    print("2) /samples 입력 시 샘플 질문 5개를 순서대로 실행합니다.")
    print("3) /exit 입력 시 종료합니다.")


def run_once(graph, query: str) -> None:
    t0 = time.perf_counter()
    result = graph.invoke({"user_query": query})
    dt = (time.perf_counter() - t0) * 1000

    print()
    print("질문:")
    print(query)
    print("====")
    print("분류:")
    print(result.get("query_category"))
    print("====")
    print("신뢰도:")
    print(result.get("confidence"))
    print("====")
    print("근거:")
    print(result.get("reasoning"))
    print("====")
    print("검색 판례:")
    print(result.get("matched_docs"))
    print("====")
    print("응답:")
    print(result.get("answer"))
    print("====")
    print(f"처리시간: {dt:.1f}ms")
    print("=" * 68)


def run_samples(graph) -> None:
    samples = [
        "사기로 돈을 빌려주고 못 받았는데 고소 가능한가요?",
        "전세 보증금 반환 소송을 하려면 절차가 어떻게 되나요?",
        "영업정지 처분 취소소송 가능한가요?",
        "이혼 후 양육권과 친권은 어떻게 정해지나요?",
        "법률 상담 받고 싶어요",
    ]
    for q in samples:
        run_once(graph, q)


def main() -> None:
    graph = build_graph()
    print_header()

    while True:
        try:
            user_input = input("질문 입력 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n종료합니다.")
            break

        if not user_input:
            print("질문이 비어 있습니다. 다시 입력해 주세요.")
            continue

        if user_input == "/exit":
            print("종료합니다.")
            break
        if user_input == "/help":
            print_help()
            continue
        if user_input == "/samples":
            run_samples(graph)
            continue

        run_once(graph, user_input)


if __name__ == "__main__":
    main()
