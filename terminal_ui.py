from __future__ import annotations

import time

from test_langgraph import build_graph

# 1. 새로 작성한 이메일 발송 함수 임포트
from email_utils import send_legal_consultation_email

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

# 2. 일반 실행과 샘플 실행을 구분하기 위해 prompt_email 인자 추가
def run_once(graph, query: str, prompt_email: bool = True) -> None:
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

    # 3. 터미널 출력이 끝난 후 이메일 전송 여부 확인 로직
    if prompt_email:
        while True:
            send_mail = input("📧 이 상담 결과를 이메일로 받아보시겠습니까? (y/n): ").strip().lower()
            
            if send_mail == 'y':
                to_email = input("받으실 이메일 주소를 입력하세요: ").strip()
                
                # 이메일 제목 생성을 위해 질문의 앞부분만 자르기
                topic_preview = query[:15] + "..." if len(query) > 15 else query
                
                # 이메일 본문에 들어갈 내용을 보기 좋게 HTML 태그와 함께 구성
                # (email_utils.py에서 \n을 <br>로 바꿔주지만, 여기서 미리 구조를 잡아줍니다)
                report_content = f"""
                <strong>[사용자 질문]</strong><br>{query}<br><br>
                <strong>[분야 분류]</strong> {result.get('query_category')} (신뢰도: {result.get('confidence')})<br>
                <strong>[분류 근거]</strong><br>{result.get('reasoning')}<br><br>
                <strong>[관련 판례]</strong><br>{result.get('matched_docs')}<br><br>
                <strong>[AI 상세 응답]</strong><br>{result.get('answer')}
                """
                
                print("\n이메일을 전송하는 중입니다. 잠시만 기다려주세요...")
                
                email_result = send_legal_consultation_email(
                    to_email=to_email,
                    consultation_topic=topic_preview,
                    report_content=report_content
                )
                
                if email_result["success"]:
                    print(f"✅ {email_result['message']}")
                else:
                    print(f"❌ 전송 실패: {email_result['error']}")
                break
                
            elif send_mail == 'n':
                break
            else:
                print("올바른 입력이 아닙니다. 'y' 또는 'n'을 입력해주세요.")


def run_samples(graph) -> None:
    samples = [
        "사기로 돈을 빌려주고 못 받았는데 고소 가능한가요?",
        "전세 보증금 반환 소송을 하려면 절차가 어떻게 되나요?",
        "영업정지 처분 취소소송 가능한가요?",
        "이혼 후 양육권과 친권은 어떻게 정해지나요?",
        "법률 상담 받고 싶어요",
    ]
    for q in samples:
        # 샘플 실행 중에는 이메일 전송을 묻지 않도록 False 처리
        run_once(graph, q, prompt_email=False)


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

        # 일반 질문 실행 (기본적으로 prompt_email=True가 적용됨)
        run_once(graph, user_input)


if __name__ == "__main__":
    main()