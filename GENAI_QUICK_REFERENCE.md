# GenAI Quick Reference Card

Quick reference for using ML scores to improve content with LLM.

## 🎯 Key Metrics at a Glance

| Metric | Range | Target | Use For |
|--------|-------|--------|---------|
| **Overall Score** | 0-100 | 70+ | Overall quality assessment |
| **Hook Strength** | 0-1 | 0.55+ | Opening sentence rewrite |
| **Conflict Score** | 0-1 | 0.50+ | Adding tension/obstacles |
| **Cliffhanger** | 0-10 | 5.0+ | Ending rewrite |
| **Retention Risk** | 0-1 | <0.45 | Identifying critical issues |
| **Emotion Variance** | 0-1 | 0.30+ | Emotional pacing |

## 🚨 Priority Matrix

### CRITICAL (Fix Immediately)
- ❌ Hook Strength < 0.30
- ❌ Cliffhanger < 2.5
- ❌ Retention Risk > 0.70
- ❌ Overall Score < 30

### HIGH (Fix Soon)
- ⚠️ Conflict Score < 0.25
- ⚠️ Hook Strength < 0.40
- ⚠️ Segment Dropoff > 0.65

### MEDIUM (Improve)
- 📝 Emotion Variance < 0.15
- 📝 Cliffhanger < 5.0
- 📝 Overall Score < 45

## 💡 Quick Fixes by Issue

### Weak Hook (< 0.30)
```
❌ "It was a normal Tuesday morning."
✅ "The photo showed my daughter tied to a chair. She was supposed to be at school."

Techniques:
- Start with conflict/mystery
- Use shocking revelation
- Create immediate curiosity
- Add sensory details
```

### Low Conflict (< 0.25)
```
❌ "She went to the store. She bought groceries."
✅ "She rushed to the store, but it was closing. The clerk refused to let her in, even though she begged."

Techniques:
- Add obstacles every 2-3 sentences
- Introduce opposition
- Raise stakes
- Create time pressure
```

### Weak Cliffhanger (< 2.5)
```
❌ "Eventually, they found some clues."
✅ "The clue led to an address - her own house. Inside, the lights were on."

Techniques:
- End with unresolved question
- Introduce new threat
- Create impossible choice
- Reveal shocking info
```

### Flat Emotions (< 0.15)
```
❌ All neutral/sad throughout
✅ Joy → Fear → Anger → Surprise → Hope

Techniques:
- Mix 3+ different emotions
- Create emotional peaks/valleys
- Use contrast (hope then despair)
- Build to climax at 60-80%
```

## 📊 Segment Analysis

| Segment | Position | High Risk If | Fix By |
|---------|----------|--------------|--------|
| Opening | 0-10% | Risk > 0.60 | Stronger hook |
| Development | 10-60% | Risk > 0.55 | More conflict |
| Climax | 60-80% | Risk > 0.50 | Emotional peak |
| Resolution | 80-100% | Risk > 0.50 | Better cliffhanger |

## 🎨 LLM Prompt Template

```python
f"""Rewrite this {category} story to improve engagement.

CURRENT SCORES:
- Overall: {score}/100 (Target: 70+)
- Hook: {hook:.2f} (Target: 0.55+)
- Conflict: {conflict:.2f} (Target: 0.50+)
- Cliffhanger: {cliff}/10 (Target: 5.0+)

ISSUES TO FIX:
{weaknesses}

SPECIFIC RECOMMENDATIONS:
{recommendations}

REQUIREMENTS:
1. Strengthen opening (current: {hook:.2f})
2. Add more conflict (current: {conflict:.2f})
3. Improve ending (current: {cliff}/10)
4. Increase emotional variety

Rewrite while maintaining core story:
{original_text}
"""
```

## 🔄 Improvement Workflow

```
1. Analyze → Get ML scores
   ↓
2. Check → Score < 70?
   ↓ Yes
3. Identify → Find critical issues
   ↓
4. Prompt → Generate LLM prompt with scores
   ↓
5. Improve → LLM rewrites content
   ↓
6. Re-analyze → Get new scores
   ↓
7. Compare → Improved?
   ├─ Yes → Accept
   └─ No → Retry with different approach
```

