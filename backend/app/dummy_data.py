"""
Dummy data generators matching the EXACT output format from BACKEND_INTEGRATION_GUIDE.md.
Replace these with actual ML/GenAI calls later.
"""
import random


# ──────────────────────────────────────────────
# DUMMY GenAI GENERATION
# ──────────────────────────────────────────────

DUMMY_EPISODES_BANK = [
    {
        "title": "Midnight Strangers & Chai",
        "hook": "The 3 AM conversation at Marine Drive fixed more than my overthinking.",
        "story": "It was 2 AM on Marine Drive. Just me, a cup of chai, and two strangers who looked like they hadn't slept in weeks. We weren't tourists; we were just running away from the day. The first guy, Rahul, looked at the sea and said, 'I quit my job yesterday. No savings, no plan.' I thought I was alone in this. Then the girl, Anjali, laughed and said, 'I'm pretending to be happy for my parents. My bank account has ₹4,000.' I realized we were all just nodes in the same broken system.",
        "cliffhanger": "But the second stranger had a secret that made me question everything about my career.",
        "text_overlays_suggestions": ["2 AM. Marine Drive.", "₹65k Salary vs ₹10k Savings.", "We were all hiding."]
    },
    {
        "title": "The Bank Balance Secret",
        "hook": "What Anjali showed me on her phone changed the way I see hustle culture forever.",
        "story": "Rahul didn't talk about his job. Anjali pulled out her phone and showed me her bank balance: zero. She was ₹2 lakh in debt from her family's wedding. She wasn't working freelance to save money; she was working to survive. That's when I realized the 'hustle culture' isn't about growth, it's about survival.",
        "cliffhanger": "And the final thing we decided that night — I still can't believe I agreed to do it.",
        "text_overlays_suggestions": ["₹2 Lakh Debt.", "Stop Comparing.", "Small Wins Only."]
    },
    {
        "title": "The Pact Under Streetlights",
        "hook": "Three strangers. One pact. Zero regrets.",
        "story": "We walked back from Marine Drive at 4 AM. The streetlights were dim, but our conversation was the clearest thing I'd heard in months. Rahul said he'd stop chasing promotions. Anjali said she'd tell her parents the truth. And me? I promised to stop measuring my worth in salary slips.",
        "cliffhanger": "But when I got home, a message was waiting on my phone that changed everything.",
        "text_overlays_suggestions": ["4 AM Walk.", "The Pact.", "Worth ≠ Salary."]
    },
    {
        "title": "The Morning After",
        "hook": "I woke up expecting regret. Instead, I found clarity.",
        "story": "Sunlight hit my face at 8 AM. I checked my phone: 47 notifications, 3 missed calls from my manager, and one text from Rahul — 'Did you really quit?' I hadn't quit. Not yet. But something shifted. I made chai the way my grandmother used to — slowly, deliberately, not scrolling through LinkedIn.",
        "cliffhanger": "Then my manager's next message arrived, and I realized the pact was about to be tested.",
        "text_overlays_suggestions": ["47 Notifications.", "Chai, Not LinkedIn.", "The Test Begins."]
    },
    {
        "title": "The Resignation That Wasn't",
        "hook": "I typed 'I quit' three times and deleted it every time.",
        "story": "My manager called again at noon. 'We need to talk about your performance review.' I sat in the conference room, palms sweating. She slid a paper across the table — not a termination letter, but a promotion. More money, same emptiness. I remembered Anjali's zero balance. I remembered Rahul's courage.",
        "cliffhanger": "I said the five words that shocked everyone in the room, including myself.",
        "text_overlays_suggestions": ["The Promotion.", "Same Emptiness.", "Five Words."]
    },
    {
        "title": "The Unraveling",
        "hook": "The domino effect of one honest conversation at Marine Drive.",
        "story": "Word spread fast. My team thought I was having a breakdown. HR scheduled a 'wellness check.' But Anjali texted: 'I told my parents everything. They cried. Then they hugged me.' Rahul updated his LinkedIn — not with a new job, but with a blog post titled 'Why I Stopped Pretending.'",
        "cliffhanger": "That evening, my phone buzzed with a message from a number I didn't recognize.",
        "text_overlays_suggestions": ["Domino Effect.", "Honest Conversations.", "The Unknown Number."]
    },
    {
        "title": "Full Circle at Marine Drive",
        "hook": "90 days later, I went back to the same spot at 2 AM.",
        "story": "Marine Drive hadn't changed. But I had. This time, I wasn't running away — I was returning. Rahul was already there, this time with a proper career plan. Anjali arrived with her debt cut in half. And me? I had taken a pay cut for a job that didn't make me want to disappear.",
        "cliffhanger": "But sitting on the same wall, a new stranger joined us — and their story made ours look simple.",
        "text_overlays_suggestions": ["90 Days Later.", "Same Wall, New Us.", "The New Stranger."]
    },
    {
        "title": "The Ripple",
        "hook": "One chai. Three strangers. A thousand ripples.",
        "story": "The new stranger was recording a podcast about burnout. She'd heard Rahul's blog post. She asked if she could share our story — not as a success story, but as a survival story. We agreed. The episode went viral. Not because we were inspiring, but because we were honest.",
        "cliffhanger": "And then the emails started pouring in from people who needed their own Marine Drive moment.",
        "text_overlays_suggestions": ["Not Success. Survival.", "Viral Honesty.", "Marine Drive Moments."]
    },
]

