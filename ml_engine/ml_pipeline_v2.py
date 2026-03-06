"""
ML Pipeline V2 - Enhanced Analysis Pipeline
Integrates semantic analysis, emotional arc, narrative structure, dropoff prediction, and keyword detection.
"""

from .feature_extractor_v2 import extract_all_features_v2
from .retention_model_v3 import predict_retention_risk_v3
from .cliffhanger_model import score_cliffhanger
from .keyword_detector import get_keyword_detector_v2 as get_keyword_detector


def analyze_episode_v2(
    text: str, 
    category: str = None,
    hook: str = None,
    cliffhanger: str = None
) -> dict:
    """
    Enhanced ML analysis pipeline for a single episode with keyword detection.
    
    Args:
        text: Raw episode story text
        category: Optional content category (auto-detected if None)
        hook: Optional episode hook (if not provided, extracted from text)
        cliffhanger: Optional episode cliffhanger (if not provided, extracted from text)
        
    Returns:
        {
            "category": str,
            "features": {
                "semantic_features": {...},
                "emotional_arc": {...},
                "narrative_structure": {...},
                "dropoff_prediction": {...},
                "keyword_analysis": {...}
            },
            "retention": {
                "risk_score": float,
                "risk_level": str,
                "segment_risks": {...},
                "reason": str,
                "recommendations": [...]
            },
            "cliffhanger": {...},
            "summary": {
                "overall_score": float,
                "engagement_level": str,
                "key_strengths": [...],
                "key_weaknesses": [...]
            }
        }
    """
    # Step 1: Detect category
    detector = get_keyword_detector()
    if category is None:
        category = detector.detect_category(text)
    
    # Step 2: Extract all features (with optional hook/cliffhanger override)
    features = extract_all_features_v2(text, hook=hook, cliffhanger=cliffhanger)
    
    # Step 3: Keyword analysis
    keyword_analysis = detector.analyze_text(text, category)
    features["keyword_analysis"] = keyword_analysis
    
    # Step 4: Predict retention risk with category-specific weighting
    retention = predict_retention_risk_v3(features, category)
    
    # Step 5: Compute cliffhanger score with keyword boosting
    sentences = features["processed_text"].get("sentences", [])
    sentence_emotions = features["sentence_emotions"]
    surprise_score = features["semantic_features"].get("cliffhanger_score", 0.0)
    conflict_score = features["semantic_features"].get("conflict_score", 0.0)
    
    cliffhanger = score_cliffhanger(
        surprise_score,
        sentence_emotions,
        conflict_score,
        text=text,
        category=category
    )
    
    # Step 6: Generate summary
    summary = _generate_summary(features, retention, cliffhanger)
    
    # Step 7: Add keyword recommendations
    keyword_recs = detector.get_recommendations(keyword_analysis)
    if keyword_recs:
        formatted_recs = [
            {"area": "Keywords", "priority": "MEDIUM", "suggestion": rec} 
            for rec in keyword_recs
        ]
        retention["recommendations"].extend(formatted_recs)
    
    return {
        "category": category,
        "features": features,
        "retention": retention,
        "cliffhanger": cliffhanger,
        "summary": summary,
    }


def _generate_summary(features: dict, retention: dict, cliffhanger: dict) -> dict:
    """Generate overall episode summary"""
    semantic = features.get("semantic_features", {})
    emotional = features.get("emotional_arc", {})
    structure = features.get("narrative_structure", {})
    
    # Compute overall score (0-100)
    hook_score = semantic.get("hook_strength", 0.0)
    conflict_score = semantic.get("conflict_score", 0.0)
    
    # Use the new 1-10 arc_score instead of basic variance
    emotion_score = emotional.get("arc_score", 1.0) / 10.0 
    
    cliff_score = cliffhanger.get("cliffhanger_score", 0.0) / 10.0  # Normalize to 0-1
    structure_quality = structure.get("structure_quality", "POOR")
    
    # Weighted average with balanced formula
    overall_score = (
        0.25 * hook_score +
        0.20 * conflict_score +
        0.20 * emotion_score +
        0.25 * cliff_score +
        0.10 * _structure_quality_to_score(structure_quality)
    )
    
    # Apply very generous boost to make scores more optimistic
    # Most content should score 60-80, only truly bad content scores below 50
    overall_score = overall_score ** 0.65  # Much more generous boost (was 0.80)
    
    # Add a baseline boost - everyone starts at 20 points
    overall_score = 20 + (overall_score * 80)  # Scale to 20-100 range
    overall_score = round(overall_score, 1)
    
    # Engagement level with much more generous thresholds
    # Goal: Most episodes should be EXCELLENT or GOOD
    if overall_score >= 70:
        engagement_level = "EXCELLENT"
    elif overall_score >= 55:
        engagement_level = "GOOD"
    elif overall_score >= 40:
        engagement_level = "FAIR"
    else:
        engagement_level = "NEEDS WORK"
    
    # Key strengths with very generous thresholds
    # Goal: Find positives in most content
    key_strengths = []
    if hook_score >= 0.30:  # Lowered from 0.40
        key_strengths.append("Strong opening hook")
    if conflict_score >= 0.25:  # Lowered from 0.35
        key_strengths.append("Good conflict development")
    if emotion_score >= 0.10:  # Lowered from 0.15
        key_strengths.append("Dynamic emotional arc")
    if cliff_score >= 0.30:  # Lowered from 0.40
        key_strengths.append("Compelling cliffhanger")
    if structure_quality in ["EXCELLENT", "GOOD", "FAIR"]:
        key_strengths.append("Well-structured narrative")
    
    # Key weaknesses with strict thresholds (only flag serious issues)
    # Goal: Only 1-2 out of 6-7 episodes should have weaknesses flagged
    key_weaknesses = []
    if hook_score < 0.15:  # Very low threshold - only truly bad hooks
        key_weaknesses.append("Hook needs strengthening")
    if conflict_score < 0.15:  # Very low threshold
        key_weaknesses.append("Could use more conflict")
    if emotion_score < 0.05:  # Very low threshold
        key_weaknesses.append("Emotional arc could be more dynamic")
    if cliff_score < 0.15:  # Very low threshold
        key_weaknesses.append("Cliffhanger could be stronger")
    
    return {
        "overall_score": overall_score,
        "engagement_level": engagement_level,
        "key_strengths": key_strengths,
        "key_weaknesses": key_weaknesses,
    }


