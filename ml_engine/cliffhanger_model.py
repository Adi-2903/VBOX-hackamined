"""
Cliffhanger Strength Scoring Engine
Computes how strong an episode's cliffhanger is using:
- Surprise score (semantic divergence of ending from context)
- Emotion spike (intensity spike in final sentences vs average)
- Conflict signal (presence of unresolved conflict)
- Keyword boosting (category-specific keywords enhance scores)

Score is scaled to 0-10.
"""

import numpy as np
from .emotion_model import get_emotion_intensities
from .keyword_detector import get_keyword_detector


def compute_emotion_spike(sentence_emotions: list[dict]) -> float:
    """
    Compute emotion spike: how much the final sentences spike above the episode average.
    Formula: max(last 3 sentence intensities) - mean(all intensities)

    Returns a float, typically 0 to ~0.5. Clamped to [0, 1].
    """
    intensities = get_emotion_intensities(sentence_emotions)
    if not intensities:
        return 0.0

    last_intensity = intensities[-1]
    
    if len(intensities) < 3:
        # For short text, the spike applies simply based on how intense the last sentence is
        spike = last_intensity * 0.5
    else:
        overall_mean = float(np.mean(intensities))
        last_three_max = float(max(intensities[-3:]))
        spike = last_three_max - overall_mean

    # Bonus if the very last sentence is intense
    if last_intensity > 0.7:
        spike += 0.15

    return round(max(0.0, min(spike, 1.0)), 4)


def compute_ending_conflict_signal(sentence_emotions: list[dict]) -> float:
    """
    Check if the ending contains unresolved conflict (negative emotions at the end).
    Returns 0 to 1.
    """
    if len(sentence_emotions) < 2:
        return 0.0

    # Look at last 20% of sentences
    split_idx = max(1, int(len(sentence_emotions) * 0.8))
    ending_emotions = sentence_emotions[split_idx:]

    conflict_emotions = {"anger", "fear", "sadness", "disgust", "surprise"}
    conflict_count = sum(
        1 for e in ending_emotions
        if e["dominant_emotion"] in conflict_emotions
    )

    signal = conflict_count / len(ending_emotions)
    return round(signal, 4)


def score_cliffhanger(
    surprise_score: float,
    sentence_emotions: list[dict],
    conflict_score: float,
    text: str = "",
    category: str = None,
) -> dict:
    """
    Compute the overall cliffhanger strength score with keyword boosting.

    Formula:
        raw = 0.5 * surprise + 0.3 * emotion_spike + 0.2 * conflict_signal
        keyword_boost = 1.0 to 1.3 based on category-specific keywords
        cliffhanger_score = raw * keyword_boost * 10  (scaled to 0-10)

    Args:
        surprise_score: Surprise score from feature extractor (0-1)
        sentence_emotions: Per-sentence emotion classification results
        conflict_score: Conflict score from feature extractor (0-1)
        text: Full episode text (optional, for keyword detection)
        category: Content category (optional, auto-detected if text provided)

    Returns:
        {
            "cliffhanger_score": float (0-10),
            "components": {
                "surprise": float,
                "emotion_spike": float,
                "conflict_signal": float,
                "keyword_boost": float (optional)
            },
            "category": str (optional),
            "keywords_found": list (optional),
            "reason": str
        }
    """
    # Compute components
    emotion_spike = compute_emotion_spike(sentence_emotions)
    conflict_signal = compute_ending_conflict_signal(sentence_emotions)

    # Weighted combination - adjusted weights
    raw = (0.50 * surprise_score) + (0.35 * emotion_spike) + (0.15 * conflict_signal)

    # Keyword boosting (if text provided)
    keyword_boost = 1.0
    keyword_info = {}
    
    if text:
        detector = get_keyword_detector()
        
        # Auto-detect category if not provided
        if category is None:
            category = detector.detect_category(text)
        
        # Get ending text (last 20%)
        sentences = text.split('.')
        split_idx = max(1, int(len(sentences) * 0.8))
        ending_text = '.'.join(sentences[split_idx:])
        
        # Detect keywords in ending
        hook_keywords = detector.detect_keywords(ending_text, category, "hook")
        conflict_keywords = detector.detect_keywords(ending_text, category, "conflict")
        resolution_keywords = detector.detect_keywords(ending_text, category, "resolution")
        
        # Massive Boost: Hook and conflict keywords boost score heavily
        # Resolution keywords reduce score
        keyword_boost = (
            1.0 +
            0.60 * hook_keywords["density"] +
            0.60 * conflict_keywords["density"] -
            0.30 * resolution_keywords["density"]
        )
        
        # Add massive structural hook if text ends in '...' or '?'
        if text.strip().endswith("...") or text.strip().endswith("?"):
            keyword_boost += 1.0 # guarantee a massive cliffhanger jump
            
        keyword_boost = max(0.9, min(keyword_boost, 2.5))  # Clamp to 0.9-2.5
        
        keyword_info = {
            "category": category,
            "keyword_boost": round(keyword_boost, 3),
            "keywords_found": {
                "hook": hook_keywords["keywords_found"],
                "conflict": conflict_keywords["keywords_found"],
                "resolution": resolution_keywords["keywords_found"]
            }
        }

    # Nonlinear scaling with more lenient thresholds
    if conflict_score < 0.10:
        # Moderate penalty for very low-conflict episodes
        adjusted_raw = raw ** 1.3
    elif raw > 0.45:
        # Cap exponential growth, switch to linear scaling towards 1.0
        adjusted_raw = raw ** 0.60
    else:
        adjusted_raw = raw ** 0.85

    # Apply keyword boost and stretch to 1-10 scale
    scaled_score = round(max(1.0, min(adjusted_raw * keyword_boost * 10, 10.0)), 2)

    # Build reason
    reasons = []
    if surprise_score > 0.5:
        reasons.append("Strong narrative twist in the ending")
    elif surprise_score > 0.25:
        reasons.append("Moderate surprise element")
    else:
        reasons.append("Predictable ending")

    if emotion_spike > 0.15:
        reasons.append("emotional intensity spikes at the end")
    else:
        reasons.append("flat emotional ending")

    if conflict_signal > 0.6:
        reasons.append("strong unresolved conflict creates tension")
    elif conflict_signal > 0.1:
        reasons.append("some tension in closing")
    
    # Add keyword-based reason
    if keyword_boost > 1.1:
        reasons.append(f"strong {keyword_info.get('category', 'category')} keywords enhance hook")
    elif keyword_boost < 0.95:
        reasons.append("resolution keywords weaken cliffhanger")

    # Strength label with adjusted thresholds
    if scaled_score >= 5.0:  # More lenient
        strength = "STRONG"
    elif scaled_score >= 2.5:  # More lenient
        strength = "MODERATE"
    else:
        strength = "WEAK"

    result = {
        "cliffhanger_score": float(scaled_score),
        "strength": strength,
        "components": {
            "surprise": round(surprise_score, 4),
            "emotion_spike": emotion_spike,
            "conflict_signal": conflict_signal,
        },
        "reason": "; ".join(reasons).capitalize(),
    }
    
    # Add keyword info if available
    if keyword_info:
        result["components"]["keyword_boost"] = keyword_info["keyword_boost"]
        result["category"] = keyword_info["category"]
        result["keywords_found"] = keyword_info["keywords_found"]
    
    return result
