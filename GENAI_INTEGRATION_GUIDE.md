# GenAI Integration Guide - ML Scores & Recommendations

This guide helps GenAI developers build an LLM that uses ML model scores and recommendations to generate improved content.

## 🎯 Overview

The ML engine analyzes content and provides:
1. **Quantitative Scores**: Hook strength, conflict, cliffhanger, retention risk
2. **Qualitative Analysis**: Emotional arc, narrative structure, segment analysis
3. **Actionable Recommendations**: Specific improvement suggestions
4. **Weakness Identification**: What needs fixing

Your GenAI LLM will use these insights to:
- Rewrite weak sections
- Enhance hooks and cliffhangers
- Improve emotional progression
- Strengthen conflict and tension
- Generate category-specific improvements

## 📊 ML Model Output Format

### Complete Output Structure

```json
{
  "category": "crime",
  "features": {
    "semantic_features": {
      "hook_strength": 0.373,
      "hook_reason": "Moderate hook - some hook elements detected",
      "conflict_score": 0.331,
      "conflict_reason": "Low conflict - only 3/10 sentences show conflict",
      "cliffhanger_score": 0.377,
      "cliffhanger_reason": "Moderate surprise element"
    },
    "emotional_arc": {
      "emotion_variance": 0.156,
      "emotion_peak": 0.994,
      "climax_position": 0.65,
      "arc_shape": "RISING_ACTION",
      "reason": "Emotions build steadily with peak at 65% through story"
    },
    "narrative_structure": {
      "structure_quality": "GOOD",
      "hook_position_score": 0.85,
      "conflict_density": 0.45,
      "twist_position_score": 0.70,
      "resolution_absence_score": 0.60,
      "reason": "Well-structured with good hook placement and moderate conflict density"
    },
    "dropoff_prediction": {
      "overall_dropoff_risk": 0.45,
      "high_risk_segments": [2, 5],
      "segments": [
        {
          "label": "Opening (0-10s)",
          "start_pct": 0.0,
          "end_pct": 0.1,
          "dropoff_risk": 0.35,
          "engagement_score": 0.65,
          "reason": "Moderate hook strength keeps viewers engaged"
        },
        {
          "label": "Development (10-60s)",
          "start_pct": 0.1,
          "end_pct": 0.6,
          "dropoff_risk": 0.55,
          "engagement_score": 0.45,
          "reason": "Low conflict density may cause boredom"
        },
        {
          "label": "Climax (60-80s)",
          "start_pct": 0.6,
          "end_pct": 0.8,
          "dropoff_risk": 0.30,
          "engagement_score": 0.70,
          "reason": "Strong emotional peak maintains engagement"
        },
        {
          "label": "Resolution (80-100s)",
          "start_pct": 0.8,
          "end_pct": 1.0,
          "dropoff_risk": 0.50,
          "engagement_score": 0.50,
          "reason": "Moderate cliffhanger provides some tension"
        }
      ],
      "reason": "Segments 2 and 5 show elevated dropoff risk"
    },
    "keyword_analysis": {
      "category": "crime",
      "hook_keywords": {
        "keywords_found": ["mystery", "shocking"],
        "density": 0.15,
        "coverage": 0.20
      },
      "conflict_keywords": {
        "keywords_found": ["danger", "threat"],
        "density": 0.10,
        "coverage": 0.15
      },
      "resolution_keywords": {
        "keywords_found": [],
        "density": 0.0,
        "coverage": 0.0
      }
    }
  },
  "retention": {
    "risk_score": 0.644,
    "risk_level": "MEDIUM",
    "segment_risks": {
      "Opening (0-10s)": {"risk": 0.35, "label": "LOW"},
      "Development (10-60s)": {"risk": 0.55, "label": "MEDIUM"},
      "Climax (60-80s)": {"risk": 0.30, "label": "LOW"},
      "Resolution (80-100s)": {"risk": 0.50, "label": "MEDIUM"}
    },
    "reason": "Moderate retention risk. Areas to improve: Flat emotional arc - limited engagement",
    "recommendations": [
      {
        "area": "Emotional Arc",
        "priority": "MEDIUM",
        "suggestion": "Add more emotional variety - mix fear, surprise, anger to create dynamic progression"
      },
      {
        "area": "Story Structure",
        "priority": "MEDIUM",
        "suggestion": "Position the emotional peak between 50-80% of the story for optimal impact"
      },
      {
        "area": "Ending Resolution",
        "priority": "MEDIUM",
        "suggestion": "Avoid neat resolutions - leave some questions unanswered to maintain tension"
      }
    ]
  },
  "cliffhanger": {
    "cliffhanger_score": 2.5,
    "strength": "MODERATE",
    "components": {
      "surprise": 0.377,
      "emotion_spike": 0.15,
      "conflict_signal": 0.40,
      "keyword_boost": 1.05
    },
    "category": "crime",
    "keywords_found": {
      "hook": ["mystery", "shocking"],
      "conflict": ["danger", "threat"],
      "resolution": []
    },
    "reason": "Moderate surprise element; emotional intensity spikes at the end; some tension in closing"
  },
  "summary": {
    "overall_score": 32.6,
    "engagement_level": "FAIR",
    "key_strengths": ["Dynamic emotional arc"],
    "key_weaknesses": ["Flat emotional arc", "Weak cliffhanger"]
  }
}
```

