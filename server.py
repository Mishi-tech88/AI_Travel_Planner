import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List

from config import initialize_gemini
from travel_planner import generate_itinerary

app = FastAPI(title="AI Travel Planner")

# --- Serve static files (HTML/CSS/JS) ---
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


# --- Request model ---
class TripRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    destination: str = Field(..., min_length=1, max_length=200)
    days: int = Field(..., ge=1, le=365)
    budget: int = Field(..., ge=1)
    interests: List[str] = Field(default_factory=list)
    travel_style: str = Field(..., pattern="^(Solo|Family|Friends)$")
    technique: str = Field(..., pattern="^(zero-shot|few-shot|structured)$")


# --- Proxy endpoint: frontend calls THIS, not Gemini ---
@app.post("/api/generate")
def generate(req: TripRequest):
    try:
        client = initialize_gemini()  # Key is loaded here, server-side only
        user_data = {
            "name": req.name,
            "destination": req.destination,
            "days": req.days,
            "budget": req.budget,
            "interests": req.interests,
            "travel_style": req.travel_style,
        }
        itinerary = generate_itinerary(client, user_data, req.technique)
        return {"itinerary": itinerary}
    except Exception as e:
        # Never leak internal errors or key details to the client
        raise HTTPException(status_code=500, detail="Failed to generate itinerary. Please try again.")