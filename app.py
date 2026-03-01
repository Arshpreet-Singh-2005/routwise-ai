import streamlit as st
import os
import requests
import json
import pandas as pd
import folium
import random
from streamlit_folium import st_folium
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool, Tool
from langchain_core.messages import HumanMessage, AIMessage
# ── CONFIG ─────────────────────────────────────────────────────────────────────
load_dotenv()
st.set_page_config(
    page_title="RouteWise AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

:root {
    --green-900: #0a1f0e;
    --green-800: #0f2d14;
    --green-700: #1a4d22;
    --green-600: #226630;
    --green-500: #2d8a42;
    --green-400: #3db357;
    --green-300: #6dcf82;
    --green-200: #a8e6b5;
    --green-100: #e8f7eb;
    --accent:    #00c853;
    --gold:      #f9a825;
    --bg:        #f5faf6;
    --surface:   #ffffff;
    --border:    #d4ead8;
    --text:      #1a2e1d;
    --muted:     #5a7a5f;
    --danger:    #c62828;
}

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── HIDE STREAMLIT DEFAULTS ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── TOP NAVBAR ── */
.navbar {
    background: var(--green-800);
    padding: 1rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 2px solid var(--green-600);
    position: sticky;
    top: 0;
    z-index: 999;
}
.navbar-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.navbar-logo {
    width: 36px; height: 36px;
    background: var(--accent);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
}
.navbar-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
}
.navbar-sub {
    font-size: 0.7rem;
    color: var(--green-300);
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.navbar-badge {
    background: rgba(0,200,83,0.15);
    border: 1px solid var(--accent);
    color: var(--accent);
    font-size: 0.7rem;
    font-family: 'DM Mono', monospace;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.08em;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--green-800) !important;
    border-right: 1px solid var(--green-700) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}
.sidebar-section {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}
.sidebar-section-title {
    font-size: 0.65rem;
    font-family: 'DM Mono', monospace;
    color: var(--green-300);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextArea label {
    color: rgba(255,255,255,0.7) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}
[data-testid="stSidebar"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,200,83,0.2) !important;
}

/* ── GENERATE BUTTON ── */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, var(--accent), #00a846) !important;
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 1.5rem !important;
    width: 100% !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 15px rgba(0,200,83,0.3) !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    box-shadow: 0 6px 20px rgba(0,200,83,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── MAIN CONTENT AREA ── */
.main-content {
    padding: 1.5rem 2rem;
}

/* ── STAT CARDS ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: var(--accent);
}
.stat-card.gold::before { background: var(--gold); }
.stat-card.red::before  { background: var(--danger); }
.stat-card.blue::before { background: #1565c0; }
.stat-label {
    font-size: 0.65rem;
    font-family: 'DM Mono', monospace;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.stat-value {
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1;
}
.stat-unit {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 2px;
}

/* ── SECTION HEADERS ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1rem;
}
.section-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.01em;
}
.section-pill {
    background: var(--green-100);
    color: var(--green-600);
    font-size: 0.65rem;
    font-family: 'DM Mono', monospace;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.05em;
}

/* ── PLAN OUTPUT ── */
.plan-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.5rem;
    line-height: 1.8;
    font-size: 0.9rem;
}
.plan-box h1, .plan-box h2, .plan-box h3 {
    color: var(--green-700) !important;
    font-weight: 700 !important;
}
.plan-box strong { color: var(--green-600); }
.plan-box code {
    background: var(--green-100);
    color: var(--green-700);
    padding: 1px 6px;
    border-radius: 4px;
    font-family: 'DM Mono', monospace;
}

/* ── GEOCODING TABLE ── */
.geo-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
}
.geo-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.25rem;
    border-bottom: 1px solid var(--border);
    font-size: 0.85rem;
}
.geo-row:last-child { border-bottom: none; }
.geo-row:hover { background: var(--green-100); }
.geo-addr { color: var(--text); font-weight: 500; }
.geo-ok   { color: #2e7d32; font-family: 'DM Mono', monospace; font-size: 0.78rem; }
.geo-fail { color: var(--danger); font-family: 'DM Mono', monospace; font-size: 0.78rem; }

/* ── MAP CONTAINER ── */
.map-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
}
.map-header {
    padding: 1rem 1.25rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.map-title {
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--text);
}
.map-meta {
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    color: var(--muted);
}

