"""
Test ML Pipeline V2 with Proper Metadata Usage
This script demonstrates the correct way to use hook and cliffhanger metadata
"""

import json
from ml_engine.ml_pipeline_v2 import analyze_episode_v2


def test_with_metadata(json_file: str):
    """Test the pipeline with proper metadata extraction"""
    
    print("\n" + "="*80)
    print(f"  TESTING WITH METADATA: {json_file}")
    print("="*80 + "\n")
    
    # Load the test data
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"📁 Category: {data['category']}")
    print(f"🎬 Direction: {data['direction']}")
    print(f"🎯 Main Hook: {data['hook']}\n")
    
    all_results = []
    
    # Analyze each episode with proper metadata
    for episode in data["episodes"]:
        print(f"\n{'='*80}")
        print(f"  EPISODE {episode['episode_number']}: {episode['title']}")
        print(f"{'='*80}\n")
        
        # Extract metadata
        story = episode['story']
        hook = episode.get('hook', '')
        cliffhanger = episode.get('cliffhanger', '')
        
        print(f"📝 Episode Hook:")
        print(f"  \"{hook}\"\n")
        
        print(f"📖 Story Length: {len(story.split())} words\n")
        
        print(f"🎬 Episode Cliffhanger:")
        print(f"  \"{cliffhanger}\"\n")
        
        # Run V2 analysis with metadata
        result = analyze_episode_v2(
            text=story,
            category=data['category'],
            hook=hook,
            cliffhanger=cliffhanger
        )
        
        all_results.append({
            "episode": episode['episode_number'],
            "title": episode['title'],
            "analysis": result
        })
        
        # Display results
        print("📊 SEMANTIC FEATURES:")
        semantic = result["features"]["semantic_features"]
        print(f"  Hook Strength: {semantic['hook_strength']:.3f}")
        print(f"    → {semantic['hook_reason']}")
        print(f"  Conflict Score: {semantic['conflict_score']:.3f}")
        print(f"    → {semantic['conflict_reason']}")
        print(f"  Cliffhanger Score: {semantic['cliffhanger_score']:.3f}")
        print(f"    → {semantic['cliffhanger_reason']}")
        
        print("\n🎭 EMOTIONAL ARC:")
        emotional = result["features"]["emotional_arc"]
        print(f"  Arc Shape: {emotional['arc_shape']}")
        print(f"  Emotion Variance: {emotional['emotion_variance']:.3f}")
        print(f"  Emotion Peak: {emotional['emotion_peak']:.3f}")
        
        print("\n🎯 RETENTION ANALYSIS:")
        retention = result["retention"]
        print(f"  Risk Score: {retention['risk_score']:.3f}")
        print(f"  Risk Level: {retention['risk_level']}")
        print(f"    → {retention['reason']}")
        
        print("\n🎬 CLIFFHANGER ANALYSIS:")
        cliff = result["cliffhanger"]
        print(f"  Score: {cliff['cliffhanger_score']:.1f}/10")
        print(f"  Strength: {cliff['strength']}")
        print(f"    → {cliff['reason']}")
        
        print("\n📈 SUMMARY:")
        summary = result["summary"]
        print(f"  Overall Score: {summary['overall_score']}/100")
        print(f"  Engagement Level: {summary['engagement_level']}")
        
        if summary["key_strengths"]:
            print(f"\n  ✅ Key Strengths:")
            for strength in summary['key_strengths']:
                print(f"     • {strength}")
        
        if summary["key_weaknesses"]:
            print(f"\n  ❌ Key Weaknesses:")
            for weakness in summary['key_weaknesses']:
                print(f"     • {weakness}")
        
        print(f"\n{'─'*80}\n")
    
    # Series-level summary
    print("\n" + "="*80)
    print("  SERIES-LEVEL SUMMARY")
    print("="*80 + "\n")
    
    avg_overall_score = sum(r['analysis']['summary']['overall_score'] for r in all_results) / len(all_results)
    avg_retention_risk = sum(r['analysis']['retention']['risk_score'] for r in all_results) / len(all_results)
    avg_hook_strength = sum(r['analysis']['features']['semantic_features']['hook_strength'] for r in all_results) / len(all_results)
    avg_cliffhanger = sum(r['analysis']['cliffhanger']['cliffhanger_score'] for r in all_results) / len(all_results)
    
    print(f"📊 Average Metrics Across All Episodes:")
    print(f"  Overall Score: {avg_overall_score:.1f}/100")
    print(f"  Retention Risk: {avg_retention_risk:.3f}")
    print(f"  Hook Strength: {avg_hook_strength:.3f}")
    print(f"  Cliffhanger Score: {avg_cliffhanger:.1f}/10")
    
    print(f"\n🎯 Episode Performance:")
    for r in all_results:
        score = r['analysis']['summary']['overall_score']
        engagement = r['analysis']['summary']['engagement_level']
        emoji = "🟢" if score >= 55 else ("🟡" if score >= 40 else "🔴")
        print(f"  {emoji} Episode {r['episode']}: {score}/100 ({engagement})")
    
    # Save full results
    output_file = json_file.replace('.json', '_full_analysis.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "series_info": {
                "category": data['category'],
                "direction": data['direction'],
                "main_hook": data['hook']
            },
            "episodes": all_results,
            "series_summary": {
                "avg_overall_score": avg_overall_score,
                "avg_retention_risk": avg_retention_risk,
                "avg_hook_strength": avg_hook_strength,
                "avg_cliffhanger_score": avg_cliffhanger
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Full analysis saved to: {output_file}")
    
    print("\n" + "="*80)
    print("  ANALYSIS COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        # Default to test_output_5.json
        json_file = "test_output_5.json"
    
    test_with_metadata(json_file)