## 🎨 Evaluation Metrics Explained

### 1. Overall Score (0-100)
- **70-100**: EXCELLENT - High-quality, engaging content
- **45-70**: GOOD - Solid content, minor improvements needed
- **30-45**: FAIR - Needs improvement in key areas
- **0-30**: POOR - Significant engagement issues

**Use for**: Overall quality assessment, prioritizing rewrites

### 2. Hook Strength (0-1)
- **0.55+**: Strong hook - compelling opening
- **0.30-0.55**: Moderate hook - some interest
- **<0.30**: Weak hook - needs immediate attention

**Use for**: Rewriting opening sentences, adding mystery/shock

### 3. Conflict Score (0-1)
- **0.50+**: Good conflict - engaging tension
- **0.25-0.50**: Moderate conflict - needs enhancement
- **<0.25**: Low conflict - critical issue

**Use for**: Adding obstacles, opposition, stakes

### 4. Cliffhanger Score (0-10)
- **5.0+**: STRONG - compelling ending
- **2.5-5.0**: MODERATE - some tension
- **<2.5**: WEAK - needs major improvement

**Use for**: Rewriting endings, adding unresolved tension

### 5. Retention Risk (0-1)
- **<0.45**: LOW - strong engagement
- **0.45-0.70**: MEDIUM - moderate engagement
- **>0.70**: HIGH - high dropoff risk

**Use for**: Identifying critical sections to rewrite

### 6. Emotional Arc Metrics
- **emotion_variance**: Higher = more dynamic (target: >0.30)
- **emotion_peak**: Intensity of climax (target: >0.70)
- **climax_position**: Where peak occurs (target: 0.50-0.80)

**Use for**: Adjusting emotional pacing, adding variety

### 7. Segment Dropoff Risk
Each segment has:
- **dropoff_risk**: 0-1 (higher = more likely to lose viewers)
- **engagement_score**: 0-1 (higher = more engaging)
- **reason**: Why this segment is risky

**Use for**: Targeted rewrites of specific sections

## 🤖 LLM Prompt Engineering Guide

### Prompt Template Structure

```python
def generate_improvement_prompt(original_text: str, ml_analysis: dict) -> str:
    """
    Generate LLM prompt using ML analysis
    """
    
    summary = ml_analysis['summary']
    retention = ml_analysis['retention']
    cliffhanger = ml_analysis['cliffhanger']
    features = ml_analysis['features']
    
    prompt = f"""You are an expert content writer specializing in {ml_analysis['category']} stories.

ORIGINAL CONTENT:
{original_text}

ML ANALYSIS RESULTS:
- Overall Score: {summary['overall_score']}/100 ({summary['engagement_level']})
- Retention Risk: {retention['risk_level']} ({retention['risk_score']:.2f})
- Hook Strength: {features['semantic_features']['hook_strength']:.2f}
- Conflict Score: {features['semantic_features']['conflict_score']:.2f}
- Cliffhanger: {cliffhanger['cliffhanger_score']}/10 ({cliffhanger['strength']})

KEY WEAKNESSES:
{chr(10).join(f"- {w}" for w in summary['key_weaknesses'])}

SPECIFIC ISSUES:
{chr(10).join(f"- {r['area']}: {r['suggestion']}" for r in retention['recommendations'][:3])}

HIGH-RISK SEGMENTS:
{_format_high_risk_segments(features['dropoff_prediction'])}

YOUR TASK:
Rewrite the content to address these issues while maintaining the core story.

REQUIREMENTS:
1. Strengthen the opening hook (current: {features['semantic_features']['hook_strength']:.2f}, target: >0.55)
2. Increase conflict and tension (current: {features['semantic_features']['conflict_score']:.2f}, target: >0.50)
3. Improve the cliffhanger ending (current: {cliffhanger['cliffhanger_score']}/10, target: >5.0)
4. Add emotional variety (current variance: {features['emotional_arc']['emotion_variance']:.2f}, target: >0.30)
5. Focus on high-risk segments: {', '.join(map(str, features['dropoff_prediction']['high_risk_segments']))}

CATEGORY-SPECIFIC KEYWORDS TO INCLUDE:
{_format_keywords(cliffhanger.get('keywords_found', {}))}

OUTPUT FORMAT:
Provide the rewritten content that addresses all issues above.
"""
    
    return prompt
```

