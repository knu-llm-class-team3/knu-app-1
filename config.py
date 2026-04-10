from langchain_ollama import OllamaEmbeddings  # pyright: ignore[reportMissingImports]
from langchain_openai import ChatOpenAI  # pyright: ignore[reportMissingImports]
from langchain_groq import ChatGroq  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
import os

# 임베딩 모델 반환
def _get_embeddings():
    load_dotenv()
    return OllamaEmbeddings(
        model="nomic-embed-text-v2-moe"
    )

def _build_model():
    load_dotenv()
    if os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(model="gpt-5-mini", temperature=0)
    return ChatGroq(model="openai/gpt-oss-20b", temperature=0)