/* ── CHAT INTERFACE ── */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-height: 320px;
    overflow-y: auto;
    padding: 0.5rem 0;
    scrollbar-width: thin;
    scrollbar-color: var(--green-600) transparent;
}
.chat-bubble {
    display: flex;
    gap: 0.5rem;
    align-items: flex-start;
}
.chat-bubble.user { flex-direction: row-reverse; }
.chat-avatar {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem;
    flex-shrink: 0;
}
.chat-avatar.ai   { background: var(--accent); color: #fff; }
.chat-avatar.user { background: var(--green-700); color: #fff; }
.chat-text {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 0.6rem 0.9rem;
    font-size: 0.8rem;
    color: rgba(255,255,255,0.9);
    max-width: 85%;
    line-height: 1.5;
}
.chat-bubble.user .chat-text {
    background: rgba(0,200,83,0.15);
    border-color: rgba(0,200,83,0.3);
}

/* ── EMPTY STATE ── */
.empty-state {
    background: var(--surface);
    border: 2px dashed var(--border);
    border-radius: 14px;
    padding: 3rem;
    text-align: center;
    color: var(--muted);
}
.empty-icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
.empty-title { font-weight: 700; font-size: 1rem; color: var(--text); margin-bottom: 0.4rem; }
.empty-sub { font-size: 0.85rem; }

/* ── DIVIDER ── */
.eco-divider {
    height: 1px;
    background: linear-gradient(to right, transparent, var(--border), transparent);
    margin: 1.5rem 0;
}

/* ── GREEN SCORE BADGE ── */
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--green-100);
    border: 1px solid var(--green-300);
    color: var(--green-700);
    font-size: 0.78rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

# ── NAVBAR ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="navbar-brand">
    <div class="navbar-logo">🌿</div>
    <div>
      <div class="navbar-title">RouteWise AI</div>
      <div class="navbar-sub">Eco-Friendly Logistics Planner</div>
    </div>
  </div>
  <div class="navbar-badge">● LIVE</div>
</div>
""", unsafe_allow_html=True)

# ── API KEY CHECK ───────────────────────────────────────────────────────────────
if not all([os.getenv("GOOGLE_API_KEY"), os.getenv("ORS_API_KEY")]):
    st.error("🚨 API keys not found! Please check your .env file or Streamlit secrets.")
    st.stop()

# ── LLM INIT ───────────────────────────────────────────────────────────────────
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

# ── SESSION STATE ───────────────────────────────────────────────────────────────
st.session_state.setdefault('agent_plan', None)
st.session_state.setdefault('geocoding_results', None)
st.session_state.setdefault('route_data', None)
st.session_state.setdefault('stop_points', None)
st.session_state.setdefault('route_summary', None)
if "messages" not in st.session_state:
    st.session_state.messages = [AIMessage(content="Hello! I'm RouteWise AI 🌿 Ask me anything about eco-friendly routing, CO2 emissions, or logistics planning!")]

# ── TOOLS ───────────────────────────────────────────────────────────────────────
@st.cache_data
def geocode_multiple_addresses(addresses: str) -> str:
    api_key = os.getenv("ORS_API_KEY")
    address_list = json.loads(addresses)
    results = []
    for address in address_list:
        url = f"https://api.openrouteservice.org/geocode/search?api_key={api_key}&text={address}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data['features']:
                coords = data['features'][0]['geometry']['coordinates']
                results.append({"address": address, "status": "✅ Success", "lon": coords[0], "lat": coords[1]})
            else:
                results.append({"address": address, "status": "❌ Failed", "error": "Address not found."})
        except requests.exceptions.RequestException as e:
            results.append({"address": address, "status": "❌ Failed", "error": str(e)})
    st.session_state.geocoding_results = results
    return json.dumps(results)

@st.cache_data
def get_route_optimization(coordinates: any) -> dict:
    api_key = os.getenv("ORS_API_KEY")
    if isinstance(coordinates, str):
        try:
            coords_list = json.loads(coordinates)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON string format for coordinates."}
    elif isinstance(coordinates, list):
        coords_list = coordinates
    else:
        return {"error": "Invalid input type for coordinates."}

    st.session_state.stop_points = coords_list
    headers = {'Authorization': api_key, 'Content-Type': 'application/json'}
    body = {"coordinates": coords_list}
    try:
        response = requests.post(
            'https://api.openrouteservice.org/v2/directions/driving-car/geojson',
            json=body, headers=headers, timeout=15
        )
        response.raise_for_status()
        data = response.json()
        st.session_state.route_data = data
        summary = data['features'][0]['properties']['summary']
        result = {
            "distance_km": round(summary['distance'] / 1000, 2),
            "duration_minutes": round(summary['duration'] / 60, 2)
        }
        st.session_state.route_summary = result
        return result
    except Exception as e:
        return {"error": f"Routing API error: {e}"}

@st.cache_data
def get_weather_forecast(location: str) -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY") or os.getenv("WEATHER_API_KEY")
    try:
        lat, lon = location.split(',')
    except ValueError:
        return "Invalid location format."
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        condition = data['weather'][0]['main']
        temp = data['main']['temp']
        return f"Weather: {condition}, Temp: {temp}°C"
    except Exception:
        return "Weather: Unknown"

def get_simulated_traffic(location: str) -> str:
    """Simulates the current traffic speed for a given location."""
    return f"Average Speed: {random.randint(30, 80)} km/h"

def calculate_co2_and_score(distance_km: float, vehicle_type: str) -> str:
    """Estimates CO2 emissions and calculates an eco-friendly Green Score."""
    co2_rates = {"car": 0.192, "bike": 0.0, "ev": 0.05, "bus": 0.08}
    co2_kg = distance_km * co2_rates.get(vehicle_type.lower(), 0.192)
    score = max(0, 100 - (co2_kg * 5))
    return f"Estimated CO2 Emission: {co2_kg:.2f} kg, Green Score: {score:.1f}/100"

tools = [
    Tool(name="GeocodeMultipleAddresses",  func=geocode_multiple_addresses, description="Converts a JSON list of addresses into coordinates."),
    Tool(name="GetRouteOptimization",      func=get_route_optimization,     description="Calculates the optimal multi-stop route between coordinates."),
    Tool(name="GetWeatherForecast",        func=get_weather_forecast,       description="Provides the weather forecast for a location."),
    Tool(name="GetSimulatedTraffic",       func=get_simulated_traffic,      description="Gets a simulated traffic speed for a location."),
    Tool(name="CalculateCO2AndScore",      func=calculate_co2_and_score,    description="Calculates CO2 emissions and a Green Score based on distance and vehicle type.")
]

# ── AGENT ───────────────────────────────────────────────────────────────────────
prompt_template = """
You are RouteWise AI, an expert eco-friendly logistics planner. Your goal is to create an efficient and sustainable delivery plan.
You have access to the following tools: {tools}

You MUST follow these specific instructions:
1. Use GeocodeMultipleAddresses ONCE to get coordinates for all addresses.
2. Inspect the geocoding results. Create a new list containing only the coordinates (lon, lat) from the successful results.
3. If there are at least two successful coordinates, use GetRouteOptimization with this filtered list.
4. Use GetWeatherForecast and GetSimulatedTraffic for the starting location.
5. Use CalculateCO2AndScore with the total distance and the user's selected vehicle type.
6. In your final answer, explicitly list any addresses that failed to geocode.

Use the following format:

Question: The user's request.
Thought: Your reasoning.
Action: One of [{tool_names}]
Action Input: The input to the action.
Observation: The result of the action.
... (repeat as needed)
Thought: I have gathered all necessary information.
Final Answer: The final comprehensive delivery plan in Markdown format.

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

agent_prompt = PromptTemplate.from_template(prompt_template)
agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True,
    handle_parsing_errors=True, max_iterations=25
)