### Example Prompts by Issue Type

#### 1. Weak Hook (score < 0.30)
```
ISSUE: Weak opening hook (score: 0.25)
CURRENT: "It was a normal Tuesday morning. John went to work as usual."

IMPROVE BY:
- Start with immediate conflict or mystery
- Use shocking revelation or unexpected event
- Create curiosity gap
- Add sensory details for immersion

EXAMPLE IMPROVEMENT:
"John's phone buzzed with a photo of his daughter - tied to a chair in a dark room. She was supposed to be at school."
```

#### 2. Low Conflict (score < 0.25)
```
ISSUE: Insufficient conflict (score: 0.20)
CURRENT CONFLICT DENSITY: 20% of sentences show conflict

IMPROVE BY:
- Add obstacles every 2-3 sentences
- Introduce opposition or antagonist
- Raise stakes progressively
- Create time pressure
- Add internal conflict

TECHNIQUES:
- "But then..." transitions
- Unexpected complications
- Character opposition
- Environmental challenges
```

#### 3. Weak Cliffhanger (score < 2.5)
```
ISSUE: Weak cliffhanger (score: 1.5)
CURRENT: "Eventually, they found some clues that might help."

IMPROVE BY:
- End with unresolved question
- Introduce new threat at the end
- Create impossible choice
- Reveal shocking information
- Leave outcome uncertain

EXAMPLE IMPROVEMENT:
"The clue led to an address - John's own house. And inside, the lights were on."
```

#### 4. Flat Emotional Arc (variance < 0.15)
```
ISSUE: Flat emotional arc (variance: 0.12)
CURRENT: Mostly neutral/sad emotions throughout

IMPROVE BY:
- Mix emotions: joy → fear → anger → surprise
- Create emotional peaks and valleys
- Use contrast (hope then despair)
- Build to emotional climax at 60-80%

EMOTION SEQUENCE EXAMPLE:
1. Joy/excitement (opening)
2. Fear/anxiety (complication)
3. Anger/frustration (conflict)
4. Surprise/shock (twist)
5. Hope/determination (ending)
```

## 📝 Sample LLM Integration Code

### Python Example with OpenAI

```python
import openai
from ml_engine.ml_pipeline_v2 import analyze_episode_v2

def improve_content_with_llm(original_text: str, category: str = None):
    """
    Use ML analysis to guide LLM content improvement
    """
    
    # Step 1: Analyze with ML model
    ml_analysis = analyze_episode_v2(original_text, category)
    
    # Step 2: Check if improvement needed
    if ml_analysis['summary']['overall_score'] >= 70:
        return {
            'improved': False,
            'reason': 'Content already excellent',
            'original': original_text,
            'analysis': ml_analysis
        }
    
    # Step 3: Generate improvement prompt
    prompt = generate_improvement_prompt(original_text, ml_analysis)
    
    # Step 4: Call LLM
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an expert content writer who improves episodic content based on ML analysis."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    improved_text = response.choices[0].message.content
    
    # Step 5: Re-analyze improved content
    improved_analysis = analyze_episode_v2(improved_text, category)
    
    # Step 6: Compare scores
    improvement = {
        'improved': True,
        'original_text': original_text,
        'improved_text': improved_text,
        'original_analysis': ml_analysis,
        'improved_analysis': improved_analysis,
        'score_improvement': {
            'overall': improved_analysis['summary']['overall_score'] - ml_analysis['summary']['overall_score'],
            'hook': improved_analysis['features']['semantic_features']['hook_strength'] - ml_analysis['features']['semantic_features']['hook_strength'],
            'conflict': improved_analysis['features']['semantic_features']['conflict_score'] - ml_analysis['features']['semantic_features']['conflict_score'],
            'cliffhanger': improved_analysis['cliffhanger']['cliffhanger_score'] - ml_analysis['cliffhanger']['cliffhanger_score']
        }
    }
    
    return improvement


def iterative_improvement(text: str, category: str = None, max_iterations: int = 3):
    """
    Iteratively improve content until target score reached
    """
    
    current_text = text
    iterations = []
    
    for i in range(max_iterations):
        result = improve_content_with_llm(current_text, category)
        iterations.append(result)
        
        if not result['improved']:
            break
        
        current_score = result['improved_analysis']['summary']['overall_score']
        
        if current_score >= 70:  # Target score
            break
        
        current_text = result['improved_text']
    
    return {
        'final_text': current_text,
        'iterations': iterations,
        'total_improvement': iterations[-1]['improved_analysis']['summary']['overall_score'] - iterations[0]['original_analysis']['summary']['overall_score']
    }
```

