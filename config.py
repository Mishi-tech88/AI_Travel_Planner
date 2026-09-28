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




# # config.py
# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()

# def initialize_gemini():
#     """Initialize the Gemini API with the API key."""
#     api_key = os.getenv("GEMINI_API_KEY")
#     if not api_key:
#         raise ValueError("GEMINI_API_KEY not found in environment variables.")
    
#     genai.configure(api_key=api_key)
    
#     # Using Gemini 1.5 Flash for fast, cost-effective responses
#     model = genai.GenerativeModel(
#         model_name="gemini-3.8-flash",
#         generation_config={
#             "temperature": 0.7,
#             "top_p": 0.95,
#             "top_k": 40,
#             "max_output_tokens": 2048,
#         }
#     )
#     return model