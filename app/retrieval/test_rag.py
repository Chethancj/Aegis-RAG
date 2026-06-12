# app/retrieval/test_rag.py

from app.llm.embeddings import generate_embedding
from app.vectorstore.qdrant_store import search
from app.llm.generate import generate_answer

question = "What is Aegis RAG?"

query_embedding = generate_embedding(question)

results = search(query_embedding)

context = "\n\n".join(
    result.payload["text"]
    for result in results
)

answer = generate_answer(question, context)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)