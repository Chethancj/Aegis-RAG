import importlib

try:
    SentenceTransformer = importlib.import_module("sentence_transformers").SentenceTransformer
except ModuleNotFoundError as exc:
    raise ImportError(
        "The sentence_transformers package is required to generate embeddings. "
        "Install it with `pip install sentence-transformers`."
    ) from exc

# instantiate the correct class from sentence_transformers
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str):
    """Generate embedding for a single piece of text and return as a list of floats."""
    return model.encode(text).tolist()