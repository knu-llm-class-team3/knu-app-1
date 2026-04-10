import os
from langchain_community.vectorstores import FAISS
from langchain_core.documents.base import Document
from langchain_community.document_loaders import CSVLoader
from langchain_ollama import OllamaEmbeddings
from typing import List
from dotenv import load_dotenv


# csv 파일 로드
def _load_documents()->List[Document]:

    loader = CSVLoader(
        file_path="./lib/precedent.csv",
        encoding='utf-8',
        metadata_columns=['case_number', 'court', 'date'],
        content_columns=['case_type', 'case_name', 'result', 'summary', 'reasoning', 'keywords']
    )

    loaded_docs = loader.load()

    return loaded_docs

# 임베딩 모델 반환
def _get_embeddings():
    return OllamaEmbeddings(
        model="nomic-embed-text-v2-moe"
        
    )

# 임베딩된 벡터스토어 반환
def _embedding(docs: List[Document])->FAISS:
    embeddings = _get_embeddings()

    vector_store = FAISS.from_documents(
        documents = docs,
        embedding = embeddings
    )
    
    return vector_store

def _save_vector_to_local(vector_store: FAISS):
    vector_store.save_local("./exp-faiss")

# 벡터스토어 로드
def _load_vector_from_local() -> FAISS:
    load_dotenv()
    return FAISS.load_local("./exp-faiss", _get_embeddings(), allow_dangerous_deserialization=True)

# 벡터스토어 초기화
def _init_vector_store():
    docs = _load_documents()
    vector_store = _embedding(docs)
    _save_vector_to_local(vector_store)
    return vector_store

# 관련 문서 검색
def retrieve_relevant_docs(category: str ,query: str) -> str:
    if os.path.exists("./exp-faiss"):
        vector_store = _load_vector_from_local()
    else:
        vector_store = _init_vector_store()
        
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs = {
            "k": 3,          
            "fetch_k": 10,    
            "lambda_mult": 0.5
        }
    )

    retrieved_docs = retriever.invoke(f'법률 분야: {category} 질문: {query}')
    
    merged_docs = _merge_retrieved_docs(retrieved_docs)
    return merged_docs
    
    
    
def _merge_retrieved_docs(retrieved_dos: List[Document]) -> str:  
    merged_docs = "\n\n".join([doc.page_content for doc in retrieved_dos])
    return merged_docs

    
    