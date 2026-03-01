import os
from typing import Any

from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter


def load_vectorstore(path: str) -> Any:
    if os.path.exists(path):
        # Required by newer LangChain/FAISS wrappers when loading local indexes.
        return FAISS.load_local(path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    return None


def ingest_text_file(filepath: str, index_path: str):
    loader = TextLoader(filepath, encoding='utf-8')
    docs = loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local(index_path)
    return vs


def query_vectorstore(vs: Any, query: str, k: int = 4) -> str:
    if vs is None:
        return "No index found. Run ingestion first."
    docs = vs.similarity_search(query, k=k)
    combined = "\n\n".join([d.page_content for d in docs])
    return combined or "No results found."
