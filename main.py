"""
형사재판 법률 보조 CLI

형사재판노드를 통해 형사 법률 질문에 답변하는 CLI 도구입니다.

사용법:
    python main.py
    python main.py --query "음주운전 처벌 기준이 어떻게 되나요?"
"""

import argparse
import sys
from dotenv import load_dotenv

load_dotenv()

from graph import criminal_trial_graph  # noqa: E402  (load_dotenv 먼저 실행)


def run_query(query: str) -> None:
    """단일 질문을 형사재판 그래프에 전달하고 결과를 출력합니다."""
    print(f"\n[질문] {query}\n")
    print("=" * 60)

    result = criminal_trial_graph.invoke({"user_query": query, "messages": []})

    print("[형사재판 법률 정보]")
    print(result["final_answer"])

    if result.get("retrieved_cases"):
        print("\n[참고 판례]")
        for case in result["retrieved_cases"]:
            print(f"  • {case['title']} — {case['law']}")
    print("=" * 60)


def interactive_mode() -> None:
    """대화형 모드로 형사 법률 질문을 처리합니다."""
    print("형사재판 법률 보조 AI에 오신 것을 환영합니다.")
    print("형사 관련 법률 질문을 입력하세요. (종료: 'q' 또는 'quit')\n")

    while True:
        try:
            query = input("질문: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n종료합니다.")
            break

        if not query:
            continue
        if query.lower() in ("q", "quit", "exit"):
            print("종료합니다.")
            break

        run_query(query)


def main() -> None:
    parser = argparse.ArgumentParser(description="형사재판 법률 보조 AI")
    parser.add_argument(
        "--query", "-q", type=str, default=None, help="처리할 형사 법률 질문"
    )
    args = parser.parse_args()

    if args.query:
        run_query(args.query)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
