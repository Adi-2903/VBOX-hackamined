"""
Embedding Model Module
Wraps sentence-transformers for generating text embeddings and computing similarity.
Used for surprise/cliffhanger detection.
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore

# Lazy-load the model
_embedding_model = None


def _get_model():
    """Lazy initialization of the sentence-transformers model."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model


def generate_embedding(text: str) -> np.ndarray:
    """Generate an embedding vector for a text string."""
    model = _get_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding


def generate_embeddings(texts: list[str]) -> np.ndarray:
    """Generate embeddings for a list of texts. Returns a 2D numpy array."""
    model = _get_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings


def compute_cosine_similarity(embedding_a: np.ndarray, embedding_b: np.ndarray) -> float:
    """
    Compute cosine similarity between two embedding vectors.
    Returns a float between -1 and 1 (typically 0 to 1 for sentence embeddings).
    """
    # Reshape to 2D if needed
    a = embedding_a.reshape(1, -1)
    b = embedding_b.reshape(1, -1)
    similarity = cosine_similarity(a, b)[0][0]
    return float(round(similarity, 4))


def compute_surprise_score(context_text: str, ending_text: str) -> float:
    """
    Compute surprise score between context and ending of an episode.
    surprise = 1 - cosine_similarity(context_embedding, ending_embedding)

    Higher score means the ending is more unexpected relative to the context.
    Returns a float between 0 and 1.
    """
    context_emb = generate_embedding(context_text)
    ending_emb = generate_embedding(ending_text)
    similarity = compute_cosine_similarity(context_emb, ending_emb)
    surprise = max(0.0, min(1.0, 1.0 - similarity))  # clamp to [0, 1]
    return round(surprise, 4)


def get_embedding_model():
    """Get the embedding model instance"""
    return _get_model()


def compute_embeddings(texts: list[str], model=None) -> np.ndarray:
    """
    Compute embeddings for a list of texts.
    
    Args:
        texts: List of text strings
        model: Optional pre-loaded model (uses global if None)
        
    Returns:
        2D numpy array of embeddings
    """
    if model is None:
        model = _get_model()
    return model.encode(texts, convert_to_numpy=True)