### Example with Anthropic Claude

```python
import anthropic
from ml_engine.ml_pipeline_v2 import analyze_episode_v2

def improve_with_claude(original_text: str, category: str = None):
    """
    Use Claude to improve content based on ML analysis
    """
    
    ml_analysis = analyze_episode_v2(original_text, category)
    
    client = anthropic.Anthropic(api_key="your-api-key")
    
    prompt = generate_improvement_prompt(original_text, ml_analysis)
    
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    improved_text = message.content[0].text
    
    # Re-analyze
    improved_analysis = analyze_episode_v2(improved_text, category)
    
    return {
        'original': original_text,
        'improved': improved_text,
        'original_score': ml_analysis['summary']['overall_score'],
        'improved_score': improved_analysis['summary']['overall_score'],
        'improvement': improved_analysis['summary']['overall_score'] - ml_analysis['summary']['overall_score']
    }
```

## 🎯 Targeted Improvement Strategies

### Strategy 1: Segment-Based Rewriting

```python
def improve_high_risk_segments(text: str, ml_analysis: dict):
    """
    Rewrite only high-risk segments
    """
    
    segments = ml_analysis['features']['dropoff_prediction']['segments']
    high_risk = [s for s in segments if s['dropoff_risk'] > 0.6]
    
    sentences = text.split('.')
    total_sentences = len(sentences)
    
    improvements = []
    
    for segment in high_risk:
        start_idx = int(segment['start_pct'] * total_sentences)
        end_idx = int(segment['end_pct'] * total_sentences)
        
        segment_text = '.'.join(sentences[start_idx:end_idx])
        
        prompt = f"""
        SEGMENT: {segment['label']}
        ISSUE: {segment['reason']}
        DROPOFF RISK: {segment['dropoff_risk']:.2f}
        
        CURRENT TEXT:
        {segment_text}
        
        Rewrite this segment to reduce dropoff risk by addressing: {segment['reason']}
        """
        
        # Call LLM for this segment
        improved_segment = call_llm(prompt)
        
        improvements.append({
            'segment': segment['label'],
            'original': segment_text,
            'improved': improved_segment
        })
    
    return improvements
```

### Strategy 2: Recommendation-Driven Rewriting

```python
def apply_recommendations(text: str, ml_analysis: dict):
    """
    Apply each recommendation sequentially
    """
    
    current_text = text
    
    for rec in ml_analysis['retention']['recommendations']:
        if rec['priority'] == 'CRITICAL':
            prompt = f"""
            CURRENT TEXT:
            {current_text}
            
            CRITICAL ISSUE: {rec['area']}
            RECOMMENDATION: {rec['suggestion']}
            
            Rewrite the text to address this specific issue.
            """
            
            current_text = call_llm(prompt)
    
    return current_text
```

### Strategy 3: Category-Specific Enhancement

```python
def enhance_with_keywords(text: str, ml_analysis: dict):
    """
    Add category-specific keywords
    """
    
    category = ml_analysis['category']
    keywords = ml_analysis['features']['keyword_analysis']
    
    missing_keywords = {
        'hook': [k for k in get_category_keywords(category, 'hook') 
                if k not in keywords['hook_keywords']['keywords_found']],
        'conflict': [k for k in get_category_keywords(category, 'conflict')
                    if k not in keywords['conflict_keywords']['keywords_found']]
    }
    
    prompt = f"""
    CATEGORY: {category}
    CURRENT TEXT: {text}
    
    MISSING KEYWORDS:
    - Hook keywords: {', '.join(missing_keywords['hook'][:5])}
    - Conflict keywords: {', '.join(missing_keywords['conflict'][:5])}
    
    Rewrite to naturally incorporate these keywords while maintaining story flow.
    """
    
    return call_llm(prompt)
```

## 📊 Evaluation & Comparison

### Before/After Comparison Template

