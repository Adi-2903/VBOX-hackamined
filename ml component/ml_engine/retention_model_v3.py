"""
Retention Risk Predictor V3 - Enhanced with New Features
Uses semantic features, emotional arc, and narrative structure.
"""


def predict_retention_risk_v3(features: dict, category: str = "general") -> dict:
    """
    Predict retention risk using enhanced feature set with category-specific weighting.
    
    Args:
        features: Dictionary containing:
            - semantic_features
            - emotional_arc
            - narrative_structure
            - dropoff_prediction
            - keyword_analysis (optional)
        category: Content category for category-specific weighting
            
    Returns:
        {
            "risk_score": float (0-1),
            "risk_level": str (LOW/MEDIUM/HIGH),
            "segment_risks": dict,
            "reason": str,
            "recommendations": list
        }
    """
    semantic = features.get("semantic_features", {})
    emotional = features.get("emotional_arc", {})
    structure = features.get("narrative_structure", {})
    dropoff = features.get("dropoff_prediction", {})
    
    # Store category in features for later use
    features["category"] = category
    
    # Extract key metrics
    hook_strength = semantic.get("hook_strength", 0.0)
    conflict_score = semantic.get("conflict_score", 0.0)
    cliffhanger_score = semantic.get("cliffhanger_score", 0.0)
    
    emotion_variance = emotional.get("emotion_variance", 0.0)
    emotion_peak = emotional.get("emotion_peak", 0.0)
    climax_position = emotional.get("climax_position", 0.5)
    
    conflict_density = structure.get("conflict_density", 0.0)
    twist_position = structure.get("twist_position_score", 0.0)
    resolution_absence = structure.get("resolution_absence_score", 0.0)
    
    overall_dropoff_risk = dropoff.get("overall_dropoff_risk", 0.5)
    
    # Compute retention risk using linear weighted combination instead of exponential
    # Lower values = better retention (lower risk)
    
    # Hook risk (critical - first 10 seconds)
    hook_risk = 1.0 - hook_strength
    
    # Conflict risk (important for middle section)
    conflict_risk = 1.0 - conflict_score
    
    # Emotional engagement risk
    # since emotion variance is heavily suppressed for short text, we cap its impact linearly
    emotion_risk = max(0.0, 1.0 - (emotion_variance * 5.0))
    
    # Cliffhanger risk (critical for retention)
    # The cliff score comes in as 0-10 from the main pipeline but 0-1 from semantic.
    # We'll normalize cliffhanger (if >1, then it's 0-10 scale)
    if cliffhanger_score > 1.0:
        norm_cliff = cliffhanger_score / 10.0
    else:
        norm_cliff = cliffhanger_score
        
    cliffhanger_risk = 1.0 - norm_cliff
    
    # Structure risk
    structure_risk = (1.0 - conflict_density) * 0.5 + (1.0 - twist_position) * 0.3 + (1.0 - resolution_absence) * 0.2
    
    # Extract linguistic bias features
    linguistic = features.get("linguistic_bias", {})
    reading_ease = linguistic.get("reading_ease", 100.0)
    repetition_count = linguistic.get("repetition_count", 0)

    # Apply keyword boost/penalty
    keyword_analysis = features.get("keyword_analysis", {})
    keyword_strength = keyword_analysis.get("overall_keyword_strength", 0.0)
    
    # Strong keywords reduce risk, weak keywords increase risk
    keyword_adjustment = (0.5 - keyword_strength) * 0.15  # -7.5% to +7.5%
    
    # Weighted combination with category-specific adjustments
    category = features.get("category", "general")
    
    # Category-specific weights (some categories need stronger hooks, others need more conflict)
    if category in ["finance", "entrepreneurship"]:
        # Finance/business needs strong hooks and cliffhangers
        risk = (
            0.35 * hook_risk +
            0.15 * conflict_risk +
            0.10 * emotion_risk +
            0.30 * cliffhanger_risk +
            0.10 * structure_risk
        )
    elif category in ["career", "self_improvement"]:
        # Personal stories need emotional arc and conflict
        risk = (
            0.25 * hook_risk +
            0.25 * conflict_risk +
            0.15 * emotion_risk +
            0.25 * cliffhanger_risk +
            0.10 * structure_risk
        )
    elif category in ["health", "productivity"]:
        # How-to content needs structure and clear progression
        risk = (
            0.30 * hook_risk +
            0.20 * conflict_risk +
            0.10 * emotion_risk +
            0.20 * cliffhanger_risk +
            0.20 * structure_risk
        )
    else:
        # Default weights
        risk = (
            0.30 * hook_risk +
            0.20 * conflict_risk +
            0.10 * emotion_risk +
            0.25 * cliffhanger_risk +
            0.15 * structure_risk
        )
    
    # Apply keyword adjustment
    risk += keyword_adjustment
    
    # Cross-validation: Check for inconsistencies between features
    # If hook is strong but cliffhanger is weak, that's suspicious
    if hook_strength > 0.6 and cliffhanger_score < 0.3:
        risk += 0.05  # Penalty for inconsistency
    
    # If conflict is high but emotion is flat, that's suspicious
    if conflict_score > 0.6 and emotion_variance < 0.08:
        risk += 0.05  # Penalty for inconsistency
    
    # If keywords are strong but semantic features are weak, boost semantic slightly
    if keyword_strength > 0.4 and (hook_strength < 0.3 or conflict_score < 0.3):
        risk -= 0.03  # Small boost for keyword presence
    
    # ---------------------------------------------------------
    # APPLY LINGUISTIC BIAS PENALTIES (Anti-LLM Heuristics)
    # ---------------------------------------------------------
    
    # 1. Repetition Penalty: LLMs use repetitive structures. Flat penalty.
    if repetition_count > 0:
        risk += (repetition_count * 0.15)
        
    # 2. Reading Ease Penalty: TikToks should be 5th-8th grade level (60-80).
    if reading_ease < 50.0:
        # Too academic/complex (Classic AI)
        risk += 0.20
    elif reading_ease > 90.0:
        # Too simplistic/childish
        risk += 0.10
    
    # Apply a curve to make scores much more generous
    # Most content should be LOW or MEDIUM risk
    risk = risk ** 1.35  # Significantly reduce risk scores (was 1.15)
    
    # Apply a baseline reduction - subtract 0.15 from all scores
    risk = max(0.0, risk - 0.15)
        
    risk = round(min(max(risk, 0.0), 1.0), 4)
    
    # Risk level classification with very generous thresholds
    # Goal: Most episodes should be LOW or MEDIUM, only 1-2 out of 6-7 should be HIGH
    if risk < 0.60:  # Raised from 0.50
        risk_level = "LOW"
    elif risk < 0.80:  # Raised from 0.75
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"
    
    # Segment-level risks
    segment_risks = _build_segment_risks(dropoff)
    
    # Build reason
    reason = _build_retention_reason(
        hook_strength, conflict_score, emotion_variance,
        cliffhanger_score, conflict_density, risk_level
    )
    
    # Generate recommendations
    recommendations = _generate_recommendations(
        hook_strength, conflict_score, emotion_variance,
        cliffhanger_score, conflict_density, emotion_peak,
        climax_position, resolution_absence
    )
    
    # Check for Linguistic/LLM bias
    linguistic_recs = _generate_linguistic_recommendations(linguistic)
    if linguistic_recs:
        recommendations = linguistic_recs + recommendations # Prioritize fixing AI bias
        
    return {
        "risk_score": risk,
        "risk_level": risk_level,
        "segment_risks": segment_risks,
        "reason": reason,
        "recommendations": recommendations,
    }


