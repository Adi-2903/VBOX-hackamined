# Backend Integration Guide - ML Retention Engine

This guide helps backend developers integrate the ML retention prediction engine into their API/service.

## 📦 Repository Structure

```
retention-ml-engine/
├── ml_engine/                          # Core ML engine (DO NOT MODIFY)
│   ├── __init__.py
│   ├── ml_pipeline_v2.py               # Main analysis pipeline
│   ├── retention_model_v3.py           # Retention risk prediction
│   ├── cliffhanger_model.py            # Cliffhanger scoring
│   ├── semantic_analyzer.py            # Semantic feature extraction
│   ├── emotional_arc_analyzer.py       # Emotional arc analysis
│   ├── narrative_structure_analyzer.py # Story structure analysis
│   ├── dropoff_predictor.py            # Segment dropoff prediction
│   ├── keyword_detector.py             # Keyword detection
│   ├── feature_extractor_v2.py         # Feature engineering
│   ├── emotion_model.py                # Emotion classification
│   ├── embedding_model.py              # Sentence embeddings
│   ├── text_processor.py               # Text preprocessing
│   ├── genai_pipeline.py               # GenAI format adapter
│   └── input_adapter.py                # Input format handling
├── training/                           # Training scripts (future use)
│   ├── prepare_training_data.py
│   └── README.md
├── tests/                              # Test files
│   ├── test_v2_pipeline.py
│   ├── test_with_fake_data.py
│   └── test_emotion_model.py
├── examples/                           # Example files
│   ├── example_story.txt
│   └── analyze_content.py
├── docs/                               # Documentation
│   ├── README.md
│   ├── IMPROVEMENTS_SUMMARY.md
│   └── READY_FOR_TRAINING.md
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore file
└── setup.py                            # Package setup (optional)
```

## 🚀 Quick Start for Backend Integration

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd retention-ml-engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

```python
from ml_engine.ml_pipeline_v2 import analyze_episode_v2

# Analyze episode content
text = "Your episode story content here..."
result = analyze_episode_v2(text, category="crime")

# Access results
print(f"Overall Score: {result['summary']['overall_score']}/100")
print(f"Retention Risk: {result['retention']['risk_level']}")
print(f"Cliffhanger: {result['cliffhanger']['cliffhanger_score']}/10")
```

## 📡 API Integration Examples

### REST API Example (Flask)

```python
from flask import Flask, request, jsonify
from ml_engine.ml_pipeline_v2 import analyze_episode_v2

app = Flask(__name__)

@app.route('/api/analyze', methods=['POST'])
def analyze_content():
    """
    Analyze episode content
    
    Request Body:
    {
        "text": "Episode content...",
        "category": "crime"  // optional
    }
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        category = data.get('category')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Run analysis
        result = analyze_episode_v2(text, category)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### FastAPI Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ml_engine.ml_pipeline_v2 import analyze_episode_v2

app = FastAPI()

class AnalysisRequest(BaseModel):
    text: str
    category: str = None

class AnalysisResponse(BaseModel):
    success: bool
    data: dict = None
    error: str = None

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_content(request: AnalysisRequest):
    """Analyze episode content for retention prediction"""
    try:
        result = analyze_episode_v2(request.text, request.category)
        return AnalysisResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 📥 Input Format

### Simple Text Input
```python
text = "Your episode story content..."
result = analyze_episode_v2(text)
```

### With Category
```python
result = analyze_episode_v2(text, category="crime")
# Supported categories: crime, romance, horror, thriller, drama, comedy
```

### GenAI Format
```python
from ml_engine.genai_pipeline import analyze_genai_episode

episode_data = {
    "title": "Episode 1",
    "story": "Story content...",
    "hook": "Opening hook...",
    "category": "crime"
}

