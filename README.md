## knu-app-1
# 프로젝트 개요 및 설명

실행 전 docker - ollama - nomic-embed-text-v2-moe 실행 필요

이 프로젝트는 사용자 법률 질문을 자동으로 분류하고, 관련 판례를 검색해 상담형 답변을 생성하는 AI 법률 어시스턴트 프로토타입입니다.  
LangGraph 기반 워크플로우로 질문을 형사, 민사, 행정, 가정/가사 분야로 라우팅하며, FAISS 벡터 검색을 통해 precedent 데이터에서 유사 판례를 찾아 답변 근거로 활용합니다.  
LLM은 환경 변수에 따라 OpenAI 또는 Groq 모델을 사용하고, 임베딩은 Ollama의 nomic-embed-text-v2-moe를 사용합니다.  
터미널 UI를 통해 질의, 샘플 실행, 결과 확인까지 한 번에 테스트할 수 있도록 구성되어 있습니다.

# 프로젝트 기술 스택
Python 3
LangChain
LangGraph
LangChain OpenAI
LangChain Groq
LangChain Community (CSVLoader, FAISS VectorStore)
LangChain Ollama (OllamaEmbeddings)
FAISS (faiss-cpu)
python-dotenv (dotenv)
Pydantic
Ollama 모델: nomic-embed-text-v2-moe
LLM 모델: OpenAI gpt-5-mini 또는 Groq openai/gpt-oss-20b
Docker 
# 프로젝트에서 잘한 점

# 프로젝트에서 아쉬운 점
--> 이로서 무엇을 배웠는지

# 프로젝트 고도화 계획
-> 아쉬운 부분을 어떤 식으로 개선할 수 있을지