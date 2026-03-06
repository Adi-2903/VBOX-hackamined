"""
Gen AI Pipeline
Specialized pipeline for Gen AI episode format with provided hooks and cliffhangers
"""

import numpy as np
from .input_adapter import parse_genai_episode, extract_hook_cliffhanger_features
from .text_processor import process_episode
from .emotion_model import classify_sentences, get_emotion_intensities
from .embedding_model import compute_surprise_score
from .retention_model_v3 import predict_retention_risk_v3 as predict_retention_risk


def analyze_genai_episode(episode_data: dict) -> dict:
    """
    Analyze episode in Gen AI format (with provided hook and cliffhanger).
    
    Args:
        episode_data: Dict with keys:
            - episode_number: int
            - title: str
            - hook: str (provided by Gen AI)
            - story: str (main content)
            - cliffhanger: str (provided by Gen AI)
            - text_overlays_suggestions: list[str]
    
    Returns:
        {
            "episode_number": int,
            "title": str,
            "hook_analysis": {
                "provided_hook": str,
                "hook_quality_score": float,
                "hook_features": dict,
            },
            "story_analysis": {
                "emotion_variance": float,
                "conflict_score": float,
                "pacing_score": float,
                "emotional_arc": list,
            },
            "cliffhanger_analysis": {
                "provided_cliffhanger": str,
                "cliffhanger_quality_score": float,
                "cliffhanger_features": dict,
            },
            "retention": {
                "risk_score": float,
                "risk_level": str,
                "reason": str,
            },
            "recommendations": list[str],
        }
    """
    # Parse Gen AI format
    parsed = parse_genai_episode(episode_data)
    
    # Extract hook/cliffhanger features
    hc_features = extract_hook_cliffhanger_features(parsed)
    
    # Process story text
    story_processed = process_episode(parsed["story_text"])
    story_sentences = story_processed["sentences"]
    
    # Analyze emotions in story
    story_emotions = classify_sentences(story_sentences)
    
    # Analyze hook separately
    hook_processed = process_episode(parsed["hook_text"])
    hook_emotions = classify_sentences(hook_processed["sentences"])
    
    # Analyze cliffhanger separately
    cliff_processed = process_episode(parsed["cliffhanger_text"])
    cliff_emotions = classify_sentences(cliff_processed["sentences"])
    
    # Compute emotion variance (story only)
    emotion_var = _compute_emotion_variance(story_emotions)
    
    # Compute conflict score (story only)
    conflict = _compute_conflict_score(story_sentences, story_emotions)
    
    # Compute pacing score (story only)
    pacing = _compute_pacing_score(story_processed)
    
    # Compute surprise score (story vs cliffhanger)
    surprise = compute_surprise_score(parsed["story_text"], parsed["cliffhanger_text"])
    
    # Analyze hook quality
    hook_quality = _analyze_hook_quality(parsed["hook_text"], hook_emotions, hc_features)
    
    # Analyze cliffhanger quality
    cliff_quality = _analyze_cliffhanger_quality(
        parsed["cliffhanger_text"], 
        cliff_emotions, 
        hc_features,
        surprise,
        conflict
    )
    
    # Compute retention risk
    retention = predict_retention_risk(
        hook_strength=hook_quality["score"],
        emotion_variance=emotion_var,
        conflict_score=conflict,
        pacing_score=pacing,
    )
    
    # Build emotional arc
    emotional_arc = [
        {
            "sentence_index": i,
            "text": story_sentences[i] if i < len(story_sentences) else "",
            "emotion": e["dominant_emotion"],
            "intensity": e["dominant_score"],
        }
        for i, e in enumerate(story_emotions)
    ]
    
    # Generate recommendations
    recommendations = _generate_recommendations(
        hook_quality["score"],
        emotion_var,
        conflict,
        pacing,
        cliff_quality["score"],
        retention["risk_level"]
    )
    
    return {
        "episode_number": parsed["metadata"]["episode_number"],
        "title": parsed["metadata"]["title"],
        "hook_analysis": {
            "provided_hook": parsed["hook_text"],
            "hook_quality_score": hook_quality["score"],
            "hook_features": hc_features,
            "hook_reason": hook_quality["reason"],
        },
        "story_analysis": {
            "emotion_variance": emotion_var,
            "conflict_score": conflict,
            "pacing_score": pacing,
            "emotional_arc": emotional_arc,
        },
        "cliffhanger_analysis": {
            "provided_cliffhanger": parsed["cliffhanger_text"],
            "cliffhanger_quality_score": cliff_quality["score"],
            "cliffhanger_features": hc_features,
            "cliffhanger_reason": cliff_quality["reason"],
            "surprise_score": surprise,
        },
        "retention": retention,
        "recommendations": recommendations,
    }