## 📈 Success Criteria

| Metric | Before | After | Success |
|--------|--------|-------|---------|
| Overall Score | <45 | 70+ | ✅ |
| Hook Strength | <0.40 | 0.55+ | ✅ |
| Conflict Score | <0.35 | 0.50+ | ✅ |
| Cliffhanger | <3.0 | 5.0+ | ✅ |
| Retention Risk | >0.60 | <0.45 | ✅ |

## 🎯 Category-Specific Keywords

### Crime
**Hook**: murder, detective, mystery, crime, investigation, suspect, victim, evidence
**Conflict**: danger, threat, chase, escape, trap, weapon, attack, confrontation

### Romance
**Hook**: love, heart, attraction, desire, passion, connection, chemistry
**Conflict**: jealousy, betrayal, misunderstanding, distance, obstacle, choice

### Horror
**Hook**: fear, terror, darkness, shadow, scream, blood, death
**Conflict**: monster, creature, haunted, possessed, trapped, hunted, nightmare

### Thriller
**Hook**: conspiracy, secret, betrayal, danger, threat, mystery
**Conflict**: chase, escape, trap, deadline, bomb, hostage, assassin

## 🔍 Quick Diagnosis

```python
def diagnose(analysis):
    issues = []
    
    if analysis['summary']['overall_score'] < 30:
        issues.append("CRITICAL: Overall quality very poor")
    
    if analysis['features']['semantic_features']['hook_strength'] < 0.30:
        issues.append("CRITICAL: Weak opening hook")
    
    if analysis['cliffhanger']['cliffhanger_score'] < 2.5:
        issues.append("CRITICAL: Weak cliffhanger")
    
    if analysis['retention']['risk_score'] > 0.70:
        issues.append("CRITICAL: High retention risk")
    
    if analysis['features']['semantic_features']['conflict_score'] < 0.25:
        issues.append("HIGH: Insufficient conflict")
    
    if analysis['features']['emotional_arc']['emotion_variance'] < 0.15:
        issues.append("MEDIUM: Flat emotional arc")
    
    return issues
```

## 📝 Example Improvements

### Example 1: Weak Hook → Strong Hook

**Before** (Hook: 0.25):
```
"It was a normal Tuesday morning. John went to work as usual."
```

**After** (Hook: 0.78):
```
"John's phone buzzed with a photo of his daughter - tied to a chair in a dark room. She was supposed to be at school."
```

**Improvement**: +0.53 hook strength

### Example 2: Low Conflict → High Conflict

**Before** (Conflict: 0.20):
```
"She walked to the store. She bought some items. She went home."
```

**After** (Conflict: 0.65):
```
"She raced to the store, but the doors were locked. The clerk inside shook his head. She pounded on the glass - she needed that medicine now, or her son would die."
```

**Improvement**: +0.45 conflict score

### Example 3: Weak Cliffhanger → Strong Cliffhanger

**Before** (Cliffhanger: 1.8):
```
"They eventually found some clues that might help solve the case."
```

**After** (Cliffhanger: 7.2):
```
"The final clue led to an address - John's own house. Through the window, he saw a figure standing over his sleeping wife. His phone was dead. He was 10 minutes away."
```

**Improvement**: +5.4 cliffhanger score

## 🎓 Best Practices

1. ✅ **Always re-analyze** after improvement
2. ✅ **Focus on critical issues** first
3. ✅ **Preserve core story** and characters
4. ✅ **Use iterative improvement** (2-3 passes)
5. ✅ **Track score changes** to measure success
6. ❌ **Don't change category** or main plot
7. ❌ **Don't add unnecessary length**
8. ❌ **Don't over-complicate** the story

## 📞 Quick Help

- **Full Guide**: `GENAI_INTEGRATION_GUIDE.md`
- **Sample Outputs**: `genai_sample_outputs.json`
- **ML Analysis**: `python examples/analyze_content.py <file>`
- **Questions**: Contact ML team

---

**Keep this card handy while building your LLM!** 📌
