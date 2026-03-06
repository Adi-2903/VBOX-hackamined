"""
Emotion Model Module
Wraps HuggingFace emotion classification for per-sentence emotion detection.
Uses the j-hartmann/emotion-english-distilroberta-base model.
"""

from transformers import pipeline

# Lazy-load the model (loaded on first call)
_emotion_pipeline = None


def _get_pipeline():
    """Lazy initialization of the emotion classification pipeline."""
    global _emotion_pipeline
    if _emotion_pipeline is None:
        _emotion_pipeline = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=None,  # return all emotion scores
            truncation=True,
            max_length=512,
        )
    return _emotion_pipeline


def classify_emotion(text: str) -> dict:
    """
    Classify the dominant emotion in a text.

    Returns:
        {
            "dominant_emotion": str,    # e.g. "joy", "anger", "fear", "surprise", "sadness", "disgust", "neutral"
            "dominant_score": float,     # confidence of dominant emotion (0-1)
            "all_emotions": dict         # all emotion scores
        }
    """
    pipe = _get_pipeline()
    results = pipe(text[:512])[0]  # truncate to model max length

    # Convert list of dicts to a single dict
    all_emotions = {r["label"]: round(r["score"], 4) for r in results}

    # Find dominant emotion
    dominant = max(results, key=lambda x: x["score"])

    return {
        "dominant_emotion": dominant["label"],
        "dominant_score": round(dominant["score"], 4),
        "all_emotions": all_emotions,
    }


def classify_sentences(sentences: list[str]) -> list[dict]:
    """
    Run emotion classification on each sentence.

    Returns a list of emotion results, one per sentence.
    Each result contains dominant emotion, score, and all emotion probabilities.
    """
    pipe = _get_pipeline()
    results = []

    for sentence in sentences:
        if not sentence.strip():
            results.append({
                "dominant_emotion": "neutral",
                "dominant_score": 1.0,
                "all_emotions": {"neutral": 1.0},
            })
            continue

        raw = pipe(sentence[:512])[0]
        all_emotions = {r["label"]: round(r["score"], 4) for r in raw}
        dominant = max(raw, key=lambda x: x["score"])

        results.append({
            "dominant_emotion": dominant["label"],
            "dominant_score": round(dominant["score"], 4),
            "all_emotions": all_emotions,
        })

    return results


def get_emotion_intensities(sentence_emotions: list[dict]) -> list[float]:
    """
    Extract the dominant emotion intensity (score) from each sentence's emotion result.
    Used for computing emotion variance and emotion spikes.
    """
    return [e["dominant_score"] for e in sentence_emotions]
