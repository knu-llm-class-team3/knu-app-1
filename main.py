"""Entry point for the lawyer agent CLI.

Usage:
    python main.py

Requires:
    OPENAI_API_KEY environment variable (set in .env or shell)
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

# Guard: ensure API key is available before importing graph/nodes
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError(
        "OPENAI_API_KEY is not set. "
        "Please copy .env.example to .env and fill in your API key."
    )

from graph import build_graph  # noqa: E402  (import after env check)


_BANNER = """
╔══════════════════════════════════════════════════╗
║       맞춤형 전담 변호사 에이전트 (v0.1)          ║
║  법률 카테고리: 민사 / 형사 / 행정 / 가사          ║
║  종료하려면  'exit' 또는 'quit' 을 입력하세요.     ║
╚══════════════════════════════════════════════════╝
"""


def main() -> None:
    print(_BANNER)
    app = build_graph()
    conversation: list = []

    while True:
        try:
            user_input = input("질문: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n종료합니다.")
            break

        if user_input.lower() in {"exit", "quit", "종료"}:
            print("종료합니다.")
            break

        if not user_input:
            continue

        conversation.append(HumanMessage(content=user_input))

        result = app.invoke({"messages": conversation})

        # Collect the last AI response
        ai_messages = [
            m for m in result["messages"] if hasattr(m, "content") and m.type == "ai"
        ]
        if ai_messages:
            answer = ai_messages[-1].content
            print(f"\n[{result.get('category', '?').upper()}] 변호사: {answer}\n")
            conversation = list(result["messages"])
        else:
            print("(응답 없음)\n")


if __name__ == "__main__":
    main()
