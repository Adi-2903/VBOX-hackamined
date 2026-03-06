# Metadata Usage Guide

## Critical: Using Hook and Cliffhanger Metadata

### The Problem

Previously, the ML pipeline was extracting hooks and cliffhangers from the story text itself, which led to:
- Inaccurate hook strength scores
- Incorrect cliffhanger analysis
- Poor model predictions
- Misalignment with actual content structure

### The Solution

The pipeline now accepts `hook` and `cliffhanger` as separate parameters, allowing you to pass the metadata directly from your content generation system.

---

## Updated API

### `analyze_episode_v2()` Function

```python
from ml_engine.ml_pipeline_v2 import analyze_episode_v2

result = analyze_episode_v2(
    text="Your story content here...",
    category="Relationships",  # Optional
    hook="Your episode hook here...",  # NEW: Pass hook metadata
    cliffhanger="Your cliffhanger here..."  # NEW: Pass cliffhanger metadata
)
```

### Parameters

- `text` (str, required): The main story content
- `category` (str, optional): Content category (auto-detected if not provided)
- `hook` (str, optional): Episode hook - if provided, analyzed separately from story
- `cliffhanger` (str, optional): Episode cliffhanger - if provided, analyzed separately from story

---

## JSON Format

Your content should follow this structure:

```json
{
  "category": "Relationships",
  "direction": "Tea Session Stories",
  "hook": "Main series hook",
  "episodes": [
    {
      "episode_number": 1,
      "title": "Episode Title",
      "hook": "Episode-specific hook",
      "story": "Main story content...",
      "cliffhanger": "Episode cliffhanger",
      "text_overlays_suggestions": ["#tag1", "#tag2"]
    }
  ]
}
```

---

## Usage Examples

### Example 1: With Metadata (Recommended)

```python
import json
from ml_engine.ml_pipeline_v2 import analyze_episode_v2

# Load your content
with open("episode_data.json") as f:
    data = json.load(f)

episode = data["episodes"][0]

# Analyze with metadata
result = analyze_episode_v2(
    text=episode["story"],
    category=data["category"],
    hook=episode["hook"],
    cliffhanger=episode["cliffhanger"]
)

print(f"Hook Strength: {result['features']['semantic_features']['hook_strength']}")
print(f"Cliffhanger Score: {result['cliffhanger']['cliffhanger_score']}/10")
```

### Example 2: Without Metadata (Fallback)

```python
# If you don't have separate metadata, the pipeline will extract from text
result = analyze_episode_v2(
    text="Your complete story with hook and cliffhanger embedded..."
)

# This works but is less accurate
```

---

## Test Scripts

### Using the New Test Script

```bash
# Test with test_output_5.json
python test_with_metadata.py test_output_5.json

# Test with test_output_2.json
python test_with_metadata.py test_output_2.json

# Test with test_output_3.json
python test_with_metadata.py test_output_3.json
```

### Updated test_v2_pipeline.py

The existing `test_v2_pipeline.py` has been updated to use metadata:

```python
result = analyze_episode_v2(
    episode["story"],
    hook=episode.get("hook"),
    cliffhanger=episode.get("cliffhanger")
)
```

---

## Why This Matters

### Accurate Hook Analysis

**Before (extracting from story):**
- Analyzed first 10-15% of story text
- Might miss the actual hook
- Could analyze setup instead of hook

**After (using metadata):**
- Analyzes the actual hook text
- More accurate hook strength scores
- Better alignment with content intent

### Accurate Cliffhanger Analysis

**Before (extracting from story):**
- Analyzed last 10-15% of story text
- Might include resolution instead of cliffhanger
- Could miss the actual cliffhanger

**After (using metadata):**
- Analyzes the actual cliffhanger text
- More accurate cliffhanger scores
- Better retention predictions

---

## Impact on Model Predictions

### Hook Strength
- More accurate scores (0.0 - 1.0)
- Better correlation with actual engagement
- Improved retention predictions

### Cliffhanger Score
- More accurate scores (0 - 10)
- Better prediction of episode-to-episode retention
- Improved recommendations

### Overall Score
- More reliable overall engagement scores
- Better identification of weak episodes
- More actionable recommendations

---

## Migration Guide

### If You're Using the Old API

**Old Code:**
```python
result = analyze_episode_v2(full_text_with_everything)
```

**New Code:**
```python
result = analyze_episode_v2(
    text=story_content,
    hook=hook_text,
    cliffhanger=cliffhanger_text
)
```

### If You Have Existing JSON Files

Your existing JSON files should already have the correct structure. Just update your code to pass the metadata:

```python
# Old way
result = analyze_episode_v2(episode["story"])

# New way
result = analyze_episode_v2(
    text=episode["story"],
    hook=episode.get("hook"),
    cliffhanger=episode.get("cliffhanger")
)
```

---

## Best Practices

1. **Always provide metadata when available**
   - Hook and cliffhanger should be separate from story
   - This ensures accurate analysis

2. **Keep metadata concise**
   - Hooks: 1-2 sentences
   - Cliffhangers: 1-2 sentences
   - Story: Main content

3. **Use consistent formatting**
   - Follow the JSON structure shown above
   - Include all required fields

4. **Test your content**
   - Use `test_with_metadata.py` to verify
   - Check hook and cliffhanger scores
   - Review recommendations

---

## Troubleshooting

### Low Hook Scores Despite Good Hook

**Problem:** Hook score is low even though you think the hook is strong.

**Solution:**
- Verify you're passing the hook parameter
- Check that hook text is not empty
- Ensure hook contains engaging elements (questions, tension, intrigue)

### Low Cliffhanger Scores

**Problem:** Cliffhanger score is low.

**Solution:**
- Verify you're passing the cliffhanger parameter
- Check that cliffhanger creates tension or unanswered questions
- Avoid generic "stay tuned" phrases

### Scores Don't Match Expectations

**Problem:** Scores seem off.

**Solution:**
- Verify you're using the new API with metadata
- Check that you're not passing the full text as hook/cliffhanger
- Review the analysis output to see what was analyzed

---

## Summary

✅ **DO:**
- Pass hook and cliffhanger as separate parameters
- Use the metadata from your JSON files
- Test with `test_with_metadata.py`

❌ **DON'T:**
- Extract hooks/cliffhangers from story text yourself
- Pass the full story as hook or cliffhanger
- Ignore the metadata fields in your JSON

---

*Last Updated: March 6, 2026*
*This is a critical change that significantly improves model accuracy*