def _build_segment_risks(dropoff: dict) -> dict:
    """Build segment-level risk breakdown"""
    segments = dropoff.get("segments", [])
    
    segment_risks = {}
    for seg in segments:
        label = seg.get("label", "Unknown")
        risk = seg.get("dropoff_risk", 0.5)
        
        if risk < 0.4:
            risk_label = "LOW"
        elif risk < 0.65:
            risk_label = "MEDIUM"
        else:
            risk_label = "HIGH"
        
        segment_risks[label] = {
            "risk": round(risk, 3),
            "label": risk_label,
        }
    
    return segment_risks


def _build_retention_reason(
    hook: float,
    conflict: float,
    emotion_var: float,
    cliffhanger: float,
    conflict_dens: float,
    risk_level: str
) -> str:
    """Build human-readable retention risk explanation"""
    weaknesses = []
    strengths = []
    
    # Identify weaknesses with generous thresholds
    if hook < 0.25:
        weaknesses.append("Hook could be stronger to grab attention faster")
    if conflict < 0.20:
        weaknesses.append("Could benefit from more conflict in middle section")
    if emotion_var < 0.08:
        weaknesses.append("Emotional arc could be more dynamic")
    if cliffhanger < 0.25:
        weaknesses.append("Cliffhanger could be more compelling")
    if conflict_dens < 0.15:
        weaknesses.append("Could add more tension in development phase")
    
    # Identify strengths with generous thresholds
    if hook >= 0.45:
        strengths.append("Strong opening hook")
    if conflict >= 0.40:
        strengths.append("Good narrative conflict")
    if emotion_var >= 0.15:
        strengths.append("Dynamic emotional progression")
    if cliffhanger >= 0.45:
        strengths.append("Strong cliffhanger ending")
    
    # Build message
    if risk_level == "LOW":
        if strengths:
            return f"Low retention risk. Strengths: {'; '.join(strengths)}"
        else:
            return "Low retention risk. Solid engagement across all metrics"
    elif risk_level == "MEDIUM":
        if weaknesses:
            return f"Moderate retention risk. Areas to improve: {'; '.join(weaknesses[:2])}"
        else:
            return "Moderate retention risk. Some engagement but room for improvement"
    else:
        if weaknesses:
            return f"High retention risk. Critical issues: {'; '.join(weaknesses[:3])}"
        else:
            return "High retention risk. Multiple engagement issues detected"


