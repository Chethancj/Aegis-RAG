from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import chunk_text

from app.llm.embeddings import generate_embedding

from app.vectorstore.qdrant_store import (
    create_collection,
    insert_chunks
)

text = load_pdf("docs/sample.pdf")

chunks = chunk_text(text)

embeddings = [
    generate_embedding(chunk)
    for chunk in chunks
]

create_collection()

insert_chunks(chunks, embeddings)

print("Finished")