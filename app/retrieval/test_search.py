from app.llm.embeddings import generate_embedding
from app.vectorstore.qdrant_store import search

query = "What is Aegis RAG?"

query_embedding = generate_embedding(query)

results = search(query_embedding)

for idx, result in enumerate(results):
    print(f"\nResult {idx+1}")
    print("Score:", result.score)
    print("Text:", result.payload["text"])