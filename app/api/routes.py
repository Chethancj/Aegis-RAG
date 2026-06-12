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


@router.post("/ask")
async def ask(req: AskRequest):

    query_embedding = generate_embedding(req.question)

    results = search(query_embedding)

    context = "\n\n".join(
        result.payload["text"]
        for result in results
    )

    answer = generate_answer(
        req.question,
        context
    )

    return {
        "question": req.question,
        "answer": answer
    }