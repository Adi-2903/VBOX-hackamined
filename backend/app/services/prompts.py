DIRECTION_LIBRARY = """
# VIRAL DIRECTION / FORMAT LIBRARY – 2026 Playbook

FINANCE
Money Mistake Confessions
Structure: 1. Shocking loss number 2. What I did wrong 3. The moment I realized 4. What it cost me 5. How I fixed it 6. Warning for viewers
Wealth Secret Explainer
Structure: 1. Controversial claim 2. Why most people don't know this 3. Step-by-step breakdown 4. Who uses this 5. How to apply it 6. Controversy address

CAREER
Quit My Job Storytime
Structure: 1. The breaking point 2. Why I stayed so long 3. The final straw 4. The resignation moment 5. First 30 days after 6. Would I do it again
Toxic Workplace Exposé
Structure: 1. First red flag you ignored 2. What normalized toxicity looks like 3. The moment you knew 4. The mental health impact 5. How you got out 6. Warning signs list

HEALTH & FITNESS
Body Transformation Series
Structure: 1. Starting point 2. Week 1–2 reality check 3. Midpoint struggle 4. What actually moved the needle 5. The biggest setback week 6. Final results

PRODUCTIVITY
Morning Routine Deconstruction
Structure: 1. Hype around popular routine 2. Why it fails for 90% of people 3. My real (imperfect) routine 4. Science behind choices 5. Proof it works 6. How to adapt
Deep Work vs Shallow Work Exposé
Structure: 1. Shocking truth about "busy" days 2. Deep work defined 3. Real examples 4. How notifications destroy it 5. 2-hour experiment 6. Challenge to viewers

ENTREPRENEURSHIP
Failed Business Storytime
Structure: 1. The exciting idea 2. Money invested 3. First signs it wasn’t working 4. Brutal moment of truth 5. What I lost 6. What I’d do differently
Side Hustle Reality Check
Structure: 1. Gurus vs reality 2. First-month numbers 3. Hours worked vs income 4. Hidden costs 5. Is it worth it? 6. Recommendation

SELF IMPROVEMENT
Habit That Changed Everything
Structure: 1. Problem before habit 2. Why I started 3. Week 1 awkwardness 4. Month 1 shift 5. Month 3+ compounding 6. Why it works
Identity Shift Story
Structure: 1. Old version of myself 2. Breaking moment 3. Decision to change 4. What I gave up 5. Who I am now 6. Uncomfortable truth

TECHNOLOGY
AI Tool Experiment Series
Structure: 1. Hype around tool 2. My goal 3. Setup & test 4. Surprising results 5. Time saved/lost 6. Verdict
Gadget Reality Check
Structure: 1. Marketing promises 2. What I paid 3. Daily usage 4. Hidden downsides 5. Worth the money? 6. Who it’s for

SOCIAL COMMENTARY
Trend Deep Dive
Structure: 1. Surface-level trend 2. Why it exploded 3. Hidden psychology 4. Who profits 5. Dark side 6. Bigger pattern
Relatable Social Struggle Series
Structure: 1. Everyday problem 2. Why it feels isolating 3. My low moment 4. Small action that helped 5. Community reaction 6. Encouragement
"""

HOOK_LIBRARY = """
# VIRAL HOOK & CLIFFHANGER LIBRARY

FINANCE
Hooks: "I lost ₹3,00,000 in one week. Here's the stupid reason why." / "Rich people legally pay 0% tax. Here's exactly how."
Cliffhangers: "But the worst part? I made the same mistake twice." / "And part 2 breaks down how to actually use this yourself."

CAREER
Hooks: "I quit my corporate job on a Tuesday. No backup plan." / "My manager said one sentence. I handed in my notice."
Cliffhangers: "Month 2 after quitting was the hardest month of my life." / "The final thing that happened — I still can't believe it was legal."

HEALTH & FITNESS
Hooks: "Day 1. I can barely do 5 push-ups. Watch what happens in 90 days." / "I stopped trying to look like Instagram. Here's what I look like now."
Cliffhangers: "Week 6 I almost quit. What stopped me is something I'm embarrassed to admit."

PRODUCTIVITY
Hooks: "The 5am routine is not for you. And the productivity gurus know it." / "I spent 12 hours building my perfect Notion system. I abandoned it in week 2."
Cliffhangers: "But the reason it failed isn't laziness. It's something systemic nobody warns you about."
"""

