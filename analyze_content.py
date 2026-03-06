"""
Quick Content Analysis Script
Analyze any text content and get retention predictions
"""

import sys
import json
from ml_engine.ml_pipeline_v2 import analyze_episode_v2


def analyze_from_text(text: str, category: str = None):
    """Analyze text content and print results"""
    
    print("\n" + "="*80)
    print("  CONTENT ANALYSIS")
    print("="*80 + "\n")
    
    # Run analysis
    result = analyze_episode_v2(text, category)
    
    # Print results
    print(f"📁 Category: {result['category']}")
    print(f"📊 Overall Score: {result['summary']['overall_score']}/100")
    print(f"🎯 Engagement: {result['summary']['engagement_level']}")
    print(f"⚠️  Retention Risk: {result['retention']['risk_score']:.3f} ({result['retention']['risk_level']})")
    
    print(f"\n📈 Key Metrics:")
    semantic = result['features']['semantic_features']
    print(f"  Hook Strength: {semantic['hook_strength']:.3f}")
    print(f"  Conflict Score: {semantic['conflict_score']:.3f}")
    print(f"  Cliffhanger: {semantic['cliffhanger_score']:.3f}")
    
    cliff = result['cliffhanger']
    print(f"\n🎬 Cliffhanger: {cliff['cliffhanger_score']:.1f}/10 ({cliff['strength']})")
    print(f"  {cliff['reason']}")
    
    print(f"\n💡 Recommendations:")
    for i, rec in enumerate(result['retention']['recommendations'][:5], 1):
        if isinstance(rec, dict):
            print(f"  {i}. [{rec['priority']}] {rec['area']}")
            print(f"     → {rec['suggestion']}")
        else:
            print(f"  {i}. {rec}")
    
    if result['summary']['key_strengths']:
        print(f"\n✅ Strengths:")
        for strength in result['summary']['key_strengths']:
            print(f"  • {strength}")
    
    if result['summary']['key_weaknesses']:
        print(f"\n❌ Weaknesses:")
        for weakness in result['summary']['key_weaknesses']:
            print(f"  • {weakness}")
    
    print("\n" + "="*80 + "\n")
    
    return result


def analyze_from_file(filepath: str, category: str = None):
    """Analyze content from a file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        # Try to parse as JSON first
        try:
            data = json.load(f)
            if 'story' in data:
                text = data['story']
                category = category or data.get('category')
            elif 'episodes' in data and len(data['episodes']) > 0:
                text = data['episodes'][0]['story']
                category = category or data['episodes'][0].get('category')
            else:
                text = json.dumps(data)
        except json.JSONDecodeError:
            # Plain text file
            f.seek(0)
            text = f.read()
    
    return analyze_from_text(text, category)


def main():
    """Main entry point"""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python analyze_content.py <file.txt>")
        print("  python analyze_content.py <file.json>")
        print("  python analyze_content.py <file.txt> <category>")
        print("\nExamples:")
        print("  python analyze_content.py story.txt")
        print("  python analyze_content.py episode.json")
        print("  python analyze_content.py story.txt crime")
        sys.exit(1)
    
    filepath = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        result = analyze_from_file(filepath, category)
        
        # Optionally save results
        output_file = filepath.rsplit('.', 1)[0] + '_analysis.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Full results saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
