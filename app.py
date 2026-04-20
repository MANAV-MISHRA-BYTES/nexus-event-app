import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import translate_v2 as translate

# Load environment variables cleanly in a production setting.
# DO NOT hardcode credentials.
load_dotenv()

app = Flask(__name__)

# Verify API Keys / configs exist, but allow the app to boot even if they fail 
# initialization so the user can see visual errors.
genai_key = os.getenv("GEMINI_API_KEY")
if genai_key:
    genai.configure(api_key=genai_key)

# Initialize Google Cloud Translation client
# This typically requires GOOGLE_APPLICATION_CREDENTIALS set in the environment.
translate_client = None
try:
    translate_client = translate.Client()
except Exception as e:
    print(f"Translation Client Initialization skipped: {e}")
    print("Ensure GOOGLE_APPLICATION_CREDENTIALS is set for translation to work.")

# A mock JSON Schedule of a Hackathon/Conference for the AI to analyze.
# This represents what might come from a database in a real app.
MOCK_SCHEDULE = {
    "sessions": [
        {"id": 1, "title": "Opening Keynote: Next-Gen Web Technologies", "time": "09:00 AM", "location": "Main Auditorium", "type": "Keynote"},
        {"id": 2, "title": "Hands-on: Accessible UI for the Web", "time": "10:30 AM", "location": "Room 101", "type": "Workshop"},
        {"id": 3, "title": "Global Innovators Mixer", "time": "12:00 PM", "location": "Lounge C", "type": "Networking"},
        {"id": 4, "title": "Mastering the Google Cloud Ecosystem", "time": "01:00 PM", "location": "Hall B", "type": "Panel"},
        {"id": 5, "title": "Vue.js & Tailwind Masterclass", "time": "03:00 PM", "location": "Room 202", "type": "Workshop"},
        {"id": 6, "title": "AI in Production: Scalability", "time": "04:30 PM", "location": "Hall A", "type": "Presentation"}
    ]
}

@app.route('/')
def index():
    """
    Renders the main single-page application.
    Passes down data (like the Maps API key and raw schedule) to the frontend securely.
    """
    maps_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
    return render_template('index.html', MOCK_SCHEDULE=MOCK_SCHEDULE, maps_key=maps_key)

@app.route('/api/optimize_roi', methods=['POST'])
def optimize_roi():
    """
    The ROI Optimizer module. Takes user's goal via JSON, pings Gemini, 
    and returns an optimized personalized schedule prioritizing high-value sessions.
    """
    data = request.json
    user_goal = data.get('goal', '')
    
    if not user_goal:
        return jsonify({"error": "No goal provided"}), 400

    # Strict JSON formatting constraint for the Gemini prompt
    prompt = f"""
    You are an expert AI event coordinator.
    Below is the complete schedule for a physical tech conference:
    {json.dumps(MOCK_SCHEDULE)}
    
    The user's specific event goal is: "{user_goal}"
    
    Analyze the schedule and return a JSON list of session IDs that are most valuable for this user's goal, ordered chronologically. Limit the output to 3 or 4 highly curated sessions to maximize ROI. Include a brief 1-sentence reasoning for why each session is selected.
    
    CRITICAL INSTRUCTION: Return ONLY a valid JSON list. Do not use blockquotes or introductory text. Format exactly like this:
    [
        {{"id": 1, "reasoning": "This keynote matches your interest in..."}}
    ]
    """
    
    try:
        if not os.getenv("GEMINI_API_KEY") or "your_" in os.getenv("GEMINI_API_KEY"):
            return jsonify({"error": "Missing Gemini API Key! Please copy .env.example to a new file named .env (with a dot at the start) and insert your real GEMINI_API_KEY."}), 400

        # Using highly efficient gemini-2.5-flash.
        model = genai.GenerativeModel('gemini-2.5-flash') 
        response = model.generate_content(prompt)
        
        # Parse the JSON. Clean up markdown block quotes if Gemini returns them.
        raw_text = response.text.replace('```json', '').replace('```', '').strip()
        optimized_schedule = json.loads(raw_text)
        return jsonify(optimized_schedule)
    except Exception as e:
        return jsonify({"error": f"Failed to optimize schedule: {str(e)}"}), 500

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """
    The Global Mingler module. Uses Google Cloud Translation API for
    accessible, real-time face-to-face networking spanning language barriers.
    """
    data = request.json
    text = data.get('text', '')
    target_lang = data.get('target', 'es')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
        
    try:
        if translate_client:
            # Translation API call
            result = translate_client.translate(text, target_language=target_lang)
            # The API returns HTML entities by default, unescape them or return as is
            # For simplicity, returning raw translation result. 
            return jsonify({"translatedText": result['translatedText']})
        else:
            # Graceful fallback for hackathon demos if keys aren't loaded properly
            return jsonify({"translatedText": f"[Mock Translation -> {target_lang.upper()}]: {text}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run in standard development mode
    app.run(debug=True, port=5000, host='0.0.0.0')
