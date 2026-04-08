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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Fondo principal: gradiente radial oscuro tipo telemetría/espacio */
.main {
    background: radial-gradient(circle at 50% 0%, #151a2e 0%, #06080d 100%);
}
.block-container { padding: 2rem 2rem 4rem; max-width: 1100px; }

/* Efecto Glassmorphism y bordes de alta tecnología para todas las tarjetas */
.hero-card, .comp-card, .fps-card, .info-note, [class^="bn-"] {
    background: rgba(15, 17, 26, 0.4) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(0, 240, 255, 0.1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    transition: all 0.3s ease;
}

.hero-card { border-radius: 12px; padding: 2rem; margin-bottom: 1.5rem; }
.score-ring { text-align: center; padding: 1rem; }

/* Puntaje General: Texto con brillo (Glow effect) */
.score-big {
    font-size: 4.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #00f0ff, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    text-shadow: 0px 0px 20px rgba(0, 240, 255, 0.3);
    font-family: 'JetBrains Mono', monospace;
}

.score-label { color: #8b949e; font-size: 0.85rem; margin-top: 8px; text-transform: uppercase; letter-spacing: 0.15em; }

/* Badges de Tier transparentes y con brillo interior */
.tier-badge {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 4px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-top: 8px;
    letter-spacing: 0.05em;
    border: 1px solid currentColor;
    background: transparent !important;
    box-shadow: inset 0 0 10px currentColor, 0 0 10px rgba(0,0,0,0.5);
}

/* Tarjetas de componentes interactivas */
.comp-card { border-radius: 8px; padding: 1.2rem; margin-bottom: 0.8rem; border-left: 2px solid transparent; }
.comp-card:hover {
    border-color: rgba(0, 240, 255, 0.5);
    border-left: 2px solid #00f0ff;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.1);
    transform: translateY(-2px);
}

.comp-label { font-size: 0.7rem; color: #00f0ff; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 6px; font-weight: 600;}
.comp-name { font-size: 1.05rem; font-weight: 500; color: #ffffff; }
.comp-detail { font-size: 0.8rem; color: #8b949e; margin: 4px 0 10px; }
.metric-val { font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; color: #c4b5fd; }

/* Cuellos de botella - Estilo terminal de alertas */
.bn-critical { border-left: 4px solid #ff003c !important; }
.bn-warning  { border-left: 4px solid #ffaa00 !important; }
.bn-good     { border-left: 4px solid #00ff66 !important; }
.bn-info     { border-left: 4px solid #00f0ff !important; }

.bn-tag-critical { color: #ff003c; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-shadow: 0 0 8px rgba(255,0,60,0.4); text-transform: uppercase; }
.bn-tag-warning  { color: #ffaa00; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-shadow: 0 0 8px rgba(255,170,0,0.4); text-transform: uppercase; }
.bn-tag-good     { color: #00ff66; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-shadow: 0 0 8px rgba(0,255,102,0.4); text-transform: uppercase; }
.bn-tag-info     { color: #00f0ff; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-shadow: 0 0 8px rgba(0,240,255,0.4); text-transform: uppercase; }

.bn-title { font-size: 0.95rem; font-weight: 500; color: #ffffff; margin: 6px 0 4px; }
.bn-desc  { font-size: 0.82rem; color: #8b949e; margin-top: 4px; line-height: 1.55; }

/* FPS Cards - Display digital */
.fps-card { border-radius: 8px; padding: 1.2rem; text-align: center; }
.fps-card:hover { border-color: #7c3aed; box-shadow: 0 0 15px rgba(124, 58, 237, 0.2); transform: scale(1.02); }
.fps-game { font-size: 0.8rem; color: #8b949e; margin-bottom: 6px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
.fps-val  { font-size: 1.9rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; text-shadow: 0 0 12px currentColor; }
.fps-res  { font-size: 0.75rem; color: #6b7280; margin-top: 6px; letter-spacing: 0.05em; }

/* Títulos de sección con línea de energía neón */
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #ffffff;
    margin: 2.8rem 0 1.2rem;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    position: relative;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.section-title::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 80px;
    height: 2px;
    background: #00f0ff;
    box-shadow: 0 0 10px #00f0ff;
}

/* Área de subida de archivo tipo escaner */
.upload-area {
    border: 2px dashed rgba(0, 240, 255, 0.3);
    border-radius: 8px;
    padding: 3rem 2rem;
    text-align: center;
    background: rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}
.upload-area:hover { border-color: #00f0ff; background: rgba(0, 240, 255, 0.03); }

/* Botón holográfico */
.stButton > button {
    background: transparent;
    color: #00f0ff;
    border: 1px solid #00f0ff;
    border-radius: 4px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    width: 100%;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    transition: all 0.3s ease;
    box-shadow: inset 0 0 10px rgba(0, 240, 255, 0.05);
}
.stButton > button:hover {
    background: rgba(0, 240, 255, 0.1);
    box-shadow: inset 0 0 15px rgba(0, 240, 255, 0.2), 0 0 15px rgba(0, 240, 255, 0.2);
    color: #fff;
    border-color: #fff;
}

.info-note {
    border-left: 4px solid #7c3aed !important;
    border-radius: 4px;
    padding: 1rem;
    font-size: 0.85rem;
    color: #c9d1d9;
    margin: 1rem 0;
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
st.markdown("## 🖥️ PC Hardware Analyzer")
st.markdown("<p style='color:#6b7280;margin-top:-8px;margin-bottom:1.5rem;'>Subí tu archivo WinSAT XML — análisis automático con Machine Learning</p>", unsafe_allow_html=True)

# ── Sidebar: CPU/GPU manual ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Especificar componentes")
    cpu_manual = st.selectbox("Procesador (CPU)", ["— Autodetectar —"] + db.get_cpu_list())
    gpu_manual = st.selectbox("Tarjeta de video (GPU)", ["— Autodetectar —"] + db.get_gpu_list())
    uso = st.selectbox("Uso principal", ["Gaming", "Trabajo / Oficina", "Diseño / Edición", "Streaming", "General"])
    resolucion = st.selectbox("Resolución de juego", ["1080p", "1440p", "4K"])

uploaded = st.file_uploader("Arrastrá tu archivo WinSAT XML acá", type=["xml"])

if uploaded is None:
    st.markdown("<div class='info-note'>📌 📌 <b>Cómo obtener el archivo:</b> Abrí PowerShell como administrador → escribí <code>winsat formal</code> → esperá que termine (5-10 min) → buscá el XML en <code>C:\\Windows\\Performance\\WinSAT\\DataStore\\</code>", unsafe_allow_html=True)
    st.stop()
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
try:
    content = uploaded.read()
    data = parse_winsat_xml(content)
except Exception as e:
    st.error(f"Error al leer el archivo: {e}")
    st.stop()

if cpu_manual != "— Autodetectar —": data["cpu_name_override"] = cpu_manual
if gpu_manual != "— Autodetectar —": data["gpu_name_override"] = gpu_manual

analysis = ml.analyze(data, uso, resolucion)
fps_data = fps_predictor.predict(analysis, resolucion)
# PREPARAMOS LAS VARIABLES DEL RADAR JUSTO DESPUÉS DEL ANÁLISIS
radar_labels = ["CPU Multi", "CPU Single", "RAM", "GPU", "NVMe", "Disk 2"]
radar_vals = [
    analysis["scores"].get("cpu", 0) / 9.9 * 100,
    analysis["scores"].get("cpu_single", 0) / 9.9 * 100,
    analysis["scores"].get("ram", 0) / 9.9 * 100,
    analysis["scores"].get("gpu", 0) / 9.9 * 100,
    analysis["scores"].get("disk", 0) / 9.9 * 100,
    analysis["scores"].get("disk2", 1.0) / 9.9 * 100,]

# ── HERO: Score general ───────────────────────────────────────────────────────
tier_colors = {
    "Entrada":    ("🔵", "rgba(30, 58, 95, 0.3)", "#60a5fa"),
    "Media":      ("🟢", "rgba(20, 83, 45, 0.3)", "#4ade80"),
    "Media-Alta": ("🟡", "rgba(120, 53, 15, 0.3)", "#fbbf24"),
    "Alta":       ("🟠", "rgba(124, 45, 18, 0.3)", "#fb923c"),
    "Entusiasta": ("🔴", "rgba(76, 29, 149, 0.3)", "#a78bfa"),
}
tier = analysis["tier"]
tier_icon, tier_bg, tier_color = tier_colors.get(tier, ("⚪", "rgba(31, 41, 55, 0.3)", "#9ca3af"))

col_score, col_info = st.columns([1, 2])
with col_score:
    overall = analysis["overall_score"]
    percentile = analysis["global_percentile"]
    st.markdown(f"""
    <div class='hero-card' style='text-align:center;'>
        <div class='score-label'>Puntaje General</div>
        <div class='score-big'>{overall:.1f}</div>
        <div class='score-label' style='margin-bottom:10px;'>de 9.9 máximo</div>
        <div style='display:inline-block; padding:6px 16px; border-radius:4px; font-size:0.8rem; font-weight:600; 
                    background:{tier_bg} !important; color:{tier_color}; border: 1px solid {tier_color}; 
                    box-shadow: inset 0 0 10px {tier_bg}, 0 0 15px {tier_bg}; text-transform: uppercase; letter-spacing:0.1em;'>
            {tier_icon} Gama {tier}
        </div>
        <div style='margin-top:15px; font-size:0.8rem; color:#8b949e;'>
            Top <b style="color:#00f0ff; font-family:var(--font-mono);">{percentile}%</b> global
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_info:
    st.markdown(f"""
    <div class='hero-card' style='height:100%;'>
        <div style='font-size:0.9rem;color:#e5e7eb;font-weight:500;margin-bottom:0.8rem;'>Resumen del sistema</div>
        <div style='font-size:0.85rem;color:#9ca3af;line-height:1.8;'>
            🖥️ <b style='color:#e5e7eb;'>CPU:</b> {analysis.get("cpu_display","Detectado")}<br>
            🎮 <b style='color:#e5e7eb;'>GPU:</b> {analysis.get("gpu_display","Detectado")}<br>
            🧠 <b style='color:#e5e7eb;'>RAM:</b> {analysis.get("ram_display","—")}<br>
            💾 <b style='color:#e5e7eb;'>Disco:</b> {analysis.get("disk_display","—")}
            🔩 <b style='color:#e5e7eb;'>Placa:</b> {data.get("motherboard","—")}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Scores por componente ─────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Puntaje por componente</div>", unsafe_allow_html=True)

components = [
    ("PROCESADOR (CPU)",       analysis.get("cpu_display","CPU"),       analysis.get("cpu_detail",""),  analysis["scores"]["cpu"],  "#00f0ff"), # Cian Neón
    ("TARJETA DE VIDEO (GPU)", analysis.get("gpu_display","GPU"),       analysis.get("gpu_detail",""),  analysis["scores"]["gpu"],  "#7c3aed"), # Violeta Eléctrico
    ("MEMORIA RAM",            analysis.get("ram_display","RAM"),       analysis.get("ram_detail",""),  analysis["scores"]["ram"],  "#ffaa00"), # Naranja Técnico
    ("DISCO PRINCIPAL",        analysis.get("disk_display","Disco"),    analysis.get("disk_detail",""), analysis["scores"]["disk"], "#00ff66"), # Verde Neón
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
fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=radar_vals + [radar_vals[0]],
    theta=radar_labels + [radar_labels[0]],
    fill='toself',
    fillcolor='rgba(0, 240, 255, 0.15)',
    line=dict(color='#00f0ff', width=2),
    name='Tu PC',
    marker=dict(size=6, color='#00f0ff')
))
fig_radar.add_trace(go.Scatterpolar(
    r=[100]*len(radar_labels) + [100],
    theta=radar_labels + [radar_labels[0]],
    fill='toself',
    fillcolor='rgba(124, 58, 237, 0.05)',
    line=dict(color='#7c3aed', width=1, dash='dot'),
    name='Top global'
))
fig_radar.update_layout(
    polar=dict(
        bgcolor='rgba(0,0,0,0)',
        radialaxis=dict(visible=True, range=[0,100], gridcolor='rgba(255,255,255,0.1)', tickfont=dict(size=10, color='#8b949e', family='JetBrains Mono'), ticksuffix=''),
        angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(size=11, color='#c9d1d9'))
    ),
    showlegend=True,
    legend=dict(font=dict(color='#c9d1d9'), bgcolor='rgba(0,0,0,0)'),
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
        color     = fps_color_map(fps_val)
        with col:
            st.markdown(f"""
            <div class='fps-card'>
                <div class='fps-game'>{game}</div>
                <div class='fps-val' style='color:{color};'>{fps_val}</div>
                <div class='fps-res'>FPS · {setting}</div>
                <div style='font-size:0.7rem;color:#6b7280;margin-top:2px;'>1% low: {fps_low}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Benchmark bar chart ───────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Comparativa vs configuraciones populares</div>", unsafe_allow_html=True)

comparison = db.get_comparison_configs(analysis)
cfg_names  = [c["name"] for c in comparison]
cfg_scores = [c["score"] for c in comparison]
cfg_colors = ["#00f0ff" if c.get("is_user") else "rgba(255,255,255,0.1)" for c in comparison]

fig_bar = go.Figure(go.Bar(
    x=cfg_scores,
    y=cfg_names,
    orientation='h',
    marker_color=cfg_colors,
    text=[f"{s:.1f}" for s in cfg_scores],
    textposition='outside',
    textfont=dict(color='#00f0ff', size=12, family='JetBrains Mono')
))
fig_bar.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(range=[0, 10], gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#8b949e', family='JetBrains Mono')),
    yaxis=dict(tickfont=dict(color='#c9d1d9', size=11)),
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
