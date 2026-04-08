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
    page_title="PC Analyzer — WinSAT ML",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
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

/* ═══════════════════════════════════════════════════════════════════════════════ */
/* HEADER HERO CYBERPUNK */
.hero-title {
    font-family: 'Orbitron', monospace !important;
    font-size: 3.5rem !important;
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

/* ═══════════════════════════════════════════════════════════════════════════════ */
/* GLASSMORPHISM CARDS */
.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(25px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
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

.glass-card:hover::before {
    left: 100%;
}

.glass-card:hover {
    transform: translateY(-8px);
    box-shadow: 
        0 25px 50px rgba(0,212,255,0.15),
        0 0 0 1px rgba(0,212,255,0.3);
    border-color: var(--neon-cyan);
}

/* ═══════════════════════════════════════════════════════════════════════════════ */
/* SCORE RING ANIMADO 3D */
.score-ring {
    position: relative;
    text-align: center;
    padding: 2rem;
}

.score-circle {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: conic-gradient(var(--neon-cyan) 0deg 270deg, #1A1A2E 270deg 360deg);
    position: relative;
    margin: 0 auto 1rem;
    animation: scoreRotate 4s linear infinite;
}

@keyframes scoreRotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.score-inner {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 120px;
    height: 120px;
    background: var(--dark-bg);
    border-radius: 50%;
    border: 3px solid var(--glass-border);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.score-big {
    font-family: 'Orbitron', monospace;
    font-size: 3rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, var(--neon-cyan), var(--neon-magenta));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(0,212,255,0.8);
}

/* ═══════════════════════════════════════════════════════════════════════════════ */
/* COMPONENT CARDS NEON */
.comp-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}

.comp-card::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 0;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1));
    transition: width 0.6s;
}

.comp-card:hover::after {
    width: 100%;
}

.comp-label {
    font-size: 0.75rem;
    color: var(--neon-cyan);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.comp-name {
    font-size: 1.1rem;
    font-weight: 600;
    background: linear-gradient(135deg, #e5e7eb, #f3f4f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}

/* ═══════════════════════════════════════════════════════════════════════════════ */
/* PROGRESS BARS ANIMADAS */
.progress-container {
    background: rgba(26,26,46,0.8);
    border-radius: 12px;
    height: 10px;
    overflow: hidden;
    margin: 1rem 0;
    position: relative;
}

.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-green));
    border-radius: 12px;
    transition: width 2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    position: relative;
    overflow: hidden;
}

.progress-bar::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* ═══════════════════════════════════════════════════════════════════════════════ */
/* BOTTLENECK ALERTS NEON */
.bn-neon {
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}

.bn-neon::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-magenta));
}

.bn-critical { 
    background: rgba(127,29,29,0.2); 
    border: 1px solid rgba(247,113,113,0.5);
    box-shadow: 0 0 20px rgba(247,113,113,0.3);
}
.bn-warning { 
    background: rgba(120,53,15,0.2); 
    border: 1px solid rgba(251,191,36,0.5);
    box-shadow: 0 0 20px rgba(251,191,36,0.3);
}
.bn-good { 
    background: rgba(20,83,45,0.2); 
    border: 1px solid rgba(74,222,128,0.5);
    box-shadow: 0 0 20px rgba(74,222,128,0.3);
}

/* ═══════════════════════════════════════════════════════════════════════════════ */
/* FPS CARDS HOLOGRÁFICAS */
.fps-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    position: relative;
    transition: all 0.3s ease;
}

.fps-card:hover {
    transform: scale(1.05);
    box-shadow: 0 20px 40px rgba(0,212,255,0.2);
}

.fps-val {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem !important;
    font-weight: 900 !important;
}

/* ═══════════════════════════════════════════════════════════════════════════════ */
/* BOTONES NEON */
.stButton > button {
    background: linear-gradient(45deg, var(--neon-cyan), var(--neon-magenta));
    border: none;
    border-radius: 16px;
    padding: 1rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0,212,255,0.3);
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 40px rgba(0,212,255,0.5);
}

.stButton > button:active {
    transform: translateY(-1px);
}

/* ═══════════════════════════════════════════════════════════════════════════════ */
/* PLOTLY DARK MODE PERFECTO */
.plotly-graph-div {
    filter: drop-shadow(0 10px 30px rgba(0,0,0,0.5));
}