# ── SIDEBAR ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.25rem 0 0.5rem;">
      <div style="font-size:0.65rem;font-family:'DM Mono',monospace;color:rgba(255,255,255,0.4);
                  letter-spacing:0.15em;text-transform:uppercase;margin-bottom:1rem;">
        ▸ Route Configuration
      </div>
    </div>
    """, unsafe_allow_html=True)

    addresses_input = st.text_area(
        "Delivery Addresses",
        "Thapar Institute of Engineering and Technology, Patiala\nGolden Temple, Amritsar\nTaj Mahal, Agra",
        height=130,
        help="Enter one address per line"
    )

    vehicle_type = st.selectbox(
        "Vehicle Type",
        ["car", "ev", "bus", "bike"],
        format_func=lambda x: {
            "car": "🚗 Car (192g CO₂/km)",
            "ev": "⚡ Electric Vehicle (50g CO₂/km)",
            "bus": "🚌 Bus (80g CO₂/km)",
            "bike": "🚲 Bike (0g CO₂/km)"
        }[x]
    )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    generate_btn = st.button("🌿 Generate Eco-Plan", use_container_width=True)

    st.markdown("""
    <div style="height:1px;background:rgba(255,255,255,0.08);margin:1.25rem 0;"></div>
    <div style="font-size:0.65rem;font-family:'DM Mono',monospace;color:rgba(255,255,255,0.4);
                letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.75rem;">
      ▸ Chat with RouteWise
    </div>
    """, unsafe_allow_html=True)

    # ── CHAT DISPLAY ──
    chat_html = '<div class="chat-container">'
    for message in st.session_state.messages[-8:]:
        is_ai = isinstance(message, AIMessage)
        avatar = "🌿" if is_ai else "👤"
        avatar_class = "ai" if is_ai else "user"
        bubble_class = "" if is_ai else "user"
        chat_html += f"""
        <div class="chat-bubble {bubble_class}">
          <div class="chat-avatar {avatar_class}">{avatar}</div>
          <div class="chat-text">{message.content}</div>
        </div>"""
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    if prompt := st.chat_input("Ask about routes, CO₂, weather..."):
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.spinner("Thinking..."):
            response = llm.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))
        st.rerun()

# ── GENERATE PLAN ───────────────────────────────────────────────────────────────
if generate_btn:
    st.session_state.agent_plan = None
    st.session_state.geocoding_results = None
    st.session_state.route_data = None
    st.session_state.stop_points = None
    st.session_state.route_summary = None
    st.cache_data.clear()

    if not addresses_input.strip():
        st.warning("Please enter at least two addresses.")
    else:
        with st.spinner("🌿 Calculating eco-friendly route..."):
            try:
                address_list = addresses_input.strip().split('\n')
                full_prompt = f"Create a delivery plan for a '{vehicle_type}' for these addresses: {json.dumps(address_list)}"
                response = agent_executor.invoke({"input": full_prompt})
                st.session_state.agent_plan = response['output']
            except Exception as e:
                st.error(f"An error occurred: {e}")

# ── MAIN CONTENT ────────────────────────────────────────────────────────────────
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# ── STAT CARDS ──
if st.session_state.get('route_summary') or st.session_state.get('geocoding_results'):
    summary = st.session_state.get('route_summary', {})
    geo = st.session_state.get('geocoding_results', [])
    stops_ok = len([g for g in geo if '✅' in g.get('status', '')])

    distance = summary.get('distance_km', '—')
    duration = summary.get('duration_minutes', '—')

    co2_rates = {"car": 0.192, "bike": 0.0, "ev": 0.05, "bus": 0.08}
    if isinstance(distance, (int, float)):
        co2 = round(distance * co2_rates.get(vehicle_type, 0.192), 2)
        score = round(max(0, 100 - co2 * 5), 1)
    else:
        co2 = "—"
        score = "—"

    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-label">Total Distance</div>
        <div class="stat-value">{distance}</div>
        <div class="stat-unit">kilometers</div>
      </div>
      <div class="stat-card gold">
        <div class="stat-label">Est. Duration</div>
        <div class="stat-value">{round(duration) if isinstance(duration, float) else duration}</div>
        <div class="stat-unit">minutes</div>
      </div>
      <div class="stat-card red">
        <div class="stat-label">CO₂ Emissions</div>
        <div class="stat-value">{co2}</div>
        <div class="stat-unit">kilograms</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Green Score</div>
        <div class="stat-value">{score}</div>
        <div class="stat-unit">out of 100</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── TWO COLUMN LAYOUT ──
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    # ── PLAN OUTPUT ──
    if st.session_state.get('agent_plan'):
        st.markdown("""
        <div class="section-header">
          <span>📋</span>
          <span class="section-title">Agent's Eco Plan</span>
          <span class="section-pill">AI GENERATED</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="plan-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.agent_plan)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">🗺️</div>
          <div class="empty-title">No Plan Generated Yet</div>
          <div class="empty-sub">Enter addresses in the sidebar and click Generate Eco-Plan</div>
        </div>
        """, unsafe_allow_html=True)

    # ── GEOCODING RESULTS ──
    if st.session_state.get('geocoding_results'):
        st.markdown("<div class='eco-divider'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-header">
          <span>📍</span>
          <span class="section-title">Address Geocoding</span>
        </div>
        """, unsafe_allow_html=True)

        geo_html = '<div class="geo-card">'
        for g in st.session_state.geocoding_results:
            status_class = "geo-ok" if "✅" in g['status'] else "geo-fail"
            coords = f"{g.get('lat',''):.4f}, {g.get('lon',''):.4f}" if g.get('lat') else "N/A"
            geo_html += f"""
            <div class="geo-row">
              <div class="geo-addr">{g['address']}</div>
              <div style="display:flex;gap:1rem;align-items:center;">
                <span style="font-size:0.72rem;font-family:'DM Mono',monospace;color:var(--muted);">{coords}</span>
                <span class="{status_class}">{g['status']}</span>
              </div>
            </div>"""
        geo_html += '</div>'
        st.markdown(geo_html, unsafe_allow_html=True)