def _generate_recommendations(
    hook: float,
    conflict: float,
    emotion_var: float,
    cliffhanger: float,
    conflict_dens: float,
    emotion_peak: float,
    climax_pos: float,
    resolution_absence: float
) -> list:
    """Generate actionable recommendations for improvement"""
    recommendations = []
    
    # Hook recommendations with generous thresholds
    if hook < 0.25:
        recommendations.append({
            "area": "Opening Hook",
            "priority": "HIGH",
            "suggestion": "Consider starting with a more attention-grabbing opening"
        })
    
    # Conflict recommendations with generous thresholds
    if conflict < 0.20 or conflict_dens < 0.15:
        recommendations.append({
            "area": "Conflict Development",
            "priority": "MEDIUM",
            "suggestion": "Could add more tension or obstacles in the middle section"
        })
    
    # Emotional arc recommendations with generous thresholds
    if emotion_var < 0.08:
        recommendations.append({
            "area": "Emotional Arc",
            "priority": "MEDIUM",
            "suggestion": "Consider adding more emotional variety for dynamic progression"
        })
    
    if emotion_peak < 0.35:
        recommendations.append({
            "area": "Emotional Intensity",
            "priority": "LOW",
            "suggestion": "Could increase emotional intensity at key moments"
        })
    
    # Climax positioning
    if climax_pos < 0.30 or climax_pos > 0.90:
        recommendations.append({
            "area": "Story Structure",
            "priority": "LOW",
            "suggestion": "Consider positioning the emotional peak between 50-80% of the story"
        })
    
    # Cliffhanger recommendations with generous thresholds
    if cliffhanger < 0.25:
        recommendations.append({
            "area": "Cliffhanger",
            "priority": "HIGH",
            "suggestion": "Consider ending with more unresolved tension or questions"
        })
    
    # Resolution recommendations
    if resolution_absence < 0.40:
        recommendations.append({
            "area": "Ending Resolution",
            "priority": "LOW",
            "suggestion": "Consider leaving some questions unanswered to maintain tension"
        })
        
    return recommendations

def _generate_linguistic_recommendations(linguistic: dict) -> list:
    """Generate recommendations related strictly to LLM Bias"""
    recs = []
    reading_ease = linguistic.get("reading_ease", 100.0)
    repetition = linguistic.get("repetition_count", 0)
    
    if repetition > 0:
        recs.append({
            "area": "Linguistic Bias",
            "priority": "CRITICAL",
            "suggestion": "Your script uses repetitive sentence structures typical of AI. Rewrite transitions like 'Moreover' or 'Additionally'."
        })
        
    if reading_ease < 50.0:
        recs.append({
            "area": "Readability",
            "priority": "HIGH",
            "suggestion": f"Script reading level is too complex (Score: {reading_ease}). Short-form video favors 5th-8th grade vocab. Simplify sentences."
        })
        
    return recs
