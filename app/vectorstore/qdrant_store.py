from numpy import source
from qdrant_client import QdrantClient  # type: ignore[import]
from qdrant_client.models import Distance, VectorParams, PointStruct  # type: ignore[import]
import uuid
from qdrant_client.models import Filter, FieldCondition, MatchValue
import os

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")

client = QdrantClient(
    host=QDRANT_HOST,
    port=6333
)

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


def insert_chunks(
    chunks,
    embeddings,
    source
):
    points = []

    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "source": source
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Inserted {len(points)} chunks")


def search(
        query_embedding, 
        source=None,
        limit=3
    ):
    query_filter = None

    if source:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="source",
                    match=MatchValue(value=source)
                )
            ]
        )
    
    
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=query_filter,
        limit=limit
    )

    return results.points

def get_documents():

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True
    )

    documents = set()

    for point in points:

        source = point.payload.get("source")

        if source:
            documents.add(source)

    return sorted(list(documents))