import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def initialize_gemini():
    """Initialize the new Google GenAI client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    
    # The new SDK uses a Client object instead of a GenerativeModel
    client = genai.Client(api_key=api_key)
    return client