/* ═══════════════════════════════════════════════════════════════════════════════ */
/* RESPONSIVE */
@media (max-width: 768px) {
    .hero-title { font-size: 2.5rem !important; }
    .score-big { font-size: 2.5rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ── Init ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_engines():
    db  = BenchmarkDB()
    ml  = MLEngine(db)
    fps = FPSPredictor()
    return db, ml, fps

db, ml, fps_predictor = load_engines()

# ── UI ───────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PC Analyzer — WinSAT ML",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# ── Sidebar: CPU/GPU manual ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Especificar componentes")
    st.markdown("<p style='font-size:0.82rem;color:#9ca3af;'>Opcional — mejora la precisión del análisis</p>", unsafe_allow_html=True)
    cpu_manual = st.selectbox("Procesador (CPU)", ["— Autodetectar —"] + db.get_cpu_list())
    gpu_manual = st.selectbox("Tarjeta de video (GPU)", ["— Autodetectar —"] + db.get_gpu_list())
    uso = st.selectbox("Uso principal", ["Gaming", "Trabajo / Oficina", "Diseño / Edición", "Streaming", "General"])
    resolucion = st.selectbox("Resolución de juego", ["1080p", "1440p", "4K"])
    st.markdown("---")
    st.markdown("<p style='font-size:0.75rem;color:#4b5563;'>Cómo obtener el archivo WinSAT:</p>", unsafe_allow_html=True)
    st.code("winsat formal", language="bash")
    st.markdown("<p style='font-size:0.75rem;color:#4b5563;'>Archivo en:<br>%windir%\\Performance\\WinSAT\\DataStore\\</p>", unsafe_allow_html=True)

# ── Upload ────────────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "Arrastrá tu archivo WinSAT XML acá",
    type=["xml"],
    help="Archivo generado por 'winsat formal' en Windows"
)

if uploaded is None:
    st.markdown("""
    <div class='info-note'>
    📌 <b>Cómo obtener el archivo:</b> Abrí PowerShell como administrador → escribí <code>winsat formal</code> → esperá que termine (5-10 min) → buscá el XML en <code>C:\\Windows\\Performance\\WinSAT\\DataStore\\</code>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class='comp-card'>
        <div class='comp-label'>CPU analizado</div>
        <div class='comp-name'>Clasificación de tier</div>
        <div class='comp-detail'>Entrada / Media / Alta / Entusiasta</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='comp-card'>
        <div class='comp-label'>Cuello de botella</div>
        <div class='comp-name'>Detección automática</div>
        <div class='comp-detail'>CPU, GPU, RAM o disco</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='comp-card'>
        <div class='comp-label'>FPS predicho</div>
        <div class='comp-name'>Por juego y resolución</div>
        <div class='comp-detail'>Cyberpunk, Fortnite, CS2 y más</div>
        </div>""", unsafe_allow_html=True)
    st.stop()

# ── Parse ─────────────────────────────────────────────────────────────────────
with st.spinner("Leyendo archivo WinSAT..."):
    try:
        content = uploaded.read()
        data = parse_winsat_xml(content)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        st.stop()

# Override con manual si el usuario lo especificó
if cpu_manual != "— Autodetectar —":
    data["cpu_name_override"] = cpu_manual
if gpu_manual != "— Autodetectar —":
    data["gpu_name_override"] = gpu_manual

# ── ML Analysis ──────────────────────────────────────────────────────────────
with st.spinner("Analizando con Machine Learning..."):
    analysis = ml.analyze(data, uso, resolucion)
    fps_data  = fps_predictor.predict(analysis, resolucion)

# ── HERO: Score general ───────────────────────────────────────────────────────
tier_colors = {
    "Entrada":    ("🔵", "#1e3a5f", "#60a5fa"),
    "Media":      ("🟢", "#14532d", "#4ade80"),
    "Media-Alta": ("🟡", "#78350f", "#fbbf24"),
    "Alta":       ("🟠", "#7c2d12", "#fb923c"),
    "Entusiasta": ("🔴", "#4c1d95", "#a78bfa"),
}
tier = analysis["tier"]
tier_icon, tier_bg, tier_color = tier_colors.get(tier, ("⚪", "#1f2937", "#9ca3af"))

col_score, col_info = st.columns([1, 2])
with col_score:
    st.markdown(f"""
    <div class='glass-card score-ring'>
        <div class='score-circle'>
            <div class='score-inner'>
                <div class='score-big'>{overall:.1f}</div>
                <div style='font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 0.3rem;'>
                    TOP {percentile}%
                </div>
            </div>
        </div>
        <div class='tier-badge' style='
            background: rgba(0,212,255,0.2);
            border: 1px solid var(--neon-cyan);
            color: var(--neon-cyan);
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            font-weight: 600;
            font-size: 0.9rem;
        '>{tier_icon} Gama {tier}</div>
    </div>
    """, unsafe_allow_html=True)

with col_info:
    spr = data.get("spr", {})
    st.markdown(f"""
    <div style='background:#1a1d2e;border:1px solid #2a2d3e;border-radius:16px;padding:1.5rem;height:100%;'>
        <div style='font-size:0.9rem;color:#e5e7eb;font-weight:500;margin-bottom:0.8rem;'>Resumen del sistema</div>
        <div style='font-size:0.85rem;color:#9ca3af;line-height:1.8;'>
            🖥️ <b style='color:#e5e7eb;'>CPU:</b> {analysis.get("cpu_display","Detectado")}<br>
            🎮 <b style='color:#e5e7eb;'>GPU:</b> {analysis.get("gpu_display","Detectado")}<br>
            🧠 <b style='color:#e5e7eb;'>RAM:</b> {analysis.get("ram_display","—")}<br>
            💾 <b style='color:#e5e7eb;'>Disco principal:</b> {analysis.get("disk_display","—")}<br>
            🪟 <b style='color:#e5e7eb;'>Sistema:</b> {data.get("os_name","Windows")}<br>
            🔩 <b style='color:#e5e7eb;'>Placa:</b> {data.get("motherboard","—")}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Scores por componente ─────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Puntaje por componente</div>", unsafe_allow_html=True)

components = [
    ("PROCESADOR (CPU)",       analysis.get("cpu_display","CPU"),       analysis.get("cpu_detail",""),  analysis["scores"]["cpu"],  "#4f8ef7"),
    ("TARJETA DE VIDEO (GPU)", analysis.get("gpu_display","GPU"),       analysis.get("gpu_detail",""),  analysis["scores"]["gpu"],  "#4ade80"),
    ("MEMORIA RAM",            analysis.get("ram_display","RAM"),       analysis.get("ram_detail",""),  analysis["scores"]["ram"],  "#a78bfa"),
    ("DISCO PRINCIPAL",        analysis.get("disk_display","Disco"),    analysis.get("disk_detail",""), analysis["scores"]["disk"], "#fbbf24"),
]

cols = st.columns(2)
for i, (label, name, detail, score, color) in enumerate(components):
    pct = min(int(score / 9.9 * 100), 100)
    with cols[i % 2]:
        st.markdown(f"""
        <div class='comp-card'>
            <div class='comp-label'>{label}</div>
            <div class='comp-name'>{name}</div>
            <div class='comp-detail'>{detail}</div>
            <div style='background:#0f1117;border-radius:4px;height:6px;overflow:hidden;'>
                <div style='width:{pct}%;height:100%;background:{color};border-radius:4px;transition:width 1s;'></div>
            </div>
            <div style='display:flex;justify-content:space-between;margin-top:5px;'>
                <span style='font-size:11px;color:#6b7280;'>vs top global</span>
                <span style='font-size:13px;font-weight:500;color:{color};'>{score:.1f} / 9.9</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Radar chart ───────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Radar de rendimiento</div>", unsafe_allow_html=True)

radar_labels = ["CPU (multi-core)", "CPU (single-core)", "RAM", "GPU", "Disco NVMe", "Disco secundario"]
radar_vals   = [
    analysis["scores"]["cpu"] / 9.9 * 100,
    analysis["scores"]["cpu_single"] / 9.9 * 100,
    analysis["scores"]["ram"] / 9.9 * 100,
    analysis["scores"]["gpu"] / 9.9 * 100,
    analysis["scores"]["disk"] / 9.9 * 100,
    analysis["scores"].get("disk2", 1.0) / 9.9 * 100,
]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=radar_vals + [radar_vals[0]],
    theta=radar_labels + [radar_labels[0]],
    fill='toself',
    fillcolor='rgba(79,142,247,0.15)',
    line=dict(color='#4f8ef7', width=2),
    name='Tu PC',
    marker=dict(size=6, color='#4f8ef7')
))
fig_radar.add_trace(go.Scatterpolar(
    r=[100]*len(radar_labels) + [100],
    theta=radar_labels + [radar_labels[0]],
    fill='toself',
    fillcolor='rgba(75,85,99,0.05)',
    line=dict(color='#374151', width=1, dash='dot'),
    name='Top global'
))
fig_radar.update_layout(
    polar=dict(
        bgcolor='#1a1d2e',
        radialaxis=dict(visible=True, range=[0,100], gridcolor='#2a2d3e', tickfont=dict(size=10, color='#6b7280'), ticksuffix=''),
        angularaxis=dict(gridcolor='#2a2d3e', tickfont=dict(size=11, color='#9ca3af'))
    ),
    showlegend=True,
    legend=dict(font=dict(color='#9ca3af'), bgcolor='rgba(0,0,0,0)'),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=380,
    margin=dict(l=60, r=60, t=20, b=20)
)
st.plotly_chart(fig_radar, use_container_width=True)

