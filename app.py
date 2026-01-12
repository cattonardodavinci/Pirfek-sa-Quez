import streamlit as st
from state import init_session_state
from take_quiz import take_quiz
from analysis import performance_analysis
from leaderboard import leaderboard

st.set_page_config(
    page_title="QuizLearn Professional", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

init_session_state()

# --- 1. Define Professional Palettes ---
PALETTES = {
    "Custom": None, 
    "Default Dark": {"bg": "#0b0e14", "txt": "#ffffff", "card": "#161b22", "accent": "#4f46e5"},
    "Midnight Blue": {"bg": "#0f172a", "txt": "#f8fafc", "card": "#1e293b", "accent": "#0ea5e9"},
    "Deep Forest": {"bg": "#061613", "txt": "#e6f4f1", "card": "#0c2d27", "accent": "#059669"},
    "Cyberpunk": {"bg": "#0d0221", "txt": "#ffffff", "card": "#1a084d", "accent": "#db2777"},
    "Nordic Light": {"bg": "#f3f4f6", "txt": "#1f2937", "card": "#ffffff", "accent": "#2563eb"},
    "Slate & Gold": {"bg": "#1e293b", "txt": "#f1f5f9", "card": "#334155", "accent": "#ca8a04"},
    "Rose Pine": {"bg": "#191724", "txt": "#e0def4", "card": "#1f1d2e", "accent": "#908caa"},
    "Espresso": {"bg": "#1c1917", "txt": "#fafaf9", "card": "#292524", "accent": "#ea580c"},
    "Material Dark": {"bg": "#212121", "txt": "#eeffff", "card": "#424242", "accent": "#00acc1"},
    "Amethyst": {"bg": "#1a103d", "txt": "#f5f3ff", "card": "#2d1b69", "accent": "#7c3aed"},
}

# --- 2. Sidebar Customization ---
with st.sidebar:
    st.title("🎨 Appearance")
    selected_palette = st.selectbox("Select Theme Mode", list(PALETTES.keys()))
    
    if selected_palette == "Custom":
        bg_color = st.color_picker("Background", "#0b0e14")
        text_color = st.color_picker("Main Text", "#ffffff")
        card_bg = st.color_picker("Card/Container", "#161b22")
        accent_color = st.color_picker("Accent Color", "#6366f1")
    else:
        bg_color = PALETTES[selected_palette]["bg"]
        text_color = PALETTES[selected_palette]["txt"]
        card_bg = PALETTES[selected_palette]["card"]
        accent_color = PALETTES[selected_palette]["accent"]

    st.session_state.active_accent = accent_color
    sub_text = f"{text_color}aa"  

# --- 3. THE FIX: HIGH-PRIORITY CSS OVERRIDES ---
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');

    /* 1. FORCE GLOBAL THEME */
    .stApp {{
        background-color: {bg_color} !important;
        background-image: 
            radial-gradient(circle at 15% 20%, {accent_color}14 0%, transparent 45%),
            radial-gradient(circle at 85% 80%, {accent_color}14 0%, transparent 45%) !important;
        color: {text_color} !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}

    /* SIDEBAR DYNAMIC THEME */
    [data-testid="stSidebar"] {{
        background-color: {bg_color} !important;
        border-right: 1px solid {accent_color}33 !important;
    }}
    [data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}
    /* Style the sidebar title specifically with a gradient */
    [data-testid="stSidebar"] h1 {{
        background: linear-gradient(90deg, {text_color} 0%, {accent_color} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }}

    /* 2. FIX THE BLUE BOX (Welcome Message) */
    div[data-testid="stNotification"] {{
        background-color: {accent_color}22 !important;
        color: {text_color} !important;
        border: 1px solid {accent_color}66 !important;
        border-radius: 12px !important;
    }}
    div[data-testid="stNotification"] svg {{
        fill: {accent_color} !important;
    }}

    /* 3. FIX TEXTBOX & SELECTBOX CURVATURE */
    div[data-baseweb="input"], 
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] {{
        border-radius: 12px !important;
        border: 1px solid {text_color}22 !important;
        background-color: transparent !important;
    }}

    /* Focus state */
    div[data-baseweb="input"]:focus-within, 
    div[data-baseweb="select"]:focus-within,
    div[data-baseweb="base-input"]:focus-within {{
        border-color: {accent_color} !important;
        box-shadow: 0 0 0 1px {accent_color} !important;
        border-radius: 12px !important;
    }}

    /* 4. FIX THE DIVIDER */
    .thin-divider {{ 
        height: 1px !important; 
        background-color: {text_color} !important;
        opacity: 0.15 !important;
        margin: 20px 0 !important;
        border: none !important;
    }}

    /* 5. TABS */
    [data-testid="stTabsTabHighlight"] {{
        background-color: {accent_color} !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{ color: {accent_color} !important; }}
    .stTabs [aria-selected="true"] {{ color: {accent_color} !important; }}

    /* 6. BUTTON GLOW EFFECT (Preserved) */
    div.stButton > button, div.stDownloadButton > button {{
        background: {accent_color} !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        border: none !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 4px 15px {accent_color}33 !important;
    }}

    div.stButton > button:hover, div.stDownloadButton > button:hover {{
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 25px {accent_color}88 !important;
        filter: brightness(1.1);
        color: white !important;
    }}
    
    div.stButton > button:active {{
        transform: scale(0.98);
    }}

    /* TITLES */
    .app-title {{
        background: linear-gradient(90deg, {text_color} 0%, {accent_color} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px; font-weight: 800; letter-spacing: -2px;
    }}
    .subtitle {{ color: {sub_text}; margin-bottom: 30px; }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="app-title">QuizLearn</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Master your craft through interactive assessment.</div>', unsafe_allow_html=True)
st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)

tabs = st.tabs(["Assessment", "Analytics", "Hall of Fame"])

with tabs[0]:
    take_quiz()
with tabs[1]:
    performance_analysis()
with tabs[2]:
    leaderboard()