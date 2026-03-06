# Training Pipeline

This directory contains scripts for training and evaluating the retention prediction models.

## Quick Start

### 1. Prepare Training Data

When you receive GenAI-generated data, prepare it for training:

```bash
python training/prepare_training_data.py genai_data.json
```

Expected input format:
```json
{
  "episodes": [
    {
      "story": "Episode text content...",
      "category": "crime",
      "labels": {
        "hook_strength": 0.8,
        "conflict_score": 0.7,
        "cliffhanger_score": 0.9,
        "retention_risk": 0.3,
        "overall_quality": 75
      }
    }
  ]
}
```

This will create:
- `training/data/training_data.csv`
- `training/data/training_data.json`

### 2. Train Models (Future)

Once you have sufficient training data, you can train ML models:

```bash
# Train XGBoost models (when implemented)
python training/train_models.py

# Evaluate models
python training/evaluate_models.py
```

## Current Pipeline (Heuristic-Based)

The current system uses heuristic-based scoring:

1. **Semantic Analysis**: Embedding-based similarity to hook/conflict/cliffhanger concepts
2. **Emotional Arc**: Emotion classification and intensity tracking
3. **Narrative Structure**: Story structure analysis
4. **Keyword Detection**: Category-specific keyword boosting

## Future Improvements

With training data, you can:

1. Train supervised models (XGBoost, Neural Networks)
2. Fine-tune embedding models for better semantic understanding
3. Learn optimal weight combinations
4. Improve category-specific predictions

## Data Requirements

For effective training:
- Minimum 500-1000 labeled episodes
- Diverse categories (crime, romance, horror, etc.)
- Balanced quality distribution (good and bad examples)
- Human-validated labels for accuracy
