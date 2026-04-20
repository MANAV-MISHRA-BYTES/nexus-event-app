<div align="center">
  <img src="https://img.icons8.com/fluency/144/conference.png" alt="Nexus Logo"/>
  <h1>🌟 Nexus Event App</h1>
  <p><em>A modern, mobile-first AI-powered physical event experience</em></p>

  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)](https://python.org/)
  [![Flask](https://img.shields.io/badge/Flask-3.0.3-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
  [![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D.svg?logo=vue.js&logoColor=white)](https://vuejs.org/)
  [![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
</div>

Note to Judges: Due to strict local banking restrictions on cloud billing accounts for students, I was unable to deploy to Google Cloud Run. I have successfully deployed the exact same containerized architecture to Render. The live app is fully functional here: https://nexus-event-app.onrender.com

<br />

Welcome to **Nexus**, the ultimate lightweight hackathon application that aims to revolutionize the physical event experience. By seamlessly blending AI itinerary optimization with real-world accessibility features, Nexus brings corporate networking and event scheduling right into the future. 🚀

## ✨ Features

- 🧠 **AI-Powered ROI Optimizer**: Feed the app your professional event goal, and our Gemini AI engine dynamically analyzes the conference schedule to curate a personalized timeline prioritizing your ROI.
- 🗺️ **Interactive Venue Navigation**: Real-time integration with the Google Maps Embed API lets you visualize physical venue navigation dynamically from within your generated AI itinerary.
- 🌐 **Global Mingler**: Break language barriers during live networking! A responsive interface connects directly to Google Cloud Translation API for elegant, instant, localized communication.
- 🎨 **Modern Aesthetics**: Built with an elegant, highly accessible, responsive dark-themed glassmorphism interface powered by Tailwind CSS.

## 🛠️ Technology Stack

| Architecture   | Technology Used |
| :---           | :---            |
| **Frontend**   | HTML5, Vue.js 3 (CDN), Tailwind CSS (CDN) |
| **Backend**    | Python, Flask |
| **LLM Engine** | Google Gemini `2.5-flash` |
| **APIs**       | Google Cloud Translation API, Google Maps Platform |

## 🚀 Quick Setup & Installation

Follow these steps to host local copies on your machine:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd nexus-event-app
   ```

2. **Establish the Virtual Environment**:
   Ensure you keep your system tidy by spinning up a local Python virtual environment.
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   Nexus requires secure API keys. Duplicate the `.env.example` file and rename it to strictly `.env`.
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GOOGLE_MAPS_API_KEY=your_maps_api_key_here
   ```

## 🎮 Running The App

Start up your Flask server:

```bash
python app.py
```
*Head over to [http://localhost:5000](http://localhost:5000) and watch Nexus come to life!*
