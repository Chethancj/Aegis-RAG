from qdrant_client import QdrantClient  # type: ignore[import]
from qdrant_client.models import Distance, VectorParams, PointStruct  # type: ignore[import]
import uuid

client = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "documents"


def create_collection():
    collections = client.get_collections()

    existing = [c.name for c in collections.collections]

    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )


def insert_chunks(chunks, embeddings):
    points = []

    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=uuid.uuid4(),
                vector=embedding,
                payload={
                    "text": chunk
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Inserted {len(points)} chunks")


def search(query_embedding, limit=3):
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit
    )

    return results.points