from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from config import initialize_gemini
from travel_planner import generate_itinerary


# -----------------------------
# FastAPI app
# -----------------------------

app = FastAPI(title="AI Travel Planner")


# Serve HTML, CSS, JS
app.mount("/static", StaticFiles(directory="static"), name="static")


# -----------------------------
# Initialize Gemini
# -----------------------------

try:
    model = initialize_gemini()
except Exception as e:
    model = None
    print(f"[ERROR] Failed to initialize Gemini: {e}")

@app.get("/")
def home():
    return FileResponse("static/index.html")

class TravelRequest(BaseModel):
    name: str
    destination: str
    days: int
    budget: float
    interests: list[str]
    travel_style: str
    technique: str = "zero-shot"

@app.post("/api/plan")
def create_plan(request: TravelRequest):

    if model is None:
        return {
            "success": False,
            "error": "Gemini failed to initialize. Check your GEMINI_API_KEY."
        }

    user_data = {
        "name": request.name,
        "destination": request.destination,
        "days": request.days,
        "budget": request.budget,
        "interests": request.interests,
        "travel_style": request.travel_style,
    }

    try:
        itinerary = generate_itinerary(
            model,
            user_data,
            request.technique
        )

        return {
            "success": True,
            "itinerary": itinerary
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }