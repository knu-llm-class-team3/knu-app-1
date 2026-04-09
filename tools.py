"""
형사재판 판례 유사도 검색 도구

사용자 질문과 관련된 형사 판례를 키워드 기반으로 검색합니다.
실제 서비스에서는 벡터 임베딩 기반 유사도 검색으로 대체할 수 있습니다.
"""

import json
import os
from typing import List

# 형사 판례 데이터 로드
_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "criminal_cases.json")


def load_criminal_cases() -> List[dict]:
    """형사 판례 데이터를 파일에서 불러옵니다."""
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def search_criminal_cases(query: str, top_k: int = 3) -> List[dict]:
    """
    키워드 기반으로 형사 판례를 검색합니다.

    Args:
        query: 사용자 질문 또는 검색어
        top_k: 반환할 최대 판례 수

    Returns:
        관련도 순으로 정렬된 판례 목록
    """
    cases = load_criminal_cases()
    query_lower = query.lower()

    scored = []
    for case in cases:
        score = 0
        # 키워드 매칭 (대소문자 구분 없이)
        matching_keywords = [kw for kw in case.get("keywords", []) if kw in query_lower]
        score += len(matching_keywords) * 3
        # 제목 완전 일치
        if case["title"].replace(" ", "") in query.replace(" ", ""):
            score += 5
        # 요약 내 단어 포함 여부
        if any(word in case["summary"] for word in query.split()):
            score += 1
        scored.append((score, case))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [case for score, case in scored[:top_k] if score > 0]