```python
def generate_comparison_report(original_text: str, improved_text: str, category: str = None):
    """
    Generate detailed before/after comparison
    """
    
    original_analysis = analyze_episode_v2(original_text, category)
    improved_analysis = analyze_episode_v2(improved_text, category)
    
    report = {
        'overall_improvement': {
            'score': {
                'before': original_analysis['summary']['overall_score'],
                'after': improved_analysis['summary']['overall_score'],
                'change': improved_analysis['summary']['overall_score'] - original_analysis['summary']['overall_score']
            },
            'engagement': {
                'before': original_analysis['summary']['engagement_level'],
                'after': improved_analysis['summary']['engagement_level']
            }
        },
        'metric_improvements': {
            'hook_strength': {
                'before': original_analysis['features']['semantic_features']['hook_strength'],
                'after': improved_analysis['features']['semantic_features']['hook_strength'],
                'change': improved_analysis['features']['semantic_features']['hook_strength'] - original_analysis['features']['semantic_features']['hook_strength']
            },
            'conflict_score': {
                'before': original_analysis['features']['semantic_features']['conflict_score'],
                'after': improved_analysis['features']['semantic_features']['conflict_score'],
                'change': improved_analysis['features']['semantic_features']['conflict_score'] - original_analysis['features']['semantic_features']['conflict_score']
            },
            'cliffhanger': {
                'before': original_analysis['cliffhanger']['cliffhanger_score'],
                'after': improved_analysis['cliffhanger']['cliffhanger_score'],
                'change': improved_analysis['cliffhanger']['cliffhanger_score'] - original_analysis['cliffhanger']['cliffhanger_score']
            },
            'retention_risk': {
                'before': original_analysis['retention']['risk_score'],
                'after': improved_analysis['retention']['risk_score'],
                'change': original_analysis['retention']['risk_score'] - improved_analysis['retention']['risk_score']  # Lower is better
            }
        },
        'weaknesses_fixed': {
            'before': original_analysis['summary']['key_weaknesses'],
            'after': improved_analysis['summary']['key_weaknesses'],
            'fixed': list(set(original_analysis['summary']['key_weaknesses']) - set(improved_analysis['summary']['key_weaknesses']))
        },
        'strengths_gained': {
            'before': original_analysis['summary']['key_strengths'],
            'after': improved_analysis['summary']['key_strengths'],
            'new': list(set(improved_analysis['summary']['key_strengths']) - set(original_analysis['summary']['key_strengths']))
        }
    }
    
    return report
```

## 🎓 Best Practices

### 1. Always Re-Analyze After Improvement
```python
# ✅ GOOD
improved_text = llm_improve(text, analysis)
new_analysis = analyze_episode_v2(improved_text)
if new_analysis['summary']['overall_score'] > analysis['summary']['overall_score']:
    return improved_text

# ❌ BAD
improved_text = llm_improve(text, analysis)
return improved_text  # No verification!
```

### 2. Use Iterative Improvement
```python
# Improve in multiple passes for better results
for i in range(3):
    analysis = analyze_episode_v2(text)
    if analysis['summary']['overall_score'] >= 70:
        break
    text = llm_improve(text, analysis)
```

### 3. Prioritize Critical Issues
```python
# Focus on CRITICAL recommendations first
critical_recs = [r for r in analysis['retention']['recommendations'] 
                 if r['priority'] == 'CRITICAL']
for rec in critical_recs:
    text = apply_recommendation(text, rec)
```

### 4. Preserve Core Story
```python
# Include in prompt:
"Maintain the core story, characters, and plot points. 
Only improve engagement, pacing, and emotional impact."
```

## 📈 Success Metrics

Track these metrics to evaluate your LLM:

1. **Score Improvement**: Average increase in overall_score
2. **Hook Success Rate**: % of rewrites with hook_strength > 0.55
3. **Cliffhanger Success**: % of rewrites with cliffhanger > 5.0
4. **Retention Improvement**: Average decrease in risk_score
5. **Iteration Efficiency**: Average iterations needed to reach target

## 🔗 Integration Workflow

```
1. Content Creation
   ↓
2. ML Analysis (analyze_episode_v2)
   ↓
3. Check Score
   ├─ Score ≥ 70 → Publish
   └─ Score < 70 → Continue
       ↓
4. Generate LLM Prompt (with ML insights)
   ↓
5. LLM Improvement
   ↓
6. Re-Analyze (verify improvement)
   ↓
7. Compare Scores
   ├─ Improved → Accept
   └─ Not Improved → Retry or Manual Review
```

## 📞 Support

- **ML Team**: [Your contact]
- **Sample Code**: See examples above
- **ML Output**: Run `python examples/analyze_content.py` for sample output
- **Questions**: Create GitHub issue

---

**Ready to build your GenAI LLM!** 🚀

Use the ML scores and recommendations to guide intelligent content improvement.
