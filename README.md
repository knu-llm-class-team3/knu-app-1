## knu-app-1
# 프로젝트 개요 및 설명
```text
저희는 사용자의 현재 상황을 간략히 입력받아 이전 판례 데이터를 기반으로 맞춤형 법률 상담을 제공하는 AI 법률 어시스턴트 에이전트 서비스를 개발했습니다.

이 서비스는 LangGraph 기반 워크플로우를 활용해 사용자의 질문을 분석하고, 사건 유형에 따라 올바른 전문 노드(가정, 행정, 형사, 민사 담당 변호사)를 호출하여 결과물을 출력합니다.

동적 라우팅: classify_query 노드가 사용자의 상황을 분석하고, 4가지 전담 변호사 노드(형사, 민사, 행정, 가정/가사) 중 가장 적합한 노드를 선택해 호출합니다.

판례 기반 답변 (RAG): 선택된 변호사 노드는 FAISS 벡터 검색을 통해 사전에 저장된 판례 데이터에서 유사 판례를 찾고, 이를 근거로 신뢰성 있는 법률 상담 정보를 제공합니다.

결과물 이메일 전송: 최종적으로 생성된 법률 상담 정보는 사용자가 이메일로 편리하게 받아볼 수 있도록 구현되었습니다.

참고: 법원 판례 데이터는 시간 관계상 생성형 AI를 활용해 Mock Data(가짜 데이터)로 구축하였으며, Ollama의 nomic-embed-text-v2-moe 임베딩 모델을 통해 각 노드들이 벡터 DB에 접근할 수 있도록 연동했습니다.
```

###실행 방법
```bash
# 실행 전 Ollama 및 Nomic 임베딩 모델 다운로드
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull nomic-embed-text-v2-moe

# 가상환경 실행 후
pip install -r requirements.txt

# 의존성 설치 이후
python terminal_ui.py
```

# 프로젝트 기술 스택
```text
- Language: Python 3

- Framework: LangChain, LangGraph

- Frontend / UI: Streamlit

- LLM Model: OpenAI gpt-4o-mini 또는 Groq llama-3.1-8b-instant 등 (환경 변수에 따라 선택)

- Embedding Model: Ollama (nomic-embed-text-v2-moe) - Docker 기반 구동

- Vector Database: FAISS (faiss-cpu)

- Libraries: LangChain Community (CSVLoader, FAISS VectorStore), python-dotenv, Pydantic
```

# 프로젝트에서 잘한 점
```text
- LangGraph 기반의 멀티 에이전트 설계: 단일 LLM 프롬프트에 의존하지 않고 classify_query 노드를 통해 질문을 분류한 뒤, 각 분야 전담 변호사 노드로 라우팅하는 구조를 짜서 답변의 전문성과 확장성을 높였습니다.

- 로컬 임베딩 환경 구축: Docker와 Ollama를 활용하여 로컬 환경에서 비용 발생 없이 빠르고 안정적으로 텍스트 임베딩과 벡터 검색(RAG)이 가능하도록 파이프라인을 구축했습니다.

- 엔드투엔드(End-to-End) 서비스 흐름 구현: 웹에서 입력을 받고 도출된 법률 상담 결과를 사용자에게 이메일로 바로 전송하는 기능까지 연동하여 완벽한 서비스 형태의 프로토타입을 완성했습니다.
```

# 프로젝트에서 아쉬운 점 및 배운 점
```text
- Mock Data 사용의 한계: 실제 대한민국 법원 판례 데이터 수집에 시간이 부족하여 생성형 AI로 만든 가짜 판례 데이터를 활용한 점이 가장 아쉽습니다.

- 배운 점: RAG 기반 서비스에서 최종 답변의 퀄리티는 결국 '원본 데이터의 신뢰성과 질'에 직결된다는 것을 깊이 깨달았습니다. 정확한 법률 서비스를 위해서는 견고한 데이터 수집 및 전처리 파이프라인이 최우선임을 배웠습니다.

- 복합적 법률 문제 처리의 한계: 현실의 사건은 '형사 고소와 동시에 민사상 손해배상 청구'처럼 여러 분야가 섞여 있는 경우가 많으나, 현재 로직은 하나의 변호사 노드로만 라우팅됩니다.

- 배운 점: LangGraph의 흐름을 설계하면서 조건부 엣지(Conditional Edge)의 한계와, 여러 에이전트가 협력하여 정보를 종합하는 더 고차원적인 그래프 설계 기법에 대한 필요성을 체감했습니다.
```

# 프로젝트 고도화 계획
```text
- 실제 판례 데이터베이스 수집 및 연동: 대한민국 법원 종합법률정보 오픈 API를 연동하거나 웹 크롤러를 구축하여 실제 대법원 및 하급심 판례 데이터를 확보하고, 이를 바탕으로 FAISS 벡터 DB를 실무 수준으로 교체할 계획입니다.

- 다중 라우팅(Multi-Routing) 및 종합 노드 도입: 질문이 여러 카테고리에 해당할 경우, 관련 변호사 노드들을 동시에 호출하여 각각의 판례와 소견을 도출한 뒤, '수석 변호사(Supervisor) 노드'가 이를 하나의 깔끔한 상담 결과로 종합해 주는 아키텍처로 고도화하겠습니다.
```