CATEGORIES = ["LIFESTYLE", "DRAMA", "THRILLER", "COMEDY", "DOCUMENTARY", "SCI-FI"]
DIRECTIONS = [
    "Tea Session Stories (Group Sharing Circle)",
    "Cinematic Monologue (Single Character Arc)",
    "Split Screen Parallel Lives",
    "Found Footage Documentary Style",
    "Animated Graphic Novel Narration",
]


DIRECTION_SUGGESTIONS = [
    {"direction_name": "Tea Session Stories (Group Sharing Circle)", "category": "Lifestyle", "why_it_fits": "Perfect for raw, relatable group conversations that feel authentic and drive engagement through shared vulnerability."},
    {"direction_name": "Cinematic Monologue (Single Character Arc)", "category": "Drama", "why_it_fits": "Strong for deeply personal stories where one voice carries the emotional weight and creates intimate connection."},
    {"direction_name": "Split Screen Parallel Lives", "category": "Documentary", "why_it_fits": "Great for contrasting perspectives or showing how the same situation affects different people simultaneously."},
    {"direction_name": "Found Footage Documentary Style", "category": "Thriller", "why_it_fits": "Adds raw authenticity and urgency. The 'discovered' format creates instant curiosity and suspense."},
    {"direction_name": "Animated Graphic Novel Narration", "category": "Sci-Fi", "why_it_fits": "Ideal for high-concept stories where visual storytelling can amplify world-building beyond live-action."},
]


def generate_dummy_directions(concept: str) -> dict:
    """Return 3 suggested directions matching GenAI's generate_directions() output."""
    selected = random.sample(DIRECTION_SUGGESTIONS, 3)
    return {"suggested_directions": selected}


def generate_dummy_series(concept: str, num_episodes: int, direction: str = "", audience: str = "") -> dict:
    """Generate a dummy series matching the GenAI test_output.json format."""
    eps = random.sample(DUMMY_EPISODES_BANK, min(num_episodes, len(DUMMY_EPISODES_BANK)))
    episodes = []
    for i, ep in enumerate(eps, 1):
        episodes.append({
            "episode_number": i,
            "title": ep["title"],
            "hook": ep["hook"],
            "story": ep["story"],
            "cliffhanger": ep["cliffhanger"],
            "text_overlays_suggestions": ep["text_overlays_suggestions"],
        })
    return {
        "category": random.choice(CATEGORIES),
        "direction": direction or random.choice(DIRECTIONS),
        "hook": episodes[0]["hook"] if episodes else concept,
        "episodes": episodes,
    }


# ──────────────────────────────────────────────
# DUMMY ML ANALYSIS — matches BACKEND_INTEGRATION_GUIDE.md output format
# ──────────────────────────────────────────────

SEGMENT_LABELS = [
    "Opening (0-10s)",
    "Setup (10-30s)",
    "Development (30-60s)",
    "Climax (60-80s)",
    "Ending (80-90s)",
]

HOOK_KEYWORDS = ["mystery", "shocking", "secret", "discovery", "impossible"]
CONFLICT_KEYWORDS = ["danger", "threat", "crisis", "confrontation", "tension"]


def _risk_label(risk: float) -> str:
    if risk < 0.45:
        return "LOW"
    elif risk < 0.70:
        return "MEDIUM"
    return "HIGH"


def _engagement_label(score: float) -> str:
    if score >= 70:
        return "EXCELLENT"
    elif score >= 45:
        return "GOOD"
    elif score >= 30:
        return "FAIR"
    return "POOR"


def _cliff_strength(score: float) -> str:
    if score >= 5.0:
        return "STRONG"
    elif score >= 2.5:
        return "MODERATE"
    return "WEAK"


