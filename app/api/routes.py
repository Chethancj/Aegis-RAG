from multiprocessing import context

from app.ingestion.ingest import ingest_pdf
import os
from fastapi import APIRouter, UploadFile, File
router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    chunk_count = ingest_pdf(file_path)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "saved_to": file_path,
        "chunk_count": chunk_count
    }
from app.llm.embeddings import generate_embedding
from app.vectorstore.qdrant_store import search
from app.llm.generate import generate_answer
from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    source: str | None = None

@router.post("/ask")
async def ask(req: AskRequest):

    query_embedding = generate_embedding(req.question)
    results = search(query_embedding, source=req.source)

    context = "\n\n".join(
        result.payload["text"]
        for result in results
    )
    print("\n" + "="*50)
    print("QUESTION:", req.question)
    print("\nCONTEXT SENT TO OLLAMA:\n")
    print(context[:2000])
    print("="*50)
    
    answer = generate_answer(
        req.question,
        context
    )

    sources = list(
    set(
        result.payload.get("source", "unknown")
        for result in results
    )
    )

    return {
    "question": req.question,
    "answer": answer,
    "sources": sources
    }

@router.get("/documents")
async def get_all_documents():

    from app.vectorstore.qdrant_store import get_documents

    return {
        "documents": get_documents()
    }