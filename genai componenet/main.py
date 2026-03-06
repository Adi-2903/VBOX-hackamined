import json
from services.direction_generator import generate_directions
from services.story_generator import generate_story


def main():

    idea = input("Enter idea: ")
    audience = input("Target audience: ")
    episodes = int(input("Number of episodes (Hackathon recommendation: 5-8): "))

    print("\nGenerating direction suggestions...\n")

    directions_data = generate_directions(idea)

    if "error" in directions_data:
        print("Error generating directions. Raw output:")
        print(directions_data["raw"])
        return

    print("\n--- SUGGESTED DIRECTIONS ---\n")
    for idx, d in enumerate(directions_data.get("suggested_directions", []), 1):
        print(f"{idx}. {d['direction_name']} ({d['category']}) - {d['why_it_fits']}")

    chosen_direction = input("\nChoose a direction name: ")

    print("\nGenerating story...\n")

    story = generate_story(
        idea=idea,
        audience=audience,
        episodes=episodes,
        direction=chosen_direction
    )

    print("\n--- GENERATED STORY (JSON) ---\n")
    print(json.dumps(story, indent=2))

    # Save to file
    output_path = "generated_story.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(story, f, indent=2, ensure_ascii=False)
    
    print(f"\nStory saved to {output_path}")


if __name__ == "__main__":
    main()