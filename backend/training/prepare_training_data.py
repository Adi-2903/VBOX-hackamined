"""
Training Data Preparation Script
Converts GenAI-generated data into format suitable for model training
"""

import json
import pandas as pd
from pathlib import Path


def prepare_training_data(input_file: str, output_dir: str = "training/data"):
    """
    Prepare training data from GenAI-generated content.
    
    Expected input format:
    {
        "episodes": [
            {
                "story": "text content...",
                "category": "crime/romance/horror/etc",
                "labels": {
                    "hook_strength": 0.0-1.0,
                    "conflict_score": 0.0-1.0,
                    "cliffhanger_score": 0.0-1.0,
                    "retention_risk": 0.0-1.0,
                    "overall_quality": 0-100
                }
            },
            ...
        ]
    }
    
    Args:
        input_file: Path to JSON file with generated data
        output_dir: Directory to save processed training data
    """
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Load data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    episodes = data.get("episodes", [])
    
    if not episodes:
        print("❌ No episodes found in input file")
        return
    
    print(f"📊 Processing {len(episodes)} episodes...")
    
    # Prepare training dataset
    training_data = []
    
    for i, episode in enumerate(episodes):
        story = episode.get("story", "")
        category = episode.get("category", "unknown")
        labels = episode.get("labels", {})
        
        if not story:
            print(f"⚠️  Skipping episode {i+1}: No story content")
            continue
        
        training_data.append({
            "episode_id": i + 1,
            "story": story,
            "category": category,
            "hook_strength": labels.get("hook_strength", 0.5),
            "conflict_score": labels.get("conflict_score", 0.5),
            "cliffhanger_score": labels.get("cliffhanger_score", 0.5),
            "retention_risk": labels.get("retention_risk", 0.5),
            "overall_quality": labels.get("overall_quality", 50),
            "word_count": len(story.split()),
            "sentence_count": len([s for s in story.split('.') if s.strip()])
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(training_data)
    
    # Save as CSV
    csv_path = f"{output_dir}/training_data.csv"
    df.to_csv(csv_path, index=False)
    print(f"✅ Saved training data to {csv_path}")
    
    # Save as JSON
    json_path = f"{output_dir}/training_data.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved training data to {json_path}")
    
    # Print statistics
    print("\n📈 Dataset Statistics:")
    print(f"  Total episodes: {len(df)}")
    print(f"  Categories: {df['category'].value_counts().to_dict()}")
    print(f"  Avg word count: {df['word_count'].mean():.1f}")
    print(f"  Avg hook strength: {df['hook_strength'].mean():.3f}")
    print(f"  Avg conflict score: {df['conflict_score'].mean():.3f}")
    print(f"  Avg cliffhanger: {df['cliffhanger_score'].mean():.3f}")
    print(f"  Avg retention risk: {df['retention_risk'].mean():.3f}")
    print(f"  Avg quality: {df['overall_quality'].mean():.1f}")
    
    return df


def validate_training_data(data_file: str):
    """Validate training data format and quality"""
    
    print("\n🔍 Validating training data...")
    
    df = pd.read_csv(data_file)
    
    issues = []
    
    # Check required columns
    required_cols = ['story', 'category', 'hook_strength', 'conflict_score', 
                     'cliffhanger_score', 'retention_risk', 'overall_quality']
    
    for col in required_cols:
        if col not in df.columns:
            issues.append(f"Missing required column: {col}")
    
    # Check for missing values
    if df['story'].isna().any():
        issues.append(f"{df['story'].isna().sum()} episodes have missing story content")
    
    # Check value ranges
    for col in ['hook_strength', 'conflict_score', 'cliffhanger_score', 'retention_risk']:
        if col in df.columns:
            if (df[col] < 0).any() or (df[col] > 1).any():
                issues.append(f"{col} has values outside [0, 1] range")
    
    if 'overall_quality' in df.columns:
        if (df['overall_quality'] < 0).any() or (df['overall_quality'] > 100).any():
            issues.append("overall_quality has values outside [0, 100] range")
    
    # Check category distribution
    if 'category' in df.columns:
        category_counts = df['category'].value_counts()
        if len(category_counts) < 2:
            issues.append("Only one category found - need diverse categories")
        
        min_samples = category_counts.min()
        if min_samples < 10:
            issues.append(f"Some categories have < 10 samples (min: {min_samples})")
    
    if issues:
        print("\n⚠️  Validation Issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ All validation checks passed!")
    
    return len(issues) == 0


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python prepare_training_data.py <input_file.json>")
        print("\nExample:")
        print("  python prepare_training_data.py genai_generated_data.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Prepare data
    df = prepare_training_data(input_file)
    
    if df is not None:
        # Validate
        validate_training_data("training/data/training_data.csv")