# ── Cuellos de botella ────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Detección de cuellos de botella (ML)</div>", unsafe_allow_html=True)

bn_type_map = {
    "critical": ("bn-critical", "bn-tag-critical", "⛔ CUELLO DE BOTELLA CRÍTICO"),
    "warning":  ("bn-warning",  "bn-tag-warning",  "⚠️ ATENCIÓN"),
    "good":     ("bn-good",     "bn-tag-good",     "✅ SIN PROBLEMA"),
    "info":     ("bn-info",     "bn-tag-info",     "ℹ️ DATO IMPORTANTE"),
}

for bn in analysis["bottlenecks"]:
    btype = bn.get("type", "info")
    card_cls, tag_cls, tag_label = bn_type_map.get(btype, bn_type_map["info"])
    st.markdown(f"""
    <div class='{card_cls}'>
        <div class='{tag_cls}'>{tag_label}</div>
        <div class='bn-title'>{bn["title"]}</div>
        <div class='bn-desc'>{bn["desc"]}</div>
    </div>
    """, unsafe_allow_html=True)

# ── FPS Predictor ─────────────────────────────────────────────────────────────
st.markdown(f"<div class='section-title'>FPS predicho en {resolucion} (Machine Learning)</div>", unsafe_allow_html=True)

fps_color_map = lambda f: "#4ade80" if f >= 100 else ("#fbbf24" if f >= 60 else "#f87171")

