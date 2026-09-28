import time
import random
from google.genai import types

from prompts import (
    build_zero_shot_prompt,
    build_few_shot_prompt,
    build_structured_reasoning_prompt,
)

PROMPT_BUILDERS = {
    "zero-shot": build_zero_shot_prompt,
    "few-shot": build_few_shot_prompt,
    "structured": build_structured_reasoning_prompt,
}


def generate_itinerary(client, user_data, technique, max_retries=5):
    """Generate itinerary with retry logic for transient errors (503, 429)."""
    technique = technique.lower().strip()

    if technique not in PROMPT_BUILDERS:
        raise ValueError(
            f"Unknown technique '{technique}'. "
            f"Choose from: {list(PROMPT_BUILDERS.keys())}"
        )

    prompt = PROMPT_BUILDERS[technique](user_data)

    # Exponential backoff parameters
    base_delay = 1.0  # Start with a 1-second delay
    max_delay = 60.0  # Cap the delay at 60 seconds

    for attempt in range(max_retries):
        try:
            # Use the Chat module to avoid the AFC warning
            chat = client.chats.create(
                model="gemini-3.8-flash",
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=8192,
                ),
            )
            response = chat.send_message(prompt)
            return response.text

        except Exception as e:
            error_str = str(e)

            # Retry on transient server errors (503) and rate limits (429)
            if "503" in error_str or "429" in error_str:
                if attempt < max_retries - 1:
                    # Calculate exponential backoff with jitter
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    jitter = random.uniform(0, delay * 0.1)  # Add up to 10% jitter
                    wait_time = delay + jitter

                    print(
                        f"\n[Attempt {attempt + 1}/{max_retries}] "
                        f"Server busy (503/429). "
                        f"Retrying in {wait_time:.1f} seconds..."
                    )
                    time.sleep(wait_time)
                    continue
                else:
                    return (
                        f"Error: The Gemini service is currently unavailable "
                        f"after {max_retries} attempts. Please try again later."
                    )
            else:
                # For non-transient errors, return the error message immediately
                return f"Error generating itinerary: {e}"

    return "Error: Failed to generate itinerary after all retry attempts."
