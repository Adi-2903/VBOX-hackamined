import json
from services.analyzer_service import analyze_and_fix_episode

def test_analyzer_flow():
    print("========================================")
    print("   VBOX: EXPLAINABLE AI ANALYST TEST")
    print("========================================")
    
    # Mock Episode Data
    episode_text = """
    So I was walking down the street today, right?
    And I saw this cat. It was a pretty cool cat. 
    It just sat there, looking at me. 
    I wondered what it was thinking. 
    Anyway, then I went home and had some chai. 
    See you in the next one!
    """
    
    # Mock ML Scores (low scores to trigger issues)
    full_ml_json = {
        "overall_score": 0.42,
        "hook_strength": 0.31,
        "conflict_score": 0.25,
        "cliffhanger_score": 0.15,
        "risk_score": 0.82,  # High risk
        "emotional_arc_score": 0.35,
        "metadata": {
            "duration": "45s",
            "pacing": "slow",
            "audience": "Gen Z"
        }
    }
    
    print("\nStarting Two-Step Analysis Chain...")
    result = analyze_and_fix_episode(episode_text, full_ml_json)
    
    if "error" in result["analyst"]:
        print(f"\nANALYST FAILED: {result['analyst']['error']}")
        return

    print("\n--- ANALYST OUTPUT (LLAMA) ---")
    print(json.dumps(result["analyst"], indent=2))
    
    if "error" in result["fixer"]:
        print(f"\nFIXER FAILED: {result['fixer']['error']}")
    else:
        print("\n--- FIXER SUGGESTIONS (MISTRAL) ---")
        print(json.dumps(result["fixer"], indent=2))
        
    # Save results
    with open("analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        
    print("\nResults saved to analysis_results.json")

if __name__ == "__main__":
    test_analyzer_flow()