games_per_row = 4
game_list = list(fps_data.items())
for row_start in range(0, len(game_list), games_per_row):
    row_games = game_list[row_start:row_start + games_per_row]
    cols = st.columns(len(row_games))
    for col, (game, info) in zip(cols, row_games):
        fps_val   = info["fps"]
        fps_low   = info["fps_low"]
        setting   = info["setting"]
        color   = fps_color_map(fps_val)
    with col:
        color = fps_color_map(fps_val)
        st.markdown(f"""
        <div class='glass-card fps-card'>
        <div class='fps-game' style='color: rgba(255,255,255,0.6);'>{game}</div>
        <div class='fps-val' style='color: {color}; text-shadow: 0 0 15px {color};'>{fps_val} FPS</div>
        <div class='fps-res'>{setting} • 1% low: {fps_low}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Benchmark bar chart ───────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Comparativa vs configuraciones populares</div>", unsafe_allow_html=True)

comparison = db.get_comparison_configs(analysis)
cfg_names  = [c["name"] for c in comparison]
cfg_scores = [c["score"] for c in comparison]
cfg_colors = ["#4f8ef7" if c.get("is_user") else "#374151" for c in comparison]

fig_bar = go.Figure(go.Bar(
    x=cfg_scores,
    y=cfg_names,
    orientation='h',
    marker_color=cfg_colors,
    text=[f"{s:.1f}" for s in cfg_scores],
    textposition='outside',
    textfont=dict(color='#9ca3af', size=11)
))
fig_bar.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(range=[0, 10], gridcolor='#2a2d3e', tickfont=dict(color='#6b7280')),
    yaxis=dict(tickfont=dict(color='#e5e7eb', size=11)),
    height=300,
    margin=dict(l=0, r=60, t=10, b=10),
    showlegend=False
)
st.plotly_chart(fig_bar, use_container_width=True)

# ── Recomendaciones ───────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Recomendaciones de upgrade</div>", unsafe_allow_html=True)

for i, rec in enumerate(analysis["recommendations"], 1):
    urgency_color = {"alta": "#f87171", "media": "#fbbf24", "baja": "#4ade80"}.get(rec["urgency"], "#9ca3af")
    st.markdown(f"""
    <div class='comp-card'>
        <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
            <div>
                <div style='font-size:0.72rem;color:#6b7280;margin-bottom:3px;'>PRIORIDAD {i}</div>
                <div style='font-size:0.95rem;font-weight:500;color:#e5e7eb;'>{rec["title"]}</div>
                <div style='font-size:0.82rem;color:#9ca3af;margin-top:4px;line-height:1.55;'>{rec["desc"]}</div>
            </div>
            <div style='background:#1f2937;border-radius:8px;padding:4px 10px;font-size:0.75rem;font-weight:500;color:{urgency_color};white-space:nowrap;margin-left:12px;'>
                {rec["urgency"].upper()}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;margin-top:3rem;color:#374151;font-size:0.75rem;'>
    PC Analyzer · Análisis basado en WinSAT + ML · Los FPS son estimaciones basadas en benchmarks históricos
</div>
""", unsafe_allow_html=True)
