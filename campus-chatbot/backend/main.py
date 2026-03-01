from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from backend.ingest import load_vectorstore
from backend.llm import answer_from_context
from backend.db import list_otherwebsites, replace_otherwebsites, create_tables

app = FastAPI(title="Campus Chatbot API")

# Allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    q: str


class WebsiteItem(BaseModel):
    name: str
    site_url: str

INDEX_PATH = os.getenv("VECTORSTORE_PATH", "faiss_index")

@app.get("/")
async def root():
    return {"message": "Campus Chatbot API", "status": "running"}

@app.post("/api/query")
async def query(req: QueryRequest):
    if not req.q.strip():
        raise HTTPException(status_code=400, detail="Empty query")
    
    vs = load_vectorstore(INDEX_PATH)
    if vs is None:
        return {"answer": "I haven't been trained on any campus information yet. Please run the ingestion script first to add documents."}
    
    # Get relevant documents
    docs = vs.similarity_search(req.q, k=4)
    if not docs:
        return {"answer": "I couldn't find any relevant information about that. Try asking something else!"}
    
    context = "\n\n".join([d.page_content for d in docs])
    answer = answer_from_context(context, req.q)
    
    return {"answer": answer}

@app.get("/health")
async def health():
    return {"status": "ok", "vectorstore_exists": os.path.exists(INDEX_PATH)}


@app.get("/api/otherwebsites")
async def get_otherwebsites():
    try:
        create_tables()
        rows = list_otherwebsites()
        return {"items": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch other websites: {e}")


@app.post("/api/otherwebsites/seed")
async def seed_otherwebsites(items: list[WebsiteItem]):
    try:
        create_tables()
        replace_otherwebsites([{"name": i.name, "site_url": i.site_url} for i in items])
        return {"ok": True, "count": len(items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to seed other websites: {e}")