with col2:
    # ── MAP ──
    st.markdown("""
    <div class="section-header">
      <span>🗺️</span>
      <span class="section-title">Route Visualization</span>
      <span class="section-pill">LIVE MAP</span>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get('route_data') and st.session_state.get('stop_points'):
        try:
            points_coords = st.session_state.stop_points
            if points_coords and len(points_coords) > 1:
                start_lat = points_coords[0][1]
                start_lon = points_coords[0][0]

                m = folium.Map(
                    location=[start_lat, start_lon],
                    zoom_start=6,
                    tiles="CartoDB positron"
                )

                # Add styled markers
                for i, point in enumerate(points_coords):
                    label = "🏁" if i == len(points_coords) - 1 else str(i + 1)
                    folium.Marker(
                        [point[1], point[0]],
                        popup=f"Stop {i+1}",
                        icon=folium.DivIcon(
                            html=f"""<div style="background:#226630;color:white;width:28px;height:28px;
                                        border-radius:50%;display:flex;align-items:center;justify-content:center;
                                        font-size:12px;font-weight:bold;border:2px solid white;
                                        box-shadow:0 2px 8px rgba(0,0,0,0.3);">{label}</div>""",
                            icon_size=(28, 28),
                            icon_anchor=(14, 14)
                        )
                    ).add_to(m)

                # Draw route
                route_coords_raw = st.session_state.route_data.get('features', [{}])[0].get('geometry', {}).get('coordinates')
                if route_coords_raw:
                    route_coords_swapped = [(c[1], c[0]) for c in route_coords_raw]
                    folium.PolyLine(
                        route_coords_swapped,
                        color='#2d8a42',
                        weight=4,
                        opacity=0.85,
                        dash_array=None
                    ).add_to(m)

                st.markdown('<div class="map-container">', unsafe_allow_html=True)
                st_folium(m, use_container_width=True, height=450)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Need at least 2 valid stops to draw route.")
        except Exception as e:
            st.error(f"Map error: {e}")
    else:
        st.markdown("""
        <div class="empty-state" style="height:450px;display:flex;flex-direction:column;align-items:center;justify-content:center;">
          <div class="empty-icon">🌍</div>
          <div class="empty-title">Map Will Appear Here</div>
          <div class="empty-sub">Generate a plan to see the optimized route</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