def analyze_genai_series(series_data: dict) -> dict:
    """
    Analyze full series in Gen AI format.
    
    Args:
        series_data: Dict with keys:
            - category: str
            - direction: str
            - hook: str (series-level hook)
            - episodes: list[dict]
    
    Returns:
        {
            "category": str,
            "direction": str,
            "series_hook": str,
            "episodes": list[dict],  # Per-episode analysis
            "series_insights": dict,
        }
    """
    episodes = series_data.get("episodes", [])
    episode_results = [analyze_genai_episode(ep) for ep in episodes]
    
    # Compute series-level metrics
    hook_scores = [r["hook_analysis"]["hook_quality_score"] for r in episode_results]
    cliff_scores = [r["cliffhanger_analysis"]["cliffhanger_quality_score"] for r in episode_results]
    retention_risks = [r["retention"]["risk_score"] for r in episode_results]
    
    avg_hook = round(float(np.mean(hook_scores)), 4) if hook_scores else 0
    avg_cliff = round(float(np.mean(cliff_scores)), 4) if cliff_scores else 0
    avg_risk = round(float(np.mean(retention_risks)), 4) if retention_risks else 0
    
    # Identify weakest/strongest episodes
    weakest_idx = int(np.argmax(retention_risks)) + 1
    strongest_idx = int(np.argmin(retention_risks)) + 1
    
    # Overall retention risk
    if avg_risk < 0.38:
        overall_risk = "LOW"
    elif avg_risk < 0.60:
        overall_risk = "MEDIUM"
    else:
        overall_risk = "HIGH"
    
    # Series recommendations
    series_recommendations = []
    if avg_hook < 0.6:
        series_recommendations.append("Strengthen hooks across episodes - add more curiosity triggers")
    if avg_cliff < 0.6:
        series_recommendations.append("Boost cliffhangers - leave more unresolved tension")
    if avg_risk > 0.5:
        series_recommendations.append("High retention risk - focus on conflict and pacing")
    
    # Check hook-to-cliffhanger continuity
    for i in range(len(episode_results) - 1):
        curr_cliff = cliff_scores[i]
        next_hook = hook_scores[i + 1]
        if curr_cliff < 0.5 and next_hook < 0.5:
            series_recommendations.append(
                f"Episode {i + 1} → {i + 2}: Weak transition - strengthen cliffhanger or next hook"
            )
    
    if not series_recommendations:
        series_recommendations.append("Series looks strong across all metrics!")
    
    return {
        "category": series_data.get("category", ""),
        "direction": series_data.get("direction", ""),
        "series_hook": series_data.get("hook", ""),
        "episodes": episode_results,
        "series_insights": {
            "avg_hook_quality": avg_hook,
            "avg_cliffhanger_quality": avg_cliff,
            "overall_retention_risk": overall_risk,
            "avg_retention_risk_score": avg_risk,
            "episode_count": len(episodes),
            "weakest_episode": weakest_idx,
            "strongest_episode": strongest_idx,
            "recommendations": series_recommendations,
        }
    }


# Helper functions

def _compute_emotion_variance(sentence_emotions: list[dict]) -> float:
    """Compute emotion variance across sentences."""
    if len(sentence_emotions) < 2:
        return 0.0
    
    intensities = get_emotion_intensities(sentence_emotions)
    variance = float(np.var(intensities))
    
    emotions = [e["dominant_emotion"] for e in sentence_emotions]
    transitions = sum(1 for i in range(1, len(emotions)) if emotions[i] != emotions[i - 1])
    transition_ratio = transitions / (len(emotions) - 1)
    
    scaled_variance = min(variance * 10, 1.0)
    score = 0.5 * scaled_variance + 0.5 * transition_ratio
    return round(min(max(score, 0.0), 1.0), 4)


def _compute_conflict_score(sentences: list[str], sentence_emotions: list[dict]) -> float:
    """Compute conflict score from sentences and emotions."""
    if not sentences:
        return 0.0
    
    full_text = " ".join(sentences).lower()
    
    # Conflict keywords
    conflict_keywords = {
        "but", "however", "problem", "danger", "wrong", "struggle", "fight",
        "crisis", "panic", "desperate", "worried", "trouble", "quit", "left",
        "miserable", "stressed", "doubt", "giving up", "low point", "rough",
    }
    
    conflict_hits = sum(1 for kw in conflict_keywords if kw in full_text)
    keyword_density = min(conflict_hits / max(len(sentences), 1), 1.0)
    
    # Polarity shifts
    positive_emotions = {"joy", "surprise"}
    negative_emotions = {"anger", "fear", "sadness", "disgust"}
    
    polarities = []
    for e in sentence_emotions:
        dom = e["dominant_emotion"]
        if dom in positive_emotions:
            polarities.append(1)
        elif dom in negative_emotions:
            polarities.append(-1)
        else:
            polarities.append(0)
    
    polarity_shifts = sum(
        1 for i in range(1, len(polarities))
        if polarities[i] != polarities[i - 1] and polarities[i] != 0 and polarities[i - 1] != 0
    )
    shift_ratio = polarity_shifts / max(len(polarities) - 1, 1)
    
    score = 0.5 * keyword_density + 0.5 * shift_ratio
    return round(min(max(score, 0.0), 1.0), 4)


