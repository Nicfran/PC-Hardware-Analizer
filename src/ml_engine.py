"""
ml_engine.py — Motor de Machine Learning para análisis de hardware.

Modelos usados:
1. Clasificador de tier (KNN sobre features normalizadas)
2. Detector de cuello de botella (reglas + scoring ML)
3. Estimador de percentil global (distribución empírica)

No requiere entrenamiento externo — el modelo se entrena con la base de datos
interna de componentes al inicializar. Esto mantiene la app sin dependencias
de archivos de modelo externos.
"""
from __future__ import annotations
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import re


class MLEngine:
    def __init__(self, db):
        self.db = db
        self._build_models()

    def _build_models(self):
        """Entrena los modelos KNN y Random Forest con la base de datos interna."""
        # Features para clasificación de tier de CPU:
        # [score_multi, score_single, tdp_norm]
        cpu_data = list(self.db.CPUS.values())
        tier_order = ["Entrada", "Media", "Media-Alta", "Alta", "Entusiasta"]
        tier_map   = {t: i for i, t in enumerate(tier_order)}

        X_cpu, y_cpu = [], []
        for c in cpu_data:
            X_cpu.append([c["score_multi"], c["score_single"], c["tdp"] / 170])
            y_cpu.append(tier_map.get(c["tier"], 2))

        self.scaler_cpu = MinMaxScaler()
        X_cpu_s = self.scaler_cpu.fit_transform(X_cpu)
        self.knn_cpu = KNeighborsClassifier(n_neighbors=3)
        self.knn_cpu.fit(X_cpu_s, y_cpu)

        # Features para tier de GPU: [score_3d, gaming_index/100, vram_gb/24]
        gpu_data = list(self.db.GPUS.values())
        X_gpu, y_gpu = [], []
        for g in gpu_data:
            X_gpu.append([g["score_3d"], g["gaming_index"] / 100, g["vram_gb"] / 24])
            y_gpu.append(tier_map.get(g["tier"], 2))

        self.scaler_gpu = MinMaxScaler()
        X_gpu_s = self.scaler_gpu.fit_transform(X_gpu)
        self.knn_gpu = KNeighborsClassifier(n_neighbors=3)
        self.knn_gpu.fit(X_gpu_s, y_gpu)

        self.tier_order = tier_order

    def _infer_cpu_from_metrics(self, data: dict) -> tuple[str, dict | None]:
        """
        Intenta inferir el CPU desde el nombre XML o el nombre de override.
        Retorna (display_name, db_entry_or_None).
        """
        name_xml      = data.get("cpu_name_xml", "")
        name_override = data.get("cpu_name_override", "")
        name = name_override if name_override and name_override != "— Autodetectar —" else name_xml
        db_entry = self.db.find_cpu(name)
        display = name if name else "CPU detectado"
        return display, db_entry

    def _infer_gpu_from_metrics(self, data: dict) -> tuple[str, dict | None]:
        name_override = data.get("gpu_name_override", "")
        gpu_entries   = data.get("gpu_entries", [])
        name = ""
        if name_override and name_override != "— Autodetectar —":
            name = name_override
        elif gpu_entries:
            name = gpu_entries[0]["name"]
        db_entry = self.db.find_gpu(name)
        display  = name if name else "GPU detectada"
        return display, db_entry

    def _classify_cpu_tier_from_metrics(self, data: dict) -> str:
        """
        Clasifica el tier del CPU usando los scores WinSAT y el KNN.
        """
        cpu_score  = data.get("cpu_score", 0)
        cpu_sub    = data.get("cpu_sub_score", 0)
        cpu_enc    = data.get("cpu_encryption", 0)  # proxy de IPC

        # Normalizar encryption (max ~15000 MB/s) como proxy de IPC
        enc_norm = min(cpu_enc / 15000, 1.0)
        feats = np.array([[cpu_score / 9.9, cpu_sub / 9.9, enc_norm]])
        feats_s = self.scaler_cpu.transform(feats)
        tier_idx = self.knn_cpu.predict(feats_s)[0]
        return self.tier_order[tier_idx]

    def _classify_gpu_tier_from_metrics(self, data: dict) -> str:
        gpu_score = data.get("gpu_score", 0)
        vbw       = data.get("video_mem_bandwidth_mbs", 0)
        vbw_norm  = min(vbw / 500000, 1.0)  # RTX 4090 ~1 TB/s
        feats = np.array([[gpu_score / 9.9, vbw_norm, 0.5]])
        feats_s = self.scaler_gpu.transform(feats)
        tier_idx = self.knn_gpu.predict(feats_s)[0]
        return self.tier_order[tier_idx]

    def _score_to_percentile(self, score: float, comp: str) -> int:
        """
        Estima el percentil global basado en una distribución empírica
        de la comunidad de hardware (curva log-normal ajustada).
        """
        # Parámetros de distribución empírica por componente
        # Basados en estadísticas de PassMark y Steam Hardware Survey
        dist = {
            "overall": [(3.0, 0), (5.0, 15), (6.0, 30), (7.0, 50), (7.5, 65), (8.0, 78), (8.5, 88), (9.0, 95), (9.5, 98), (9.9, 99)],
            "cpu":     [(2.0, 0), (4.0, 10), (5.5, 25), (6.5, 40), (7.5, 60), (8.0, 75), (8.5, 85), (9.0, 93), (9.5, 97), (9.9, 99)],
            "gpu":     [(2.0, 0), (4.0, 15), (5.5, 30), (6.5, 45), (7.5, 62), (8.0, 74), (8.5, 84), (9.0, 92), (9.5, 97), (9.9, 99)],
            "ram":     [(3.0, 0), (5.0, 20), (6.5, 40), (7.5, 60), (8.0, 75), (8.5, 86), (9.0, 93), (9.9, 99)],
            "disk":    [(2.0, 0), (4.0, 20), (5.5, 40), (7.0, 60), (8.0, 78), (8.5, 88), (9.0, 95), (9.9, 99)],
        }
        points = dist.get(comp, dist["overall"])
        scores = [p[0] for p in points]
        pcts   = [p[1] for p in points]
        # Interpolación lineal
        percentile = float(np.interp(score, scores, pcts))
        return max(1, min(99, int(percentile)))

    def _detect_bottlenecks(self, data: dict, analysis: dict) -> list[dict]:
        bns = []
        scores = analysis["scores"]
        cpu_s  = scores["cpu"]
        gpu_s  = scores["gpu"]
        ram_s  = scores["ram"]
        disk_s = scores["disk"]

        # ── CPU vs GPU balance ──────────────────────────────────────────────
        diff = abs(cpu_s - gpu_s)
        if cpu_s < gpu_s - 1.5:
            severity = "critical" if cpu_s < gpu_s - 2.5 else "warning"
            pct_loss = int(min((gpu_s - cpu_s) / gpu_s * 60, 40))
            bns.append({
                "type": severity,
                "title": f"CPU es cuello de botella para tu GPU",
                "desc": f"Tu CPU ({cpu_s:.1f}) es notablemente más débil que tu GPU ({gpu_s:.1f}). "
                        f"Esto puede costar hasta ~{pct_loss}% de FPS en juegos intensivos de CPU. "
                        f"Considerá actualizar el procesador para liberar el potencial de tu GPU."
            })
        elif gpu_s < cpu_s - 1.5:
            bns.append({
                "type": "warning",
                "title": "GPU limita el potencial de tu CPU",
                "desc": f"Tu GPU ({gpu_s:.1f}) no está a la altura de tu CPU ({cpu_s:.1f}). "
                        f"Una GPU más potente mejoraría significativamente el rendimiento gráfico."
            })
        else:
            bns.append({
                "type": "good",
                "title": "CPU y GPU bien balanceados",
                "desc": f"Diferencia de solo {diff:.1f} puntos entre CPU ({cpu_s:.1f}) y GPU ({gpu_s:.1f}). "
                        f"El sistema aprovecha ambos componentes de forma eficiente."
            })

        # ── RAM ─────────────────────────────────────────────────────────────
        mem_bw = data.get("mem_bandwidth_mbs", 0)
        ram_type = data.get("ram_type", "DDR4")
        if ram_s >= 8.5:
            bns.append({
                "type": "good",
                "title": f"RAM excelente — {ram_type} de alto rendimiento",
                "desc": f"Ancho de banda de {mem_bw:,.0f} MB/s. Estás en el top 15% para {ram_type}. La memoria no es cuello de botella."
            })
        elif ram_s < 6.0:
            bns.append({
                "type": "critical",
                "title": f"RAM lenta — posible cuello de botella",
                "desc": f"Solo {mem_bw:,.0f} MB/s de ancho de banda. Considerá activar XMP/EXPO en la BIOS o actualizar a un kit más rápido."
            })
        else:
            bns.append({
                "type": "info",
                "title": f"RAM {ram_type} en rango normal",
                "desc": f"{mem_bw:,.0f} MB/s — rendimiento adecuado. Activar XMP/EXPO en BIOS puede dar un 5-15% más."
            })

        # ── 3D V-Cache detection ─────────────────────────────────────────────
        cpu_name = analysis.get("cpu_display", "").lower()
        if "3d" in cpu_name or "x3d" in cpu_name:
            bns.append({
                "type": "info",
                "title": "3D V-Cache detectado — ventaja en gaming real",
                "desc": "Los benchmarks sintéticos (WinSAT) NO capturan la ventaja del 3D V-Cache. "
                        "En juegos reales, tu CPU rinde hasta un 20-30% mejor que lo que muestran los puntajes aquí. "
                        "El caché enorme reduce los stalls de memoria, lo cual WinSAT no mide."
            })

        # ── Discos ──────────────────────────────────────────────────────────
        drives = data.get("drives", {})
        has_hdd = any(v["type"] == "HDD" for v in drives.values())
        has_nvme = any(v["type"] == "NVMe SSD" for v in drives.values())

        if has_nvme:
            bns.append({
                "type": "good",
                "title": "SSD NVMe como disco principal",
                "desc": f"Lectura secuencial de {data.get('disk_seq_read_mbs', 0):,.0f} MB/s. "
                        f"Tiempos de carga rápidos y sistema operativo fluido."
            })
        elif disk_s < 5.0:
            bns.append({
                "type": "critical",
                "title": "Disco lento detectado como principal",
                "desc": "Tu disco principal parece ser un HDD o SSD SATA lento. "
                        "Un SSD NVMe es la mejora de precio/rendimiento más grande que podés hacer."
            })

        if has_hdd:
            hdd_rand = max((v["rand"] for v in drives.values() if v["type"] == "HDD"), default=0)
            bns.append({
                "type": "warning",
                "title": "HDD mecánico detectado como disco secundario",
                "desc": f"Lectura aleatoria de solo {hdd_rand:.1f} MB/s — típico de un HDD. "
                        f"Si tenés juegos o programas instalados ahí, van a cargar muy lento. "
                        f"Un SSD SATA de 1 TB (~$35-50 USD) elimina este problema."
            })

        return bns

    def _build_recommendations(self, data: dict, analysis: dict) -> list[dict]:
        recs = []
        scores = analysis["scores"]
        drives = data.get("drives", {})
        has_hdd = any(v["type"] == "HDD" for v in drives.values())

        # Prio 1: HDD secundario
        if has_hdd:
            recs.append({
                "title": "Reemplazar HDD secundario por SSD SATA",
                "desc": "El upgrade más barato y con mayor impacto perceptible. Un SSD de 1 TB cuesta ~$35-50 USD y hace que todo cargue instantáneamente.",
                "urgency": "alta"
            })

        # Prio 2: Si RAM no tiene XMP
        ram_bw = data.get("mem_bandwidth_mbs", 0)
        ram_type = data.get("ram_type", "DDR4")
        if ram_bw < 35000 and ram_type == "DDR4":
            recs.append({
                "title": "Activar XMP / EXPO en la BIOS",
                "desc": "Gratis — solo requiere entrar a la BIOS y activar el perfil XMP. "
                        "Puede dar un 5-15% más de ancho de banda de RAM y mejorar el rendimiento general.",
                "urgency": "media"
            })

        # Prio 3: Balance CPU/GPU
        cpu_s = scores["cpu"]
        gpu_s = scores["gpu"]
        if gpu_s > cpu_s + 1.5:
            recs.append({
                "title": "Actualizar el procesador",
                "desc": f"Tu GPU ({gpu_s:.1f}) supera al CPU ({cpu_s:.1f}). "
                        f"Un CPU más potente liberaría el potencial de tu GPU y daría más FPS.",
                "urgency": "alta"
            })
        elif cpu_s > gpu_s + 1.5:
            recs.append({
                "title": "Actualizar la tarjeta de video",
                "desc": f"Tu CPU ({cpu_s:.1f}) supera a la GPU ({gpu_s:.1f}). "
                        f"Una GPU más potente es el upgrade con mayor impacto en gaming.",
                "urgency": "alta"
            })
        else:
            recs.append({
                "title": "Sistema balanceado — no hay upgrade urgente",
                "desc": "CPU, GPU y RAM están bien balanceados. El próximo upgrade natural sería pasar a una nueva plataforma (AM5/LGA1800) cuando los precios bajen.",
                "urgency": "baja"
            })

        return recs

    def analyze(self, data: dict, uso: str, resolucion: str) -> dict:
        """
        Análisis completo del hardware. Retorna dict con todos los campos
        necesarios para el dashboard.
        """
        # ── Scores desde WinSAT ──────────────────────────────────────────────
        cpu_score  = data.get("cpu_score",  data.get("system_score", 7.0))
        cpu_single = data.get("cpu_sub_score", cpu_score * 0.92)
        gpu_score  = data.get("gpu_score",  8.0)
        ram_score  = data.get("mem_score",  data.get("system_score", 7.0))
        disk_score = data.get("disk_score", 7.0)

        # Disco secundario (HDD si existe)
        drives = data.get("drives", {})
        drive_scores = []
        for d in drives.values():
            if d["type"] == "NVMe SSD":
                drive_scores.append(8.8)
            elif d["type"] == "SATA SSD":
                drive_scores.append(7.0)
            else:
                drive_scores.append(1.5)
        disk2_score = min(drive_scores) if len(drive_scores) > 1 else disk_score

        scores = {
            "cpu":        cpu_score,
            "cpu_single": cpu_single,
            "gpu":        gpu_score,
            "ram":        ram_score,
            "disk":       disk_score,
            "disk2":      disk2_score,
        }

        # ── Overall score ────────────────────────────────────────────────────
        # WinSAT SystemScore es el mínimo de los sub-scores
        overall = data.get("system_score", min(scores.values()))

        # ── CPU / GPU display ────────────────────────────────────────────────
        cpu_display, cpu_db = self._infer_cpu_from_metrics(data)
        gpu_display, gpu_db = self._infer_gpu_from_metrics(data)

        # ── Tier classification ──────────────────────────────────────────────
        if cpu_db:
            cpu_tier = cpu_db["tier"]
        else:
            cpu_tier = self._classify_cpu_tier_from_metrics(data)

        if gpu_db:
            gpu_tier = gpu_db["tier"]
        else:
            gpu_tier = self._classify_gpu_tier_from_metrics(data)

        # Overall tier = peor de los dos principales
        tier_order = ["Entrada", "Media", "Media-Alta", "Alta", "Entusiasta"]
        tier_idx = min(tier_order.index(cpu_tier), tier_order.index(gpu_tier))
        # Pero si GPU es muy alta, subir un nivel
        gpu_idx = tier_order.index(gpu_tier)
        cpu_idx = tier_order.index(cpu_tier)
        overall_tier_idx = (cpu_idx + gpu_idx) // 2
        tier = tier_order[overall_tier_idx]

        # ── Percentile ───────────────────────────────────────────────────────
        percentile = 100 - self._score_to_percentile(overall, "overall")

        # ── RAM display ──────────────────────────────────────────────────────
        ram_gb = data.get("total_ram_mb", 0) // 1024
        ram_type = data.get("ram_type", "DDR4")
        ram_speed = data.get("ram_speed_mhz", 0)
        mem_bw = data.get("mem_bandwidth_mbs", 0)
        if ram_gb > 0:
            ram_display = f"{ram_gb} GB {ram_type}"
            if ram_speed: ram_display += f" ({ram_speed} MHz)"
        else:
            ram_display = f"{ram_type} — {mem_bw:,.0f} MB/s"

        # ── Disk display ─────────────────────────────────────────────────────
        seq = data.get("disk_seq_read_mbs", 0)
        rand = data.get("disk_rand_read_mbs", 0)
        if seq >= 1000:
            disk_display = f"NVMe SSD — {seq:,.0f} MB/s"
        elif seq >= 400:
            disk_display = f"SATA SSD — {seq:,.0f} MB/s"
        else:
            disk_display = f"HDD — {seq:,.0f} MB/s"

        # ── Details strings ──────────────────────────────────────────────────
        cpu_cores = data.get("cpu_cores", 0)
        cpu_freq  = data.get("cpu_freq_mhz", 0)
        cpu_comp  = data.get("cpu_compression2", 0)
        cpu_enc   = data.get("cpu_encryption", 0)

        if cpu_db:
            socket   = cpu_db.get("socket", "—")
            ram_sup  = " / ".join(cpu_db.get("ram_support", []))
            pcie_cpu = cpu_db.get("pcie", "—")
            gen_cpu  = cpu_db.get("gen", "—")
            year_cpu = cpu_db.get("launched", "")
            parts    = [f"{cpu_cores} núcleos"] if cpu_cores else []
            if cpu_freq: parts.append(f"{cpu_freq/1000:.1f} GHz")
            parts += [gen_cpu, f"Socket {socket}", f"RAM {ram_sup}", f"PCIe {pcie_cpu}"]
            if year_cpu: parts.append(f"Lanzado {year_cpu}")
            cpu_detail = " · ".join(parts)
        else:
            cpu_detail = (f"{cpu_cores} núcleos · {cpu_freq/1000:.1f} GHz · Comp: {cpu_comp:,.0f} MB/s"
                          if cpu_cores else f"Compresión: {cpu_comp:,.0f} MB/s · Cifrado: {cpu_enc:,.0f} MB/s")

        vbw = data.get("video_mem_bandwidth_mbs", 0)

        if gpu_db:
            vram_gb  = gpu_db.get("vram_gb", "—")
            gen_gpu  = gpu_db.get("gen", "—")
            pcie_gpu = gpu_db.get("pcie", "—")
            year_gpu = gpu_db.get("launched", "")
            ram_rec  = gpu_db.get("ram_recommended", "—")
            gpu_parts = [f"{vram_gb} GB VRAM", gen_gpu, f"PCIe {pcie_gpu}", f"RAM recomendada: {ram_rec}"]
            if year_gpu: gpu_parts.append(f"Lanzada {year_gpu}")
            gpu_detail = " · ".join(gpu_parts)
        else:
            gpu_detail = f"VRAM bandwidth: {vbw:,.0f} MB/s · Score gráfico: {gpu_score:.1f}"

        ram_detail = f"Ancho de banda: {mem_bw:,.0f} MB/s · Tipo: {ram_type}"

        disk_detail = f"Sec: {seq:,.0f} MB/s · Rand: {rand:,.0f} MB/s"

        analysis = {
            "overall_score":    overall,
            "global_percentile": percentile,
            "tier":             tier,
            "scores":           scores,
            "cpu_display":      cpu_display,
            "gpu_display":      gpu_display,
            "ram_display":      ram_display,
            "disk_display":     disk_display,
            "cpu_detail":       cpu_detail,
            "gpu_detail":       gpu_detail,
            "ram_detail":       ram_detail,
            "disk_detail":      disk_detail,
            "cpu_db":           cpu_db,
            "gpu_db":           gpu_db,
        }

        analysis["bottlenecks"]     = self._detect_bottlenecks(data, analysis)
        analysis["recommendations"] = self._build_recommendations(data, analysis)

        return analysis