result = analyze_genai_episode(episode_data)
```

## 📤 Output Format

```json
{
  "category": "crime",
  "features": {
    "semantic_features": {
      "hook_strength": 0.373,
      "conflict_score": 0.331,
      "cliffhanger_score": 0.377,
      "hook_reason": "...",
      "conflict_reason": "...",
      "cliffhanger_reason": "..."
    },
    "emotional_arc": {
      "emotion_variance": 0.156,
      "emotion_peak": 0.994,
      "climax_position": 0.65,
      "arc_shape": "RISING_ACTION",
      "reason": "..."
    },
    "narrative_structure": {
      "structure_quality": "GOOD",
      "hook_position_score": 0.85,
      "conflict_density": 0.45,
      "twist_position_score": 0.70,
      "reason": "..."
    },
    "dropoff_prediction": {
      "overall_dropoff_risk": 0.45,
      "high_risk_segments": [2, 5],
      "segments": [
        {
          "label": "Opening (0-10s)",
          "dropoff_risk": 0.35,
          "engagement_score": 0.65
        }
      ],
      "reason": "..."
    }
  },
  "retention": {
    "risk_score": 0.644,
    "risk_level": "MEDIUM",
    "segment_risks": {
      "Opening (0-10s)": {"risk": 0.35, "label": "LOW"},
      "Development (10-60s)": {"risk": 0.55, "label": "MEDIUM"}
    },
    "reason": "Moderate retention risk. Areas to improve: ...",
    "recommendations": [
      {
        "area": "Opening Hook",
        "priority": "CRITICAL",
        "suggestion": "Start with a shocking revelation..."
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
    "reason": "Moderate surprise element; emotional intensity spikes at the end"
  },
  "summary": {
    "overall_score": 32.6,
    "engagement_level": "FAIR",
    "key_strengths": ["Dynamic emotional arc"],
    "key_weaknesses": ["Weak cliffhanger"]
  }
}
```

## 🔑 Key Metrics Explained

### Overall Score (0-100)
- **70+**: EXCELLENT - High-quality, engaging content
- **45-70**: GOOD - Solid content, minor improvements
- **30-45**: FAIR - Needs improvement in key areas
- **<30**: POOR - Significant engagement issues

### Retention Risk (0-1)
- **<0.45**: LOW - Strong engagement, low dropoff risk
- **0.45-0.70**: MEDIUM - Moderate engagement, some improvements needed
- **>0.70**: HIGH - High dropoff risk, critical issues

### Cliffhanger Score (0-10)
- **5.0+**: STRONG - Compelling ending, drives continuation
- **2.5-5.0**: MODERATE - Some tension, room for improvement
- **<2.5**: WEAK - Predictable, low motivation to continue

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ML engine
COPY ml_engine/ ./ml_engine/

# Copy API code
COPY api.py .

# Expose port
EXPOSE 8000

# Run API
CMD ["python", "api.py"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  ml-engine:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_CACHE_DIR=/app/cache
    volumes:
      - model-cache:/app/cache
    restart: unless-stopped

volumes:
  model-cache:
```

## ⚡ Performance Considerations

### Response Times
- **First request**: ~3-5 seconds (model loading)
- **Subsequent requests**: ~50-200ms per episode
- **Batch processing**: ~30-50ms per episode

### Memory Usage
- **Base**: ~500MB (models loaded)
- **Per request**: ~10-20MB
- **Recommended**: 2GB RAM minimum

### Optimization Tips

1. **Model Caching**: Models are loaded once and cached
```python
# Models auto-cache on first use
# No manual caching needed
```

2. **Batch Processing**:
```python
from ml_engine.ml_pipeline_v2 import analyze_series_v2

episodes = ["Episode 1 text...", "Episode 2 text...", ...]
results = analyze_series_v2(episodes)
```

3. **Async Processing**:
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

async def analyze_async(text, category=None):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor, 
        analyze_episode_v2, 
        text, 
        category
    )
```

## 🔒 Security Considerations

1. **Input Validation**:
```python
def validate_input(text, max_length=10000):
    if not text or not isinstance(text, str):
        raise ValueError("Text must be a non-empty string")
    if len(text) > max_length:
        raise ValueError(f"Text exceeds maximum length of {max_length}")
    return text.strip()
```

2. **Rate Limiting**: Implement rate limiting on your API
3. **Authentication**: Add API key authentication
4. **Input Sanitization**: Sanitize text input to prevent injection

## 📊 Monitoring & Logging

```python
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_with_logging(text, category=None):
    start_time = time.time()
    
    try:
        logger.info(f"Starting analysis - Category: {category}, Length: {len(text)}")
        result = analyze_episode_v2(text, category)
        
        duration = time.time() - start_time
        logger.info(f"Analysis complete - Duration: {duration:.2f}s, Score: {result['summary']['overall_score']}")
        
        return result
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_v2_pipeline.py

# Test with fake data
python tests/test_with_fake_data.py

# Test emotion model
python tests/test_emotion_model.py
```

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: ML Engine Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python tests/test_v2_pipeline.py
        python tests/test_with_fake_data.py
```

## 📞 Support & Contact

- **ML Team Lead**: [Your Name]
- **Issues**: Create GitHub issue
- **Documentation**: See `docs/` folder
- **Questions**: [Your Contact]

## 🔮 Future Enhancements

When training data arrives:
1. Supervised ML models (XGBoost, Neural Networks)
2. Fine-tuned embeddings
3. Category-specific models
4. Real-time learning

See `training/README.md` for details.

## ⚠️ Important Notes

1. **DO NOT MODIFY** files in `ml_engine/` without consulting ML team
2. **Models auto-download** on first run (requires internet)
3. **Cache directory** will be created automatically
4. **Python 3.8+** required
5. **2GB RAM** minimum recommended

## 📝 Example Integration Checklist

- [ ] Clone repository
- [ ] Install dependencies
- [ ] Test basic analysis
- [ ] Create API endpoint
- [ ] Add input validation
- [ ] Implement error handling
- [ ] Add logging
- [ ] Test with sample data
- [ ] Deploy to staging
- [ ] Monitor performance
- [ ] Deploy to production

---

**Version**: 1.0  
**Last Updated**: 2026-03-06  
**ML Engine Version**: v2.0