def _compute_pacing_score(processed_text: dict) -> float:
    """Compute pacing score from processed text."""
    sentences = processed_text["sentences"]
    if not sentences:
        return 0.0
    
    avg_len = processed_text["avg_sentence_length"]
    
    if avg_len <= 8:
        length_score = 1.0
    elif avg_len <= 15:
        length_score = 1.0 - (avg_len - 8) / 14
    else:
        length_score = max(0.1, 1.0 - (avg_len - 8) / 14)
    
    verb_density = processed_text["action_verb_count"] / max(processed_text["word_count"], 1)
    verb_score = min(verb_density * 8, 1.0)
    
    dialogue_score = min(processed_text["dialogue_count"] / max(len(sentences), 1), 1.0)
    
    score = 0.4 * length_score + 0.4 * verb_score + 0.2 * dialogue_score
    return round(min(max(score, 0.0), 1.0), 4)


def _analyze_hook_quality(hook_text: str, hook_emotions: list[dict], features: dict) -> dict:
    """Analyze quality of provided hook."""
    if not hook_text:
        return {"score": 0.0, "reason": "No hook provided"}
    
    score = 0.5  # Base score
    reasons = []
    
    # Length check (ideal: 10-20 words)
    word_count = features["hook_word_count"]
    if 10 <= word_count <= 20:
        score += 0.2
        reasons.append("Good length")
    elif word_count < 10:
        score -= 0.1
        reasons.append("Too short")
    else:
        score -= 0.05
        reasons.append("Slightly long")
    
    # Question hook bonus
    if features["has_question_hook"]:
        score += 0.15
        reasons.append("Question hook")
    
    # Number hook bonus (specific details)
    if features["has_number_hook"]:
        score += 0.10
        reasons.append("Specific details")
    
    # Emotion check
    if hook_emotions and hook_emotions[0]["dominant_emotion"] != "neutral":
        if hook_emotions[0]["dominant_score"] > 0.60:
            score += 0.15
            reasons.append(f"Emotional ({hook_emotions[0]['dominant_emotion']})")
    
    # Curiosity keywords
    curiosity_words = ["quit", "happened", "secret", "truth", "never", "finally", "discovered"]
    if any(word in hook_text.lower() for word in curiosity_words):
        score += 0.10
        reasons.append("Curiosity trigger")
    
    score = round(min(max(score, 0.0), 1.0), 4)
    reason = "; ".join(reasons) if reasons else "Standard hook"
    
    return {"score": score, "reason": reason}


def _analyze_cliffhanger_quality(cliff_text: str, cliff_emotions: list[dict], 
                                  features: dict, surprise: float, conflict: float) -> dict:
    """Analyze quality of provided cliffhanger."""
    if not cliff_text:
        return {"score": 0.0, "reason": "No cliffhanger provided"}
    
    score = 0.4  # Base score
    reasons = []
    
    # Ellipsis bonus (creates suspense)
    if features["has_ellipsis_cliffhanger"]:
        score += 0.15
        reasons.append("Suspenseful ending")
    
    # Surprise score
    if surprise > 0.5:
        score += 0.20
        reasons.append("Strong twist")
    elif surprise > 0.3:
        score += 0.10
        reasons.append("Moderate surprise")
    
    # Conflict requirement
    if conflict < 0.15:
        score *= 0.7  # Penalty for low conflict
        reasons.append("Low conflict")
    elif conflict > 0.4:
        score += 0.10
        reasons.append("High tension")
    
    # Emotion check
    if cliff_emotions and cliff_emotions[-1]["dominant_emotion"] in ["fear", "surprise", "anger"]:
        if cliff_emotions[-1]["dominant_score"] > 0.60:
            score += 0.15
            reasons.append("Emotional ending")
    
    # Teaser words
    teaser_words = ["next", "wait", "spoiler", "stay tuned", "chapter", "happened", "can't believe"]
    if any(word in cliff_text.lower() for word in teaser_words):
        score += 0.10
        reasons.append("Teaser element")
    
    score = round(min(max(score, 0.0), 1.0), 4)
    reason = "; ".join(reasons) if reasons else "Standard cliffhanger"
    
    return {"score": score, "reason": reason}


def _generate_recommendations(hook_score: float, emotion_var: float, conflict: float,
                               pacing: float, cliff_score: float, risk_level: str) -> list[str]:
    """Generate actionable recommendations."""
    recommendations = []
    
    if hook_score < 0.5:
        recommendations.append("Strengthen hook: Add a question or specific number/detail")
    if emotion_var < 0.3:
        recommendations.append("Add emotional variety: Include more emotional transitions")
    if conflict < 0.3:
        recommendations.append("Increase conflict: Add more tension and obstacles")
    if pacing < 0.4:
        recommendations.append("Improve pacing: Use shorter sentences and more action verbs")
    if cliff_score < 0.5:
        recommendations.append("Boost cliffhanger: Add ellipsis or teaser for next episode")
    if risk_level == "HIGH":
        recommendations.append("High retention risk: Focus on hook and conflict")
    
    if not recommendations:
        recommendations.append("Episode looks strong! Keep up the good work.")
    
    return recommendations
