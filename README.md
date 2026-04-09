# knu-app-1

**맞춤형 전담 변호사 에이전트** — KNU LLM Class Team 3

LangChain과 LangGraph를 활용한 법률 분야별 AI 변호사 에이전트입니다.

## 주요 기능

- **자동 카테고리 분류**: 사용자의 질문을 민사 / 형사 / 행정 / 가사 중 하나로 자동 분류합니다.
- **카테고리별 전문 노드**: 각 법률 분야 전담 LLM 노드가 질문에 답변합니다.
- **판례 검색 도구**: 모킹 판례 데이터에서 키워드 유사도 검색으로 관련 판례를 참조합니다.

## 프로젝트 구조

```
knu-app-1/
├── main.py            # CLI 진입점
├── graph.py           # LangGraph 에이전트 그래프
├── nodes.py           # 라우터 & 카테고리별 노드
├── tools.py           # 판례 검색 도구
├── state.py           # 공유 에이전트 상태
├── data/
│   └── case_law.json  # 모킹 판례 데이터
├── requirements.txt
└── .env.example
```

## 빠른 시작

1. 의존성 설치:

```bash
pip install -r requirements.txt
```

2. 환경 변수 설정:

```bash
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 입력
```

3. 실행:

```bash
python main.py
```

## 법률 카테고리

| 카테고리 | 영문 키 | 주요 분야 |
|----------|---------|---------|
| 민사 | civil | 계약, 손해배상, 채권·채무, 부동산 |
| 형사 | criminal | 사기, 폭행·상해, 횡령·배임 |
| 행정 | administrative | 행정처분, 허가·인허가, 세금 부과 |
| 가사 | family | 이혼, 상속, 친권·양육권 |
