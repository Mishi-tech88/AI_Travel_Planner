# main.py
# AI Travel Planner — CLI entry point
# Run with: python main.py

from config import initialize_gemini
from travel_planner import generate_itinerary


def get_user_input():
    """Collect traveler details from the user via terminal prompts."""
    print("\n" + "=" * 60)
    print("           AI TRAVEL PLANNER — powered by Gemini")
    print("=" * 60)

    name = input("Name: ").strip()
    destination = input("Destination: ").strip()

    # Validate days as an integer
    while True:
        try:
            days = int(input("Number of Days: ").strip())
            if days <= 0:
                print("Please enter a positive number of days.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number (e.g., 4).")

    # Validate budget as a number
    while True:
        try:
            budget = float(input("Budget (USD): ").strip())
            if budget <= 0:
                print("Please enter a positive budget.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number (e.g., 800).")

    interests_raw = input(
        "Interests (comma-separated, e.g., Food, Beaches, Shopping): "
    ).strip()
    interests = [i.strip() for i in interests_raw.split(",") if i.strip()]

    travel_style = input("Travel Style (Solo/Family/Friends): ").strip()

    return {
        "name": name,
        "destination": destination,
        "days": days,
        "budget": budget,
        "interests": interests,
        "travel_style": travel_style,
    }


def choose_technique():
    """Ask the user which prompting technique to use."""
    print("\nChoose a prompting technique:")
    print("  1. Zero-Shot")
    print("  2. Few-Shot")
    print("  3. Structured Reasoning")

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        mapping = {"1": "zero-shot", "2": "few-shot", "3": "structured"}
        if choice in mapping:
            return mapping[choice]
        print("Invalid choice. Please enter 1, 2, or 3.")


def main():
    # Step 1: Initialize Gemini
    try:
        model = initialize_gemini()
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize Gemini: {e}")
        print("Check that your .env file contains a valid GEMINI_API_KEY.")
        return

    # Step 2: Collect user input
    user_data = get_user_input()

    # Step 3: Choose prompting technique
    technique = choose_technique()

    # Step 4: Generate itinerary
    print("\n" + "=" * 60)
    print(f"Generating itinerary using '{technique}' prompting...")
    print("=" * 60 + "\n")

    itinerary = generate_itinerary(model, user_data, technique)

    # Step 5: Display result
    print(itinerary)
    print("\n" + "=" * 60)
    print("                 END OF ITINERARY")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()