def analyze_dummy_episode(episode_number: int = 1, title: str = "Untitled", text: str = "", category: str | None = None) -> dict:
    """
    Generate a dummy analysis result matching the EXACT output format
    from BACKEND_INTEGRATION_GUIDE.md §Output Format.
    """
    cat = category or random.choice(["crime", "romance", "horror", "thriller", "drama", "comedy"])

    # --- Semantic features ---
    hook_strength = round(random.uniform(0.25, 0.95), 3)
    conflict_score = round(random.uniform(0.20, 0.85), 3)
    cliff_score = round(random.uniform(0.25, 0.90), 3)

    # --- Emotional arc ---
    emotion_variance = round(random.uniform(0.05, 0.45), 3)
    emotion_peak = round(random.uniform(0.60, 0.99), 3)
    climax_position = round(random.uniform(0.45, 0.85), 2)
    arc_shapes = ["RISING_ACTION", "FALLING", "DYNAMIC", "FLAT"]
    arc_shape = random.choice(arc_shapes)

    # --- Narrative structure ---
    qualities = ["EXCELLENT", "GOOD", "FAIR", "POOR"]
    hook_pos_score = round(random.uniform(0.5, 0.95), 2)
    conflict_density = round(random.uniform(0.25, 0.75), 2)
    twist_pos_score = round(random.uniform(0.4, 0.90), 2)
    structure_quality = random.choice(qualities)

    # --- Dropoff prediction ---
    segments = []
    high_risk_indices = []
    for idx, label in enumerate(SEGMENT_LABELS):
        engagement = round(random.uniform(0.35, 0.85), 2)
        dropoff = round(max(0, 1.0 - engagement - random.uniform(0, 0.15)), 2)
        segments.append({"label": label, "dropoff_risk": dropoff, "engagement_score": engagement})
        if dropoff > 0.45:
            high_risk_indices.append(idx)

    overall_dropoff = round(sum(s["dropoff_risk"] for s in segments) / len(segments), 3)

    # --- Retention ---
    risk_score = round(random.uniform(0.20, 0.80), 3)
    risk_level = _risk_label(risk_score)

    segment_risks = {}
    for seg in segments:
        segment_risks[seg["label"]] = {"risk": seg["dropoff_risk"], "label": _risk_label(seg["dropoff_risk"])}

    recommendations = []
    if hook_strength < 0.5:
        recommendations.append({
            "area": "Opening Hook",
            "priority": "CRITICAL",
            "suggestion": "Start with a shocking revelation or unanswered question in the first 5 seconds."
        })
    if conflict_density < 0.4:
        recommendations.append({
            "area": "Conflict Density",
            "priority": "HIGH",
            "suggestion": "Increase tension in the development section (10-60s) by adding obstacles or opposition."
        })
    if cliff_score < 0.5:
        recommendations.append({
            "area": "Cliffhanger",
            "priority": "HIGH",
            "suggestion": "End with an unresolved tension point — avoid closure in the last 10 seconds."
        })
    if high_risk_indices:
        seg_names = [SEGMENT_LABELS[i] for i in high_risk_indices]
        recommendations.append({
            "area": "Pacing",
            "priority": "MEDIUM",
            "suggestion": f"High drop-off risk in: {', '.join(seg_names)}. Add emotional beats or visual hooks."
        })
    if not recommendations:
        recommendations.append({
            "area": "General",
            "priority": "LOW",
            "suggestion": "Content structure is solid. Consider minor pacing tweaks for peak engagement."
        })

    retention_reason = f"{'High' if risk_level == 'HIGH' else 'Moderate' if risk_level == 'MEDIUM' else 'Low'} retention risk. "
    retention_reason += f"Hook: {hook_strength:.2f}, Conflict: {conflict_score:.2f}, Cliffhanger: {cliff_score:.2f}"

    # --- Cliffhanger ---
    surprise = round(random.uniform(0.15, 0.85), 3)
    emotion_spike = round(random.uniform(0.10, 0.65), 2)
    conflict_signal = round(random.uniform(0.15, 0.70), 2)
    keyword_boost = round(random.uniform(0.95, 1.15), 2)
    raw_cliff = 0.65 * surprise + 0.25 * emotion_spike + 0.10 * conflict_signal
    cliffhanger_score = round(min(10, raw_cliff * keyword_boost * 10), 1)

    keywords_hook = random.sample(HOOK_KEYWORDS, k=random.randint(1, 3))
    keywords_conflict = random.sample(CONFLICT_KEYWORDS, k=random.randint(1, 2))

    # --- Summary ---
    overall_score = round(max(5, min(100, (1 - risk_score) * 80 + cliffhanger_score * 2)), 1)
    engagement_level = _engagement_label(overall_score)

    key_strengths = []
    key_weaknesses = []
    if arc_shape == "DYNAMIC":
        key_strengths.append("Dynamic emotional arc")
    if hook_strength > 0.7:
        key_strengths.append("Strong opening hook")
    if cliffhanger_score >= 5.0:
        key_strengths.append("Compelling cliffhanger")
    if emotion_variance > 0.2:
        key_strengths.append("Good emotional range")
    if not key_strengths:
        key_strengths.append("Consistent pacing")

    if cliffhanger_score < 2.5:
        key_weaknesses.append("Weak cliffhanger")
    if hook_strength < 0.4:
        key_weaknesses.append("Weak opening hook")
    if conflict_density < 0.3:
        key_weaknesses.append("Low conflict density")
    if high_risk_indices:
        key_weaknesses.append("High drop-off risk segments")
    if not key_weaknesses:
        key_weaknesses.append("Minor pacing inconsistencies")

    return {
        "category": cat,
        "features": {
            "semantic_features": {
                "hook_strength": hook_strength,
                "conflict_score": conflict_score,
                "cliffhanger_score": cliff_score,
                "hook_reason": f"Hook semantic similarity: {hook_strength:.3f}",
                "conflict_reason": f"Conflict density measured at {conflict_score:.3f}",
                "cliffhanger_reason": f"Ending tension level: {cliff_score:.3f}",
            },
            "emotional_arc": {
                "emotion_variance": emotion_variance,
                "emotion_peak": emotion_peak,
                "climax_position": climax_position,
                "arc_shape": arc_shape,
                "reason": f"Emotional arc classified as {arc_shape} with peak at position {climax_position}",
            },
            "narrative_structure": {
                "structure_quality": structure_quality,
                "hook_position_score": hook_pos_score,
                "conflict_density": conflict_density,
                "twist_position_score": twist_pos_score,
                "reason": f"Structure quality: {structure_quality}. Hook at {hook_pos_score}, twist at {twist_pos_score}",
            },
            "dropoff_prediction": {
                "overall_dropoff_risk": overall_dropoff,
                "high_risk_segments": high_risk_indices,
                "segments": segments,
                "reason": f"Overall dropoff risk: {overall_dropoff:.3f}. {len(high_risk_indices)} high-risk segment(s) detected.",
            },
        },
        "retention": {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "segment_risks": segment_risks,
            "reason": retention_reason,
            "recommendations": recommendations,
        },
        "cliffhanger": {
            "cliffhanger_score": cliffhanger_score,
            "strength": _cliff_strength(cliffhanger_score),
            "components": {
                "surprise": surprise,
                "emotion_spike": emotion_spike,
                "conflict_signal": conflict_signal,
                "keyword_boost": keyword_boost,
            },
            "category": cat,
            "keywords_found": {
                "hook": keywords_hook,
                "conflict": keywords_conflict,
                "resolution": [],
            },
            "reason": f"{'Strong' if cliffhanger_score >= 5 else 'Moderate' if cliffhanger_score >= 2.5 else 'Weak'} surprise element; emotional intensity {'spikes' if emotion_spike > 0.4 else 'moderate'} at the end",
        },
        "summary": {
            "overall_score": overall_score,
            "engagement_level": engagement_level,
            "key_strengths": key_strengths,
            "key_weaknesses": key_weaknesses,
        },
    }


