import os

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import chunk_pages


from app.llm.embeddings import generate_embedding

from app.vectorstore.qdrant_store import (
    create_collection,
    insert_chunks
)


def ingest_pdf(file_path: str):
    print(f"Processing: {file_path}")

    pages = load_pdf(file_path)
    chunks = chunk_pages(pages)

    total_chars = sum(
        len(page["text"])
        for page in pages
    )

    print(f"Characters: {total_chars}")

    print(f"Chunks: {len(chunks)}")

    embeddings = [
        generate_embedding(chunk["text"])
        for chunk in chunks
    ]

    create_collection()

    filename = os.path.basename(file_path)
    insert_chunks(
        chunks,
        embeddings,
        filename
    )

    print(f"Inserted {len(chunks)} chunks")

    return len(chunks)