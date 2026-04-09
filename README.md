# knu-app-1

법률 보조 AI — LangGraph 기반 재판 카테고리별 법률 정보 제공 앱

## 프로젝트 구조

```
knu-app-1/
├── main.py                 # CLI 진입점
├── graph.py                # LangGraph 그래프 정의
├── nodes.py                # 형사재판노드 (LangGraph 노드)
├── tools.py                # 판례 유사도 검색 도구
├── state.py                # 공유 에이전트 상태 정의
├── data/
│   └── criminal_cases.json # 형사 판례 모킹 데이터
├── requirements.txt
└── .env.example
```

## 형사재판노드 (Criminal Trial Node)

`nodes.py`의 `criminal_trial_node` 함수는 형사 법률 관련 사용자 질문을 처리합니다.

**처리 흐름:**
1. 사용자 질문으로 관련 형사 판례 검색 (`tools.py`)
2. 검색된 판례와 함께 LLM(GPT)에 답변 요청
3. 결과를 LangGraph 상태(`AgentState`)에 저장

## 시작하기

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. API 키 설정
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 입력

# 3. 실행
python main.py                                       # 대화형 모드
python main.py --query "음주운전 처벌 기준이 어떻게 되나요?"  # 단일 질문
```

## 지원 재판 카테고리

| 카테고리 | 설명 |
|----------|------|
| 형사재판 | 폭행, 절도, 사기, 명예훼손, 음주운전 등 |
| 민사재판 | (별도 노드에서 구현 예정) |
| 가정재판 | (별도 노드에서 구현 예정) |
| 행정재판 | (별도 노드에서 구현 예정) |