def analyze_dummy_series(episodes: list[dict], category: str | None = None) -> dict:
    """Generate full series analysis with per-episode + series insights."""
    analyses = []
    for ep in episodes:
        analysis = analyze_dummy_episode(
            episode_number=ep.get("episode_number", 1),
            title=ep.get("title", "Untitled"),
            text=ep.get("story", ""),
            category=category,
        )
        analyses.append({
            "episode_number": ep.get("episode_number", 1),
            "title": ep.get("title", "Untitled"),
            "analysis": analysis,
        })

    scores = [a["analysis"]["summary"]["overall_score"] for a in analyses]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
    weakest = min(range(len(scores)), key=lambda i: scores[i]) + 1 if scores else 1
    strongest = max(range(len(scores)), key=lambda i: scores[i]) + 1 if scores else 1

    if len(scores) >= 3:
        first_half = sum(scores[:len(scores) // 2]) / (len(scores) // 2)
        second_half = sum(scores[len(scores) // 2:]) / (len(scores) - len(scores) // 2)
        trend = "improving" if second_half > first_half + 3 else ("declining" if first_half > second_half + 3 else "stable")
    else:
        trend = "stable"

    return {
        "episodes": analyses,
        "series_insights": {
            "avg_overall_score": avg_score,
            "trend": trend,
            "consistency_score": round(1.0 - (max(scores) - min(scores)) / 100, 2) if scores else 1.0,
            "weakest_episode": weakest,
            "strongest_episode": strongest,
        },
    }
