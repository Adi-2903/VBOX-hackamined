import json
import os
from services.direction_generator import generate_directions
from services.story_generator import generate_story
from dotenv import load_dotenv

load_dotenv()

def test_story_flow():
    print("========================================")
    print("   VBOX: STORY DECOMPOSER TEST TOOL")
    print("========================================")
    
    idea = input("Story Idea [Default: Tech heist in Neo-Mumbai]: ") or "Tech heist in Neo-Mumbai"
    audience = input("Target Audience [Default: Gen Z Creators]: ") or "Gen Z Creators"
    episodes = int(input("Episodes [Default: 5]: ") or 5)
    
    print("\nSTEP 1: ANALYZING IDEA & FETCHING DIRECTIONS...")
    directions_data = generate_directions(idea)
    
    if "error" in directions_data:
        print(f"FAILED: {directions_data['error']}")
        return

    print("\nAVAILABLE DIRECTIONS:")
    suggestions = directions_data.get("suggested_directions", [])
    for idx, d in enumerate(suggestions, 1):
        print(f"[{idx}] {d['direction_name']}")
        print(f"    Category: {d['category']}")
        print(f"    Why: {d['why_it_fits']}\n")
    
    choice = int(input("Select direction number (1-3): ") or 1)
    chosen_direction = suggestions[choice-1]['direction_name']
    
    print(f"\nSTEP 2: GENERATING {episodes} EPISODES FOR '{chosen_direction}'...")
    story_data = generate_story(idea, audience, episodes, chosen_direction)
    
    if "error" in story_data:
        print(f"STORY GEN FAILED: {story_data['error']}")
        print("Raw Response:", story_data.get("raw_response"))
    else:
        print("\nSTEP 3: SUCCESS! SAVING TO 'test_output.json'...")
        with open("test_output.json", "w", encoding="utf-8") as f:
            json.dump(story_data, f, indent=2, ensure_ascii=False)
            
        print("\nSTORY STRUCTURE PREVIEW:")
        print(f"Category: {story_data.get('category')}")
        print(f"Hook: {story_data.get('hook')}")
        print("\nEpisodes Generated:")
        for ep in story_data.get("episodes", []):
            print(f"- Ep {ep['episode_number']}: {ep['title']}")
            print(f"  Cliffhanger: {ep['cliffhanger']}")
    print("\nFull JSON saved to test_output.json")
if __name__ == "__main__":
    test_story_flow()