def _structure_quality_to_score(quality: str) -> float:
    """Convert structure quality to numeric score"""
    mapping = {
        "EXCELLENT": 1.0,
        "GOOD": 0.75,
        "FAIR": 0.50,
        "POOR": 0.25,
    }
    return mapping.get(quality, 0.25)


def analyze_series_v2(episodes: list[str]) -> dict:
    """
    Batch analysis of a full episodic series with enhanced insights.
    
    Args:
        episodes: List of episode texts
        
    Returns:
        {
            "episodes": list of individual episode analyses,
            "series_insights": {
                "avg_retention_risk": float,
                "avg_overall_score": float,
                "consistency_score": float,
                "trend": str,
                "recommendations": [...]
            }
        }
    """
    if not episodes:
        return {"episodes": [], "series_insights": {}}
    
    # Analyze each episode
    episode_analyses = []
    for i, episode_text in enumerate(episodes):
        analysis = analyze_episode_v2(episode_text)
        analysis["episode_number"] = i + 1
        episode_analyses.append(analysis)
    
    # Compute series-level insights
    series_insights = _compute_series_insights(episode_analyses)
    
    return {
        "episodes": episode_analyses,
        "series_insights": series_insights,
    }


def _compute_series_insights(episodes: list[dict]) -> dict:
    """Compute series-level insights"""
    if not episodes:
        return {}
    
    # Extract metrics
    retention_risks = [ep["retention"]["risk_score"] for ep in episodes]
    overall_scores = [ep["summary"]["overall_score"] for ep in episodes]
    
    avg_retention_risk = sum(retention_risks) / len(retention_risks)
    avg_overall_score = sum(overall_scores) / len(overall_scores)
    
    # Consistency score (lower variance = more consistent)
    import numpy as np
    score_variance = np.var(overall_scores)
    consistency_score = max(0, 100 - score_variance)
    
    # Trend analysis
    if len(episodes) >= 3:
        first_half_avg = sum(overall_scores[:len(episodes)//2]) / (len(episodes)//2)
        second_half_avg = sum(overall_scores[len(episodes)//2:]) / (len(episodes) - len(episodes)//2)
        
        if second_half_avg > first_half_avg + 5:
            trend = "IMPROVING"
        elif second_half_avg < first_half_avg - 5:
            trend = "DECLINING"
        else:
            trend = "STABLE"
    else:
        trend = "INSUFFICIENT_DATA"
    
    # Series-level recommendations
    recommendations = []
    
    if avg_retention_risk > 0.60:
        recommendations.append("High average retention risk - focus on stronger hooks and cliffhangers")
    
    if consistency_score < 70:
        recommendations.append("Inconsistent episode quality - aim for more uniform engagement levels")
    
    if trend == "DECLINING":
        recommendations.append("Quality declining over series - review later episodes for engagement issues")
    
    weak_episodes = [i+1 for i, ep in enumerate(episodes) if ep["summary"]["overall_score"] < 40]
    if weak_episodes:
        recommendations.append(f"Episodes {weak_episodes} need significant improvement")
    
    return {
        "avg_retention_risk": round(avg_retention_risk, 3),
        "avg_overall_score": round(avg_overall_score, 1),
        "consistency_score": round(consistency_score, 1),
        "trend": trend,
        "recommendations": recommendations,
    }
