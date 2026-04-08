# 🖥️ PC Hardware Analyzer — WinSAT + ML

Analizá el hardware de tu PC de forma automática subiendo el archivo XML de WinSAT.
La app usa Machine Learning para clasificar componentes, detectar cuellos de botella
y predecir FPS en juegos populares.

---

## ¿Cómo obtener el archivo WinSAT?

1. Abrí **PowerShell como Administrador** (Win + X → Terminal Administrador)
2. Ejecutá:
   ```
   winsat formal
   ```
3. Esperá 5-10 minutos a que termine
4. El archivo XML está en:
   ```
   C:\Windows\Performance\WinSAT\DataStore\
   ```
   Buscá el que dice `Formal.Assessment (Recent).WinSAT.xml`

---

## Instalación local

### Requisitos
- Python 3.10 o superior
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/winsat-analyzer.git
cd winsat-analyzer

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la app
streamlit run app.py
```

La app se abre automáticamente en `http://localhost:8501`

---

## Deploy en Streamlit Cloud (gratis)

1. Subí este proyecto a un repositorio de GitHub
2. Entrá a [share.streamlit.io](https://share.streamlit.io)
3. Conectá tu cuenta de GitHub
4. Seleccioná el repositorio y `app.py` como archivo principal
5. Click en **Deploy** — listo en 2 minutos

---

## Estructura del proyecto

```
winsat-analyzer/
├── app.py                  # App principal Streamlit
├── requirements.txt        # Dependencias Python
├── README.md
└── src/
    ├── __init__.py
    ├── parser.py           # Parseo del XML de WinSAT (UTF-16)
    ├── benchmark_db.py     # Base de datos de componentes y benchmarks
    ├── ml_engine.py        # Motor ML: clasificación + cuello de botella
    └── fps_predictor.py    # Predicción de FPS por juego (GradientBoosting)
```

---

## Cómo funciona el ML

| Módulo | Algoritmo | Qué hace |
|--------|-----------|----------|
| Clasificación de tier | K-Nearest Neighbors | Clasifica CPU/GPU en Entrada/Media/Alta/Entusiasta |
| Detección de cuello de botella | Reglas + scoring | Detecta si CPU, GPU, RAM o disco limitan el sistema |
| Predicción de FPS | Gradient Boosting Regressor | Predice FPS por juego según gaming_index + resolución |
| Percentil global | Interpolación empírica | Estima posición vs población global (basado en PassMark/Steam Survey) |

Los modelos se entrenan al iniciar la app con la base de datos interna — no requieren archivos de modelo externos.

---

## Funcionalidades

- **Subida de XML**: Drag & drop del archivo WinSAT
- **Override manual**: Si sabés tu CPU/GPU exacto, podés especificarlo en el panel lateral
- **Score general**: Puntaje WinSAT con percentil global estimado
- **Radar de rendimiento**: Comparativa visual vs top global por componente
- **Cuello de botella**: Detección automática con explicaciones en lenguaje simple
- **FPS predichos**: 12 juegos populares en 1080p/1440p/4K
- **Comparativa**: Tu setup vs configuraciones populares del mercado
- **Recomendaciones**: Qué mejorar y en qué orden de prioridad

---

## Notas

- Los FPS son **estimaciones** basadas en benchmarks públicos. Pueden variar según la calidad del driver, temperatura, y configuración del juego.
- WinSAT **no mide** el 3D V-Cache (Ryzen X3D). La app lo detecta y lo aclara en el análisis.
- El archivo XML puede pesar entre 500 KB y 2 MB — es normal.

---

## Licencia

MIT — libre para usar, modificar y distribuir.