STORY_PROMPT_TEMPLATE = """You are an expert short-form video creator for Instagram Reels, TikTok, YouTube Shorts — specializing in addictive, relatable episodic "story time" content for Indian audiences in 2026.

Your job: Generate {episodes} high-virality episode(s) based on the user idea.

Follow these steps EXACTLY:
- Figure out the main category from the idea.
- Stick to ONLY the direction the user chose.
- For episode 1: Pick a strong hook from the hook library (or make one very close if nothing fits perfectly).
- Build a natural story arc across the episodes: start with something that grabs attention, add tension and feelings in the middle, end each one with a cliffhanger that makes people click next.
- Keep the same characters and timeline — what happens early must matter later.
- Write each episode short enough for 40–60 seconds spoken (around 150–250 words).
- Talk like a normal person chatting with a friend: casual words, "yaar", "bhai", short sentences, some laughs or sighs. Go a little more serious only when the story is heavy.
- Keep it real for India 2026: normal jobs pay ₹40k–₹90k/month, freelance starts small and shaky, rent/food in cities ₹15k–₹25k/month, family pressure, slow progress, no sudden rich endings.
- End every episode with a fresh cliffhanger that teases the next real feeling in THIS story — don't copy old ones.

Target Audience: {audience}
User Idea: {idea}
Chosen Direction: {direction}

HOOK LIBRARY:
{hook_library}

DIRECTION LIBRARY:
{direction_library}

Return ONLY clean JSON — nothing else (no markdown wrappers):

{{
  "category": "...",
  "direction": "...",
  "hook": "...",
  "episodes": [
    {{
      "episode_number": 1,
      "title": "... (short catchy title)",
      "hook": "... (first line or two of the video)",
      "story": "... (full spoken script, feels like talking to a friend)",
      "cliffhanger": "... (one sentence teaser for next episode)",
      "text_overlays_suggestions": ["short phrase 1", "phrase 2", "phrase 3"]
    }}
  ]
}}
"""

ML_EPISODE_ANALYSIS_PROMPT = """You are an expert ML text analysis API. Your job is to analyze this episodic story script and return highly structured JSON matching our pipeline specification.

Analyze the sentiment, emotional arc, hook strength, dropoff risks, and cliffhanger impact.

Text to analyze:
{text}

Category: {category}

Return ONLY a valid JSON object matching this schema exactly (No markdown formatting, no backticks):
{{
    "category": "{category}",
    "features": {{
        "semantic_features": {{
            "hook_strength": 0.85,  // float 0.0-1.0
            "conflict_score": 0.70, // float 0.0-1.0
            "cliffhanger_score": 0.90, // float 0.0-1.0
            "hook_reason": "String explaining hook strength",
            "conflict_reason": "String explaining conflict density",
            "cliffhanger_reason": "String explaining cliffhanger tension"
        }},
        "emotional_arc": {{
            "emotion_variance": 0.35, // float 0.0-1.0
            "emotion_peak": 0.95, // float 0.0-1.0
            "climax_position": 0.80, // float 0.0-1.0 representing percentage into the episode
            "arc_shape": "RISING_ACTION", // One of: RISING_ACTION, FALLING, DYNAMIC, FLAT
            "reason": "String explaining emotional arc"
        }},
        "narrative_structure": {{
            "structure_quality": "EXCELLENT", // One of: EXCELLENT, GOOD, FAIR, POOR
            "hook_position_score": 0.90, // float 0.0-1.0
            "conflict_density": 0.65, // float 0.0-1.0
            "twist_position_score": 0.85, // float 0.0-1.0
            "reason": "String explaining narrative structure"
        }},
        "dropoff_prediction": {{
            "overall_dropoff_risk": 0.25, // float 0.0-1.0
            "high_risk_segments": [1], // list of indices where dropoff > 0.45
            "segments": [
                {{"label": "Hook (0-10s)", "dropoff_risk": 0.15, "engagement_score": 0.90}},
                {{"label": "Setup (10-30s)", "dropoff_risk": 0.30, "engagement_score": 0.70}},
                {{"label": "Action (30-45s)", "dropoff_risk": 0.20, "engagement_score": 0.85}},
                {{"label": "Climax (45-55s)", "dropoff_risk": 0.10, "engagement_score": 0.95}},
                {{"label": "Cliffhanger (55-60s)", "dropoff_risk": 0.05, "engagement_score": 0.98}}
            ],
            "reason": "String explaining dropoff prediction"
        }}
    }},
    "retention": {{
        "risk_score": 0.25, // float 0.0-1.0
        "risk_level": "LOW", // One of: LOW, MEDIUM, HIGH
        "segment_risks": {{
            "Hook (0-10s)": {{"risk": 0.15, "label": "LOW"}},
            "Setup (10-30s)": {{"risk": 0.30, "label": "MEDIUM"}},
            "Action (30-45s)": {{"risk": 0.20, "label": "LOW"}},
            "Climax (45-55s)": {{"risk": 0.10, "label": "LOW"}},
            "Cliffhanger (55-60s)": {{"risk": 0.05, "label": "LOW"}}
        }},
        "reason": "String explaining retention analysis",
        "recommendations": [
            {{"area": "Setup", "priority": "MEDIUM", "suggestion": "String suggesting how to improve pacing"}}
        ]
    }},
    "cliffhanger": {{
        "cliffhanger_score": 8.5, // float 0.0-10.0
        "strength": "STRONG", // One of: STRONG, MODERATE, WEAK
        "components": {{
            "surprise": 0.85, // float 0.0-1.0
            "emotion_spike": 0.90, // float 0.0-1.0
            "conflict_signal": 0.80, // float 0.0-1.0
            "keyword_boost": 1.05 // float near 1.0
        }},
        "category": "{category}",
        "keywords_found": {{
            "hook": ["keyword1", "keyword2"],
            "conflict": ["keyword3"],
            "resolution": []
        }},
        "reason": "String explaining cliffhanger details"
    }},
    "summary": {{
        "overall_score": 88.5, // float 0.0-100.0
        "engagement_level": "EXCELLENT", // One of: EXCELLENT, GOOD, FAIR, POOR
        "key_strengths": ["Strong opening hook", "Compelling cliffhanger"],
        "key_weaknesses": ["Minor pacing drop in setup"]
    }}
}}
"""
