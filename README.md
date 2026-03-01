# 🌿 RouteWise AI
### Eco-Friendly Logistics Planner powered by LangChain & Gemini

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20App-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.27-green.svg)](https://langchain.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-orange.svg)](https://deepmind.google/gemini)
[![Hackathon](https://img.shields.io/badge/🏆-Hackathon%20Winner-gold.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🏆 About

**RouteWise AI** is an intelligent eco-friendly logistics planner that won the **October 2024 Hackathon**. It uses a **LangChain ReAct Agent** powered by **Google Gemini 2.5 Flash** to optimize multi-stop delivery routes, calculate real-time CO₂ emissions, assign Green Scores, and trigger automated agentic interventions — all through a clean interactive Streamlit dashboard.

---

## ✨ Features

**🗺️ Smart Route Optimization**
Multi-stop delivery route planning using OpenRouteService API with real-time map visualization powered by Folium.

**🌱 CO₂ Tracking & Green Score**
Real-time carbon emission calculations for different vehicle types (Car, EV, Bus, Bike) with a Green Score out of 100.

**🤖 LangChain ReAct Agent**
Autonomous AI agent that plans, geocodes, routes, checks weather and calculates emissions in a single intelligent workflow.

**🌦️ Weather & Traffic Intelligence**
Live weather forecasts via OpenWeatherMap and simulated traffic speed data for smarter route planning.

**💬 AI Chat Assistant**
Built-in chat interface powered by Gemini for answering logistics and eco-routing questions in real time.

**📍 Interactive Map**
Numbered stop markers with green polyline route drawn on a clean CartoDB basemap.

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Frontend** | Streamlit |
| **AI Agent** | LangChain ReAct Agent |
| **LLM** | Google Gemini 2.5 Flash |
| **Routing API** | OpenRouteService |
| **Weather API** | OpenWeatherMap |
| **Map Visualization** | Folium + streamlit-folium |
| **Data Processing** | Pandas |
| **Language** | Python 3.10+ |

---

## 🤖 How the Agent Works

RouteWise AI uses a **ReAct (Reasoning + Acting)** agent that follows this workflow automatically:

```
1. GeocodeMultipleAddresses  →  Convert all addresses to coordinates
       ↓
2. GetRouteOptimization      →  Calculate optimal multi-stop route
       ↓
3. GetWeatherForecast        →  Check weather at starting location
       ↓
4. GetSimulatedTraffic       →  Get current traffic speed
       ↓
5. CalculateCO2AndScore      →  Calculate emissions & Green Score
       ↓
6. Final Answer              →  Comprehensive eco delivery plan
```

---

## 🌱 Vehicle CO₂ Rates

| Vehicle | CO₂ per km | Best For |
|---------|-----------|----------|
| 🚗 Car | 192g | General delivery |
| ⚡ Electric Vehicle | 50g | Eco-conscious routing |
| 🚌 Bus | 80g | Bulk delivery |
| 🚲 Bike | 0g | Short urban distances |

---

## 📁 Project Structure

```
routewise-ai/
│
├── app.py                  ← Main Streamlit application
├── requirements.txt        ← Python dependencies
├── .env.example            ← API key template (safe to share)
├── .gitignore              ← Git ignore rules
└── README.md               ← Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Arshpreet-Singh-2005/routewise-ai.git
cd routewise-ai
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

Edit `.env`:
```
GOOGLE_API_KEY=your_google_api_key_here
ORS_API_KEY=your_openrouteservice_api_key_here
OPENWEATHER_API_KEY=your_openweathermap_api_key_here
```

### 5. Run the App
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🔑 Getting API Keys

| API | Where to Get | Free Tier |
|-----|-------------|-----------|
| **Google Gemini** | [aistudio.google.com](https://aistudio.google.com) | ✅ Free |
| **OpenRouteService** | [openrouteservice.org](https://openrouteservice.org/dev/#/signup) | ✅ Free (2000 req/day) |
| **OpenWeatherMap** | [openweathermap.org/api](https://openweathermap.org/api) | ✅ Free (1000 req/day) |

---

## ☁️ Deploy on Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set **Main file path** to `app.py`
5. Go to **Advanced Settings → Secrets** and add:
```toml
GOOGLE_API_KEY = "your_key_here"
ORS_API_KEY = "your_key_here"
OPENWEATHER_API_KEY = "your_key_here"
```
6. Click **Deploy**

---

## 🖥️ How to Use

**Step 1** — Enter delivery addresses in the sidebar (one per line)

**Step 2** — Select your vehicle type

**Step 3** — Click **🌿 Generate Eco-Plan**

**Step 4** — View your optimized route on the map with:
- Total distance and estimated duration
- CO₂ emissions calculated for your vehicle type
- Green Score out of 100
- Full agent-generated delivery plan in Markdown
- Stop-by-stop geocoding results with coordinates

**Step 5** — Use the **AI Chat** in the sidebar to ask follow-up questions

---

## 📊 Example Output

```
Route: Patiala → Amritsar → Agra
Distance:        847 km
Duration:        623 minutes
CO₂ Emissions:  42.35 kg  (Car)  |  4.24 kg  (EV)
Green Score:     78.8 / 100
Weather:         Clear, 28°C
Traffic:         65 km/h average speed
```

---

## 🏆 Hackathon

This project was built for and **won** the October 2024 Hackathon.

**Category:** AI & Sustainability

**Key Innovation:** Combining a LangChain ReAct Agent with real-world routing APIs to create a fully autonomous eco-logistics planner that not only finds the best route but also quantifies its environmental impact and suggests greener alternatives.

---

## 🔮 Future Improvements

- [ ] Real-time traffic data via Google Maps API
- [ ] Multi-modal routing (combine car + public transport)
- [ ] Historical route analytics dashboard
- [ ] Email/SMS delivery update notifications
- [ ] REST API endpoint for third-party integration
- [ ] Carbon offset suggestions and eco-tips per route
- [ ] Mobile-responsive design

---

## 📚 References

- [LangChain Documentation](https://docs.langchain.com)
- [Google Gemini API](https://ai.google.dev)
- [OpenRouteService API](https://openrouteservice.org/dev/#/api-docs)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Folium Documentation](https://python-visualization.github.io/folium)

---

## 👤 Author

**Arshpreet Singh**
- GitHub: [@Arshpreet-Singh-2005](https://github.com/Arshpreet-Singh-2005)
- LinkedIn: [Arshpreet Singh](https://www.linkedin.com/in/arshpreet-singh-56089531a/)

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with 🌿 for a Greener Planet
  <br>
  LangChain · Gemini 2.5 · OpenRouteService · Streamlit
  <br><br>
  🏆 Hackathon Winner — October 2024
</p>
