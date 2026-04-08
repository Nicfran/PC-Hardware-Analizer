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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main { background: #0f1117; }
.block-container { padding: 2rem 2rem 4rem; max-width: 1100px; }

.hero-card {
    background: linear-gradient(135deg, #1a1d2e 0%, #0f1117 100%);
    border: 1px solid #2a2d3e;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}

.score-ring {
    text-align: center;
    padding: 1rem;
}

.score-big {
    font-size: 4rem;
    font-weight: 600;
    background: linear-gradient(135deg, #4f8ef7, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}

.score-label { color: #6b7280; font-size: 0.85rem; margin-top: 4px; }

.tier-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 500;
    margin-top: 8px;
}

.comp-card {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s;
}
.comp-card:hover { border-color: #4f8ef7; }

.comp-label { font-size: 0.72rem; color: #6b7280; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 4px; }
.comp-name { font-size: 1rem; font-weight: 500; color: #e5e7eb; }
.comp-detail { font-size: 0.8rem; color: #9ca3af; margin: 4px 0 10px; }

.metric-val { font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; color: #a78bfa; }

.bn-critical { background: #1f1011; border: 1px solid #7f1d1d; border-radius: 10px; padding: 1rem; margin-bottom: 0.6rem; }
.bn-warning  { background: #1c1708; border: 1px solid #78350f; border-radius: 10px; padding: 1rem; margin-bottom: 0.6rem; }
.bn-good     { background: #0a1f0e; border: 1px solid #14532d; border-radius: 10px; padding: 1rem; margin-bottom: 0.6rem; }
.bn-info     { background: #0c1a2e; border: 1px solid #1e3a5f; border-radius: 10px; padding: 1rem; margin-bottom: 0.6rem; }

.bn-tag-critical { color: #f87171; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em; }
.bn-tag-warning  { color: #fbbf24; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em; }
.bn-tag-good     { color: #4ade80; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em; }
.bn-tag-info     { color: #60a5fa; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em; }

.bn-title { font-size: 0.95rem; font-weight: 500; color: #e5e7eb; margin: 2px 0; }
.bn-desc  { font-size: 0.82rem; color: #9ca3af; margin-top: 4px; line-height: 1.55; }

.fps-card {
    background: #1a1d2e;
    border: 1px solid #2a2d3e;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.fps-game { font-size: 0.8rem; color: #9ca3af; margin-bottom: 4px; }
.fps-val  { font-size: 1.6rem; font-weight: 600; }
.fps-res  { font-size: 0.75rem; color: #6b7280; margin-top: 2px; }

.section-title {
    font-size: 1rem;
    font-weight: 500;
    color: #e5e7eb;
    margin: 1.8rem 0 0.8rem;
    padding-bottom: 6px;
    border-bottom: 1px solid #2a2d3e;
}

.upload-area {
    border: 2px dashed #2a2d3e;
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    background: #0f1117;
}

.stButton > button {
    background: linear-gradient(135deg, #4f8ef7, #7c3aed);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.5rem;
    font-weight: 500;
    width: 100%;
}

.info-note {
    background: #0c1a2e;
    border-left: 3px solid #4f8ef7;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    font-size: 0.82rem;
    color: #9ca3af;
    margin: 0.8rem 0;
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
    overall = analysis["overall_score"]
    percentile = analysis["global_percentile"]
    st.markdown(f"""
    <div style='background:#1a1d2e;border:1px solid #2a2d3e;border-radius:16px;padding:1.5rem;text-align:center;'>
        <div style='font-size:0.75rem;color:#6b7280;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:8px;'>Puntaje General</div>
        <div class='score-big'>{overall:.1f}</div>
        <div class='score-label'>de 9.9 máximo</div>
        <div style='display:inline-block;padding:4px 14px;border-radius:20px;font-size:0.78rem;font-weight:500;margin-top:10px;background:{tier_bg};color:{tier_color};'>
            {tier_icon} Gama {tier}
        </div>
        <div style='margin-top:12px;font-size:0.85rem;color:#9ca3af;'>Top <b style="color:#e5e7eb;">{percentile}%</b> global</div>
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
