# Quick Start Guide - ML Retention Model

## Installation

```bash
# Already installed if you have the project
pip install -r requirements.txt
```

## Basic Usage

### Analyze a Single Episode

```python
from ml_engine.ml_pipeline_v2 import analyze_episode_v2

# Your episode text
text = """
I lost $50,000 in crypto last year. Everyone said it was a scam, but I didn't listen.
The market crashed overnight. My savings were gone. I had to sell my car to pay rent.
But then I discovered something that changed everything...
"""

# Analyze (category auto-detected)
result = analyze_episode_v2(text)

# Print results
print(f"Overall Score: {result['summary']['overall_score']}/100")
print(f"Engagement: {result['summary']['engagement_level']}")
print(f"Retention Risk: {result['retention']['risk_level']}")
print(f"Category: {result['category']}")

# Get recommendations
for rec in result['retention']['recommendations'][:3]:
    print(f"[{rec['priority']}] {rec['area']}: {rec['suggestion']}")
```

### Analyze a Full Series

```python
from ml_engine.ml_pipeline_v2 import analyze_series_v2

episodes = [
    "Episode 1 text...",
    "Episode 2 text...",
    "Episode 3 text..."
]

result = analyze_series_v2(episodes)

# Series metrics
insights = result['series_insights']
print(f"Average Score: {insights['avg_overall_score']}/100")
print(f"Consistency: {insights['consistency_score']}/100")
print(f"Trend: {insights['trend']}")

# Individual episodes
for ep in result['episodes']:
    print(f"Episode {ep['episode_number']}: {ep['summary']['overall_score']}/100")
```

## Understanding Scores

### Overall Score (0-100)
- **55-100**: EXCELLENT - Ready for production
- **40-54**: GOOD - Minor improvements recommended
- **25-39**: FAIR - Some improvements needed
- **0-24**: NEEDS WORK - Significant revisions required

### Retention Risk
- **LOW** (<0.50): Great retention potential
- **MEDIUM** (0.50-0.75): Acceptable retention
- **HIGH** (>0.75): Risk of viewer drop-off

### Feature Scores (0-1)
- **Hook Strength**: Opening engagement (first 10%)
- **Conflict Score**: Middle tension (10-80%)
- **Cliffhanger Score**: Ending hook (last 10%)
- **Emotional Arc**: 1-10 scale of emotional progression

## Categories

Auto-detected categories:
- `finance` - Money, investing, budgeting
- `career` - Jobs, workplace, professional growth
- `health` - Fitness, wellness, mental health
- `productivity` - Time management, habits, systems
- `entrepreneurship` - Startups, business, side hustles
- `self_improvement` - Personal growth, mindset
- `lifestyle` - Daily life, relationships, social
- `technology` - Tech, gadgets, AI
- `education` - Learning, skills, academics
- `history_science_culture` - Knowledge, discovery

## Tips for Better Scores

### 1. Strong Hook (First 10 seconds)
✅ Start with shocking statement or question
✅ Create immediate curiosity
✅ Use category-specific keywords

### 2. Build Conflict (Middle 60%)
✅ Add obstacles and tension
✅ Show emotional progression
✅ Keep viewers engaged

### 3. Compelling Cliffhanger (Last 10 seconds)
✅ Leave questions unanswered
✅ Create urgency for next episode
✅ Avoid neat resolutions

### 4. Use Keywords
✅ Include category-specific terms
✅ Use emotional language
✅ Add action verbs

## Common Issues & Fixes

### Low Score (<40)
**Problem**: Weak hook, flat emotion, or poor structure
**Fix**: 
- Rewrite opening with shocking statement
- Add more conflict and tension
- Strengthen cliffhanger ending

### Wrong Category Detection
**Problem**: Content misclassified
**Fix**:
- Add more category-specific keywords
- Specify category manually: `analyze_episode_v2(text, category="finance")`

### Too Many Recommendations
**Problem**: Model suggests many improvements
**Fix**:
- Focus on HIGH priority items first
- Ignore LOW priority suggestions initially
- Iterate based on score improvements

## Advanced Usage

### Get Detailed Features

```python
result = analyze_episode_v2(text)

# Semantic features
semantic = result['features']['semantic_features']
print(f"Hook: {semantic['hook_strength']:.3f}")
print(f"Conflict: {semantic['conflict_score']:.3f}")
print(f"Cliffhanger: {semantic['cliffhanger_score']:.3f}")

# Emotional arc
emotional = result['features']['emotional_arc']
print(f"Arc Score: {emotional['arc_score']}/10")
print(f"Arc Shape: {emotional['arc_shape']}")
print(f"Peak Position: {emotional['climax_position']:.1%}")

# Keywords
keywords = result['features']['keyword_analysis']
print(f"Keywords Found: {keywords.get('total_keywords_found', 0)}")
print(f"Keyword Strength: {keywords['overall_keyword_strength']:.3f}")
```

### Custom Category

```python
# Force specific category
result = analyze_episode_v2(text, category="entrepreneurship")
```

## Model Characteristics

### Generous Scoring
- Average content scores 50-70/100
- Constructive feedback
- Fewer critical warnings
- Realistic expectations

### Category-Aware
- Different weights per category
- Finance emphasizes hooks & cliffhangers
- Career balances conflict & emotion
- Health prioritizes structure

### Multi-Signal Validation
- Combines semantic analysis + keywords
- Cross-validates features
- Detects inconsistencies
- More robust predictions

## Support

For issues or questions:
1. Check `FINAL_MODEL_SUMMARY.md` for detailed info
2. Review `MODEL_IMPROVEMENTS_V3.md` for technical details
3. See `KEYWORD_STRATEGY_GUIDE.md` for keyword tips

---

**Model Version**: V3 (Production Ready)
**Confidence**: 80%
**Last Updated**: March 6, 2026
