from sentence_transformers import SentenceTransformer
import numpy as np

_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text: str) -> np.ndarray:
    return _model.encode(text, normalize_embeddings=True)

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))
