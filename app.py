```python
import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json
import re
from src.parser import parse_winsat_xml
from src.ml_engine import MLEngine
from src.benchmark_db import BenchmarkDB
from src.fps_predictor import FPSPredictor

st.set_page_config(
    page_title="🖥️ PC Analyzer Pro — Cyber Edition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS CYBERPUNK ULTRA ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --neon-cyan: #00D4FF;
    --neon-magenta: #FF00D4;
    --neon-green: #00FF88;
    --neon-orange: #FFAA00;
    --dark-bg: #0A0A0A;
    --glass-bg: rgba(255,255,255,0.05);
    --glass-border: rgba(0,212,255,0.2);
}

html, body, [class*="css"] { 
    font-family: 'Inter', sans-serif; 
    background: var(--dark-bg) !important;
}

.main { 
    background: linear-gradient(-45deg, var(--dark-bg), #1A1A2E, #16213E, #0F0F23);
    background-size: 400% 400%;
    animation: gradientShift 20s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* HEADER HERO */
.hero-title {
    font-family: 'Orbitron', monospace !important;
    font-size: 4rem !important;
    font-weight: 900 !important;
    background: linear-gradient(45deg, var(--neon-cyan), var(--neon-magenta), var(--neon-green), var(--neon-orange));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    background-size: 300% 300%;
    animation: neonFlow 3s ease-in-out infinite, glowPulse 2s ease-in-out infinite alternate;
    text-shadow: 0 0 30px rgba(0,212,255,0.6);
    line-height: 1.1;
}

@keyframes neonFlow {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

@keyframes glowPulse {
    from { filter: drop-shadow(0 0 10px rgba(0,212,255,0.5)); }
    to { filter: drop-shadow(0 0 25px rgba(0,212,255,0.8)); }
}

.hero-subtitle {
    font-size: 1.4rem;
    color: rgba(255,255,255,0.8);
    font-weight: 300;
    margin: 1rem 0 3rem;
    text-shadow: 0 0 10px rgba(0,212,255,0.3);
}

/* GLASSMORPHISM */
.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(25px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.1), transparent);
    transition: left 0.6s;
}

.glass-card:hover::before { left: 100%; }

.glass-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 30px 60px rgba(0,212,255,0.2), 0 0 0 1px rgba(0,212,255,0.4);
    border-color: var(--neon-cyan);
}

/* SCORE RING 3D */
.score-ring { text-align: center; padding: 2.5rem; }

.score-circle {
    width: 220px; height: 220px;
    border-radius: 50%;
    background: conic-gradient(var(--neon-cyan) 0deg 270deg, #1A1A2E 270deg 360deg);
    position: relative;
    margin: 0 auto 1.5rem;
    animation: scoreRotate 4s linear infinite;
}

@keyframes scoreRotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.score-inner {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 150px; height: 150px;
    background: var(--dark-bg);
    border-radius: 50%;
    border: 4px solid var(--glass-border);
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
}

.score-big {
    font-family: 'Orbitron', monospace !important;
    font-size: 3.5rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, var(--neon-cyan), var(--neon-magenta));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 25px rgba(0,212,255,0.9);
    line-height: 1;
}

.tier-badge {
    background: rgba(0,212,255,0.15);
    border: 1px solid var(--neon-cyan);
    color: var(--neon-cyan);
    padding: 0.7rem 2rem;
    border-radius: 50px;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.05em;
    text-shadow: 0 0 10px rgba(0,212,255,0.5);
}

/* COMPONENTS */
.comp-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}

.comp-card::after {
    content: ''; position: absolute;
    top: 0; right: 0; width: 0; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1));
    transition: width 0.6s;
}

.comp-card:hover::after { width: 100%; }

.comp-label {
    font-size: 0.8rem;
    color: var(--neon-cyan);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 0.8rem;
}

.comp-name {
    font-size: 1.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #e5e7eb, #f3f4f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

/* PROGRESS BARS */
.progress-container {
    background: rgba(26,26,46,0.8);
    border-radius: 12px;
    height: 12px;
    overflow: hidden;
    margin: 1.2rem 0;
    position: relative;
}

.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-green));
    border-radius: 12px;
    transition: width 2.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    position: relative;
}

.progress-bar::after {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* BOTTLENECKS */
.bn-neon {
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}

.bn-neon::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 5px;
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-magenta));
}

.bn-critical { 
    background: rgba(127,29,29,0.25); 
    border: 1px solid rgba(247,113,113,0.6);
    box-shadow: 0 0 30px rgba(247,113,113,0.4);
}
.bn-warning { 
    background: rgba(120,53,15,0.25); 
    border: 1px solid rgba(251,191,36,0.6);
    box-shadow: 0 0 30px rgba(251,191,36,0.4);
}
.bn-good { 
    background: rgba(20,83,45,0.25); 
    border: 1px solid rgba(74,222,128,0.6);
    box-shadow: 0 0 30px rgba(74,222,128,0.4);
}

/* FPS CARDS */
.fps-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 2rem;
    text-align: center;
    position: relative;
    transition: all 0.4s ease;
    box-shadow: 0 15px 35px rgba(0,0,0,0.3);
}

.fps-card:hover {
    transform: scale(1.08) translateY(-5px);
    box-shadow: 0 25px 50px rgba(0,212,255,0.3);
}

.fps-val {
    font-family: 'Orbitron', monospace !important;
    font-size: 2.8rem !important;
    font-weight: 900 !important;
    text-shadow: 0 0 20px currentColor;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(45deg, var(--neon-cyan), var(--neon-magenta));
    border: none;
    border-radius: 20px;
    padding: 1.2rem 2.5rem;
    font-weight: 700;
    font-size: 1.1rem;
    position: relative;
    overflow: hidden;
    transition: all 0.4s ease;
    box-shadow: 0 15px 35px rgba(0,212,255,0.4);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.stButton > button:hover {
    transform: translateY(-5px);
    box-shadow: 0 25px 50px rgba(0,212,255,0.6);
}

.stButton > button:active { transform: translateY(-2px); }

/* SECTIONS */
.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--neon-cyan), var(--neon-magenta));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 3rem 0 1.5rem;
    padding-bottom: 1rem;
    position: relative;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-magenta));
    border-radius: 2px;
}

/* UPLOAD */
.upload-area {
    border: 3px dashed var(--glass-border);
    border-radius: 24px;
    padding: 4rem 3rem;
    text-align: center;
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
}

.upload-area:hover {
    border-color: var(--neon-cyan);
    box-shadow: 0 0 30px rgba(0,212,255,0.3);
}

/* PLOTLY */
.plotly-graph-div {
    filter: drop-shadow(0 20px 40px rgba(0,0,0,0.5));
    border-radius: 20px;
    overflow: hidden;
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .hero-title { font-size: 2.8rem !important; }
    .score-big { font-size: 2.8rem !important; }
    .glass-card { padding: 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# ── PARTICULAS DE FONDO ───────────────────────────────────────────────────────
st.components.v1.html("""
<div id="particles-js" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;"></div>
<script src='https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js'></script>
<script>
particlesJS('particles-js', {
    particles: {
        number: { value: 60, density: { enable: true, value_area: 800 } },
        color: { value: ['#00D4FF', '#FF00D4', '#00FF88'] },
        shape: { type: 'circle' },
        opacity: { value: 0.4, random: true },
        size: { value: 4, random: true },
        line_linked: { enable: true, distance: 120, color: '#00D4FF', opacity: 0.3, width: 1 },
        move: { enable: true, speed: 1.5, direction: 'none', random: true }
    },
    interactivity: {
        detect_on: 'canvas',
        events: { 
            onhover: { enable: true, mode: 'grab' }, 
            onclick: { enable: true, mode: 'push' },
            resize: true 
        }
    }
});
</script>
""", height=100)

# ── Init ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_engines():
    db  = BenchmarkDB()
    ml  = MLEngine(db)
    fps = FPSPredictor()
    return db, ml, fps

db, ml, fps_predictor = load_engines()

# ── UI ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align: center; padding: 4rem 2rem 2rem;'>
    <h1 class='hero-title'>⚡ PC ANALYZER PRO</h1>
    <p class='hero-subtitle'>WinSAT + Machine Learning • FPS Predictor IA • Análisis en Tiempo Real</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎮 Configuración Manual")
    st.markdown("<p style='font-size:0.85rem;color:rgba(255,255,255,0.6);'>Mejora la precisión del análisis</p>", unsafe_allow_html=True)
    cpu_manual = st.selectbox("🧠 CPU", ["— Autodetectar —"] + db.get_cpu_list())
    gpu_manual = st.selectbox("🎮 GPU", ["— Autodetectar —"] + db.get_gpu_list())
    uso = st.selectbox("🎯 Uso principal", ["Gaming", "Trabajo / Oficina", "Diseño / Edición", "Streaming", "General"])
    resolucion = st.selectbox("📺 Resolución", ["1080p", "1440p", "4K"])
    
    st.markdown("---")
    st.markdown("""
    <div style='background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 12px; backdrop-filter: blur(10px);'>
        <div style='font-size: 0.8rem; color: rgba(255,255,255,0.7); line-height: 1.5;'>
            💡 <b>winsat formal</b> en PowerShell (admin)<br>
            📁 <code>%windir%\\Performance\\WinSAT\\DataStore\\</code>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Upload ───────────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "🔍 Arrastrá tu archivo WinSAT XML",
    type=["xml"],
    help="winsat formal → 5-10 min → XML en DataStore"
)

if uploaded is None:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='glass-card' style='height: 200px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🧠</div>
            <div style='font-weight: 600; color: var(--neon-cyan);'>CPU Tier</div>
            <div style='color: rgba(255,255,255,0.6); font-size: 0.9rem;'>Entrada → Entusiasta</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("")
       
