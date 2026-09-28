# ✈️ AI Travel Planner

Generate personalized travel itineraries using three prompting techniques:
**Zero-Shot**, **Few-Shot**, and **Structured Reasoning**.

---

## 📋 Features

- Personalized day-by-day itinerary based on user preferences
- Budget-aware recommendations
- Three prompting techniques for comparison
- CLI + Streamlit web UI

---

## ⚙️ Setup

```bash
# 1. Clone / create project folder
mkdir ai-travel-planner
cd ai-travel-planner
```
```bash
# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux
```
```bash
# 3. Install dependencies
pip install -r requirements.txt
```
```bash
# 4. Add your Gemini API key
# Create .env file:
GEMINI_API_KEY=your_api_key_here
```
```bash
#run on localhost
uvicorn main:app --reload # Uvicorn running on http://127.0.0.1:8000
# run CLI
python main.py
```
Get a free API key: https://aistudio.google.com/app/apikey
