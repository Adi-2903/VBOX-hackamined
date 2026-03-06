# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-03-06

### 🎉 Major Release - Production Ready

### Added
- **Metadata Support**: Pipeline now accepts separate `hook` and `cliffhanger` parameters
- **Generous Scoring**: Adjusted scoring to give most content 60-75/100 range
- **Improved Retention Model**: More realistic risk assessment (LOW/MEDIUM/HIGH)
- **Enhanced Documentation**: Complete guides for metadata usage, backend integration, and GenAI
- **Test Script**: `test_with_metadata.py` for proper testing with metadata

### Changed
- **Scoring Formula**: 
  - Added 20-point baseline (scores range 20-100 instead of 0-100)
  - Applied stronger power boost (0.65 instead of 0.80)
  - Adjusted engagement thresholds (EXCELLENT: 70+, GOOD: 55-69)
- **Retention Risk Thresholds**:
  - LOW: <0.60 (was <0.50)
  - MEDIUM: 0.60-0.79 (was 0.50-0.74)
  - HIGH: 0.80+ (was 0.75+)
- **Strength Detection**: More generous thresholds (hook: 30%+, conflict: 25%+)
- **Weakness Detection**: Stricter thresholds (only flags issues below 15%)

### Fixed
- **Critical**: Fixed hook and cliffhanger extraction to use metadata instead of text extraction
- **Circular Import**: Fixed keyword_detector.py circular import issue
- **Backward Compatibility**: Pipeline works with or without metadata

### Removed
- All test JSON files (test_output_2, 3, 4, 5)
- All test analysis markdown files
- Old test scripts that don't use metadata
- Empty directories and cache files
- Outdated summary and handoff documents

### Technical Details

**API Changes:**
```python
# Old API
result = analyze_episode_v2(text)

# New API (recommended)
result = analyze_episode_v2(
    text=story,
    category="Relationships",
    hook=episode_hook,
    cliffhanger=episode_cliffhanger
)
```

**Scoring Changes:**
- Most episodes now score 60-75/100 (was 40-55)
- Only 1-2 out of 6-7 episodes should score below 55
- Retention risk is more realistic (most are LOW or MEDIUM)

### Migration Guide

If you have existing code:

1. Update your API calls to pass `hook` and `cliffhanger` parameters
2. Expect higher scores (60-75 range is normal)
3. Use `test_with_metadata.py` as reference
4. Read `METADATA_USAGE_GUIDE.md` for details

---

## [1.0.0] - 2026-03-05

### Initial Release
- Basic ML pipeline with semantic analysis
- Emotion classification
- Retention prediction
- Cliffhanger scoring
- Keyword detection

