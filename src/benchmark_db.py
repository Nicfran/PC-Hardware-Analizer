"""
benchmark_db.py — Base de datos de benchmarks de componentes.
Actualizado: 2025/2026
Fuentes: PassMark, TechPowerUp, Gamers Nexus, Digital Foundry, Tom's Hardware.

Campos CPU: score_multi, score_single, tier, tdp, gen, socket, ram_support, pcie, launched
Campos GPU: score_3d, gaming_index, vram_gb, tier, gen, pcie, launched, ram_recommended
"""
from __future__ import annotations


class BenchmarkDB:

    CPUS = {

        # ── AMD Ryzen 3000 (Zen 2) — AM4 ────────────────────────────────────
        "ryzen 5 3600":      {"score_multi":5.8,"score_single":6.2,"tier":"Media",      "tdp":65, "gen":"Zen 2",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2019},
        "ryzen 5 3600x":     {"score_multi":6.0,"score_single":6.4,"tier":"Media",      "tdp":95, "gen":"Zen 2",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2019},
        "ryzen 7 3700x":     {"score_multi":6.6,"score_single":6.3,"tier":"Media-Alta", "tdp":65, "gen":"Zen 2",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2019},
        "ryzen 7 3800x":     {"score_multi":6.8,"score_single":6.4,"tier":"Media-Alta", "tdp":105,"gen":"Zen 2",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2019},
        "ryzen 9 3900x":     {"score_multi":7.8,"score_single":6.4,"tier":"Alta",       "tdp":105,"gen":"Zen 2",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2019},
        "ryzen 9 3950x":     {"score_multi":8.4,"score_single":6.4,"tier":"Alta",       "tdp":105,"gen":"Zen 2",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2019},

        # ── AMD Ryzen 5000 (Zen 3 / Zen 3D) — AM4 ───────────────────────────
        "ryzen 3 5300g":     {"score_multi":4.8,"score_single":7.2,"tier":"Entrada",    "tdp":65, "gen":"Zen 3",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"3.0","launched":2021},
        "ryzen 5 5500":      {"score_multi":6.4,"score_single":7.4,"tier":"Media",      "tdp":65, "gen":"Zen 3",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"3.0","launched":2022},
        "ryzen 5 5600":      {"score_multi":7.2,"score_single":7.8,"tier":"Media-Alta", "tdp":65, "gen":"Zen 3",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2021},
        "ryzen 5 5600g":     {"score_multi":6.8,"score_single":7.6,"tier":"Media",      "tdp":65, "gen":"Zen 3",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"3.0","launched":2021},
        "ryzen 5 5600x":     {"score_multi":7.4,"score_single":8.0,"tier":"Media-Alta", "tdp":65, "gen":"Zen 3",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2020},
        "ryzen 5 5600x3d":   {"score_multi":7.5,"score_single":7.9,"tier":"Media-Alta", "tdp":65, "gen":"Zen 3 3D", "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2023},
        "ryzen 7 5700":      {"score_multi":7.6,"score_single":7.7,"tier":"Media-Alta", "tdp":65, "gen":"Zen 3",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2022},
        "ryzen 7 5700g":     {"score_multi":7.4,"score_single":7.6,"tier":"Media-Alta", "tdp":65, "gen":"Zen 3",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"3.0","launched":2021},
        "ryzen 7 5700x":     {"score_multi":7.9,"score_single":7.9,"tier":"Alta",       "tdp":65, "gen":"Zen 3",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2022},
        "ryzen 7 5700x3d":   {"score_multi":8.0,"score_single":7.8,"tier":"Alta",       "tdp":65, "gen":"Zen 3 3D", "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2024},
        "ryzen 7 5800x":     {"score_multi":8.2,"score_single":8.1,"tier":"Alta",       "tdp":105,"gen":"Zen 3",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2020},
        "ryzen 7 5800x3d":   {"score_multi":8.2,"score_single":7.9,"tier":"Entusiasta", "tdp":105,"gen":"Zen 3 3D", "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2022},
        "ryzen 9 5900x":     {"score_multi":8.9,"score_single":8.2,"tier":"Entusiasta", "tdp":105,"gen":"Zen 3",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2020},
        "ryzen 9 5950x":     {"score_multi":9.3,"score_single":8.2,"tier":"Entusiasta", "tdp":105,"gen":"Zen 3",    "socket":"AM4","ram_support":["DDR4"],         "pcie":"4.0","launched":2020},

        # ── AMD Ryzen 7000 (Zen 4 / Zen 4D) — AM5 ───────────────────────────
        "ryzen 5 7600":      {"score_multi":8.0,"score_single":9.0,"tier":"Alta",       "tdp":65, "gen":"Zen 4",    "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2022},
        "ryzen 5 7600x":     {"score_multi":8.2,"score_single":9.1,"tier":"Alta",       "tdp":105,"gen":"Zen 4",    "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2022},
        "ryzen 5 7600x3d":   {"score_multi":8.3,"score_single":9.0,"tier":"Alta",       "tdp":105,"gen":"Zen 4 3D", "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2024},
        "ryzen 7 7700":      {"score_multi":8.6,"score_single":9.0,"tier":"Alta",       "tdp":65, "gen":"Zen 4",    "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2022},
        "ryzen 7 7700x":     {"score_multi":8.8,"score_single":9.2,"tier":"Entusiasta", "tdp":105,"gen":"Zen 4",    "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2022},
        "ryzen 7 7800x3d":   {"score_multi":8.7,"score_single":9.0,"tier":"Entusiasta", "tdp":120,"gen":"Zen 4 3D", "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2023},
        "ryzen 9 7900":      {"score_multi":9.0,"score_single":9.1,"tier":"Entusiasta", "tdp":65, "gen":"Zen 4",    "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2022},
        "ryzen 9 7900x":     {"score_multi":9.3,"score_single":9.2,"tier":"Entusiasta", "tdp":170,"gen":"Zen 4",    "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2022},
        "ryzen 9 7900x3d":   {"score_multi":9.3,"score_single":9.0,"tier":"Entusiasta", "tdp":120,"gen":"Zen 4 3D", "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2023},
        "ryzen 9 7950x":     {"score_multi":9.7,"score_single":9.2,"tier":"Entusiasta", "tdp":170,"gen":"Zen 4",    "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2022},
        "ryzen 9 7950x3d":   {"score_multi":9.8,"score_single":9.0,"tier":"Entusiasta", "tdp":120,"gen":"Zen 4 3D", "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2023},

        # ── AMD Ryzen 9000 (Zen 5 / Zen 5D) — AM5  [2024/2025] ─────────────
        "ryzen 5 9600":      {"score_multi":8.3,"score_single":9.4,"tier":"Alta",       "tdp":65, "gen":"Zen 5",    "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2024},
        "ryzen 5 9600x":     {"score_multi":8.5,"score_single":9.5,"tier":"Alta",       "tdp":105,"gen":"Zen 5",    "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2024},
        "ryzen 7 9700x":     {"score_multi":9.0,"score_single":9.5,"tier":"Entusiasta", "tdp":65, "gen":"Zen 5",    "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2024},
        "ryzen 7 9800x3d":   {"score_multi":9.1,"score_single":9.4,"tier":"Entusiasta", "tdp":120,"gen":"Zen 5 3D", "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2024},
        "ryzen 9 9900x":     {"score_multi":9.5,"score_single":9.5,"tier":"Entusiasta", "tdp":120,"gen":"Zen 5",    "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2024},
        "ryzen 9 9950x":     {"score_multi":9.8,"score_single":9.6,"tier":"Entusiasta", "tdp":170,"gen":"Zen 5",    "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2024},
        "ryzen 9 9950x3d":   {"score_multi":9.9,"score_single":9.5,"tier":"Entusiasta", "tdp":170,"gen":"Zen 5 3D", "socket":"AM5","ram_support":["DDR5"],         "pcie":"5.0","launched":2025},

        # ── Intel 10th Gen (Comet Lake) — LGA1200 ───────────────────────────
        "core i3-10100":     {"score_multi":4.2,"score_single":6.8,"tier":"Entrada",    "tdp":65, "gen":"Comet Lake",   "socket":"LGA1200","ram_support":["DDR4"],"pcie":"3.0","launched":2020},
        "core i3-10100f":    {"score_multi":4.2,"score_single":6.8,"tier":"Entrada",    "tdp":65, "gen":"Comet Lake",   "socket":"LGA1200","ram_support":["DDR4"],"pcie":"3.0","launched":2020},
        "core i5-10400":     {"score_multi":5.6,"score_single":7.0,"tier":"Media",      "tdp":65, "gen":"Comet Lake",   "socket":"LGA1200","ram_support":["DDR4"],"pcie":"3.0","launched":2020},
        "core i5-10400f":    {"score_multi":5.6,"score_single":7.0,"tier":"Media",      "tdp":65, "gen":"Comet Lake",   "socket":"LGA1200","ram_support":["DDR4"],"pcie":"3.0","launched":2020},
        "core i5-10600k":    {"score_multi":6.2,"score_single":7.4,"tier":"Media",      "tdp":125,"gen":"Comet Lake",   "socket":"LGA1200","ram_support":["DDR4"],"pcie":"3.0","launched":2020},
        "core i7-10700k":    {"score_multi":6.8,"score_single":7.5,"tier":"Media-Alta", "tdp":125,"gen":"Comet Lake",   "socket":"LGA1200","ram_support":["DDR4"],"pcie":"3.0","launched":2020},
        "core i9-10900k":    {"score_multi":7.4,"score_single":7.6,"tier":"Alta",       "tdp":125,"gen":"Comet Lake",   "socket":"LGA1200","ram_support":["DDR4"],"pcie":"3.0","launched":2020},

        # ── Intel 11th Gen (Rocket Lake) — LGA1200 ──────────────────────────
        "core i5-11400":     {"score_multi":6.4,"score_single":7.6,"tier":"Media",      "tdp":65, "gen":"Rocket Lake",  "socket":"LGA1200","ram_support":["DDR4"],"pcie":"4.0","launched":2021},
        "core i5-11400f":    {"score_multi":6.4,"score_single":7.6,"tier":"Media",      "tdp":65, "gen":"Rocket Lake",  "socket":"LGA1200","ram_support":["DDR4"],"pcie":"4.0","launched":2021},
        "core i5-11600k":    {"score_multi":6.8,"score_single":8.0,"tier":"Media-Alta", "tdp":125,"gen":"Rocket Lake",  "socket":"LGA1200","ram_support":["DDR4"],"pcie":"4.0","launched":2021},
        "core i7-11700k":    {"score_multi":7.4,"score_single":8.1,"tier":"Media-Alta", "tdp":125,"gen":"Rocket Lake",  "socket":"LGA1200","ram_support":["DDR4"],"pcie":"4.0","launched":2021},
        "core i9-11900k":    {"score_multi":7.6,"score_single":8.2,"tier":"Alta",       "tdp":125,"gen":"Rocket Lake",  "socket":"LGA1200","ram_support":["DDR4"],"pcie":"4.0","launched":2021},

        # ── Intel 12th Gen (Alder Lake) — LGA1700 ───────────────────────────
        "core i3-12100":     {"score_multi":5.8,"score_single":8.0,"tier":"Entrada",    "tdp":60, "gen":"Alder Lake",   "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2022},
        "core i3-12100f":    {"score_multi":5.8,"score_single":8.0,"tier":"Entrada",    "tdp":58, "gen":"Alder Lake",   "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2022},
        "core i5-12400":     {"score_multi":7.5,"score_single":8.4,"tier":"Media-Alta", "tdp":65, "gen":"Alder Lake",   "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2022},
        "core i5-12400f":    {"score_multi":7.5,"score_single":8.4,"tier":"Media-Alta", "tdp":65, "gen":"Alder Lake",   "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2022},
        "core i5-12600k":    {"score_multi":8.1,"score_single":8.6,"tier":"Alta",       "tdp":125,"gen":"Alder Lake",   "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2021},
        "core i5-12600kf":   {"score_multi":8.1,"score_single":8.6,"tier":"Alta",       "tdp":125,"gen":"Alder Lake",   "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2021},
        "core i7-12700":     {"score_multi":8.4,"score_single":8.6,"tier":"Alta",       "tdp":65, "gen":"Alder Lake",   "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2021},
        "core i7-12700k":    {"score_multi":8.6,"score_single":8.7,"tier":"Alta",       "tdp":125,"gen":"Alder Lake",   "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2021},
        "core i7-12700kf":   {"score_multi":8.6,"score_single":8.7,"tier":"Alta",       "tdp":125,"gen":"Alder Lake",   "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2021},
        "core i9-12900k":    {"score_multi":9.0,"score_single":8.8,"tier":"Entusiasta", "tdp":125,"gen":"Alder Lake",   "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2021},
        "core i9-12900ks":   {"score_multi":9.1,"score_single":8.9,"tier":"Entusiasta", "tdp":150,"gen":"Alder Lake",   "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2022},

        # ── Intel 13th Gen (Raptor Lake) — LGA1700 ──────────────────────────
        "core i3-13100":     {"score_multi":6.2,"score_single":8.3,"tier":"Entrada",    "tdp":60, "gen":"Raptor Lake",  "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2023},
        "core i3-13100f":    {"score_multi":6.2,"score_single":8.3,"tier":"Entrada",    "tdp":58, "gen":"Raptor Lake",  "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2023},
        "core i5-13400":     {"score_multi":8.0,"score_single":8.6,"tier":"Alta",       "tdp":65, "gen":"Raptor Lake",  "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2023},
        "core i5-13400f":    {"score_multi":8.0,"score_single":8.6,"tier":"Alta",       "tdp":65, "gen":"Raptor Lake",  "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2023},
        "core i5-13600k":    {"score_multi":8.7,"score_single":8.9,"tier":"Alta",       "tdp":125,"gen":"Raptor Lake",  "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2022},
        "core i5-13600kf":   {"score_multi":8.7,"score_single":8.9,"tier":"Alta",       "tdp":125,"gen":"Raptor Lake",  "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2022},
        "core i7-13700":     {"score_multi":8.9,"score_single":8.9,"tier":"Entusiasta", "tdp":65, "gen":"Raptor Lake",  "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2023},
        "core i7-13700k":    {"score_multi":9.1,"score_single":9.0,"tier":"Entusiasta", "tdp":125,"gen":"Raptor Lake",  "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2022},
        "core i7-13700kf":   {"score_multi":9.1,"score_single":9.0,"tier":"Entusiasta", "tdp":125,"gen":"Raptor Lake",  "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2022},
        "core i9-13900":     {"score_multi":9.3,"score_single":9.1,"tier":"Entusiasta", "tdp":65, "gen":"Raptor Lake",  "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2023},
        "core i9-13900k":    {"score_multi":9.5,"score_single":9.1,"tier":"Entusiasta", "tdp":125,"gen":"Raptor Lake",  "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2022},
        "core i9-13900ks":   {"score_multi":9.6,"score_single":9.2,"tier":"Entusiasta", "tdp":150,"gen":"Raptor Lake",  "socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2023},

        # ── Intel 14th Gen (Raptor Lake Refresh) — LGA1700 ──────────────────
        "core i5-14400":     {"score_multi":8.1,"score_single":8.7,"tier":"Alta",       "tdp":65, "gen":"Raptor Lake R","socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2024},
        "core i5-14400f":    {"score_multi":8.1,"score_single":8.7,"tier":"Alta",       "tdp":65, "gen":"Raptor Lake R","socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2024},
        "core i5-14600k":    {"score_multi":8.8,"score_single":9.0,"tier":"Alta",       "tdp":125,"gen":"Raptor Lake R","socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2023},
        "core i5-14600kf":   {"score_multi":8.8,"score_single":9.0,"tier":"Alta",       "tdp":125,"gen":"Raptor Lake R","socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2023},
        "core i7-14700":     {"score_multi":9.0,"score_single":9.0,"tier":"Entusiasta", "tdp":65, "gen":"Raptor Lake R","socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2024},
        "core i7-14700k":    {"score_multi":9.2,"score_single":9.1,"tier":"Entusiasta", "tdp":125,"gen":"Raptor Lake R","socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2023},
        "core i7-14700kf":   {"score_multi":9.2,"score_single":9.1,"tier":"Entusiasta", "tdp":125,"gen":"Raptor Lake R","socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2023},
        "core i9-14900":     {"score_multi":9.4,"score_single":9.1,"tier":"Entusiasta", "tdp":65, "gen":"Raptor Lake R","socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2024},
        "core i9-14900k":    {"score_multi":9.6,"score_single":9.2,"tier":"Entusiasta", "tdp":125,"gen":"Raptor Lake R","socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2023},
        "core i9-14900ks":   {"score_multi":9.7,"score_single":9.3,"tier":"Entusiasta", "tdp":150,"gen":"Raptor Lake R","socket":"LGA1700","ram_support":["DDR4","DDR5"],"pcie":"5.0","launched":2024},

        # ── Intel Core Ultra (Arrow Lake) — LGA1851  [2024/2025] ────────────
        "core ultra 5 245k":  {"score_multi":8.8,"score_single":9.0,"tier":"Alta",       "tdp":125,"gen":"Arrow Lake","socket":"LGA1851","ram_support":["DDR5"],    "pcie":"5.0","launched":2024},
        "core ultra 7 265k":  {"score_multi":9.3,"score_single":9.1,"tier":"Entusiasta", "tdp":125,"gen":"Arrow Lake","socket":"LGA1851","ram_support":["DDR5"],    "pcie":"5.0","launched":2024},
        "core ultra 9 285k":  {"score_multi":9.6,"score_single":9.2,"tier":"Entusiasta", "tdp":125,"gen":"Arrow Lake","socket":"LGA1851","ram_support":["DDR5"],    "pcie":"5.0","launched":2024},
    }

    GPUS = {

        # ── NVIDIA GTX Pascal / Turing ───────────────────────────────────────
        "gtx 1050 ti":       {"score_3d":2.8,"gaming_index":10,"vram_gb":4, "tier":"Entrada",    "gen":"Pascal",       "pcie":"3.0","launched":2016,"ram_recommended":"DDR4"},
        "gtx 1060 3gb":      {"score_3d":3.2,"gaming_index":13,"vram_gb":3, "tier":"Entrada",    "gen":"Pascal",       "pcie":"3.0","launched":2016,"ram_recommended":"DDR4"},
        "gtx 1060 6gb":      {"score_3d":3.8,"gaming_index":16,"vram_gb":6, "tier":"Entrada",    "gen":"Pascal",       "pcie":"3.0","launched":2016,"ram_recommended":"DDR4"},
        "gtx 1070":          {"score_3d":4.8,"gaming_index":22,"vram_gb":8, "tier":"Media",      "gen":"Pascal",       "pcie":"3.0","launched":2016,"ram_recommended":"DDR4"},
        "gtx 1080":          {"score_3d":5.5,"gaming_index":27,"vram_gb":8, "tier":"Media",      "gen":"Pascal",       "pcie":"3.0","launched":2016,"ram_recommended":"DDR4"},
        "gtx 1080 ti":       {"score_3d":6.2,"gaming_index":34,"vram_gb":11,"tier":"Media-Alta", "gen":"Pascal",       "pcie":"3.0","launched":2017,"ram_recommended":"DDR4"},
        "gtx 1650":          {"score_3d":3.0,"gaming_index":12,"vram_gb":4, "tier":"Entrada",    "gen":"Turing",       "pcie":"3.0","launched":2019,"ram_recommended":"DDR4"},
        "gtx 1650 super":    {"score_3d":3.6,"gaming_index":16,"vram_gb":4, "tier":"Entrada",    "gen":"Turing",       "pcie":"3.0","launched":2019,"ram_recommended":"DDR4"},
        "gtx 1660":          {"score_3d":4.4,"gaming_index":21,"vram_gb":6, "tier":"Media",      "gen":"Turing",       "pcie":"3.0","launched":2019,"ram_recommended":"DDR4"},
        "gtx 1660 super":    {"score_3d":4.8,"gaming_index":24,"vram_gb":6, "tier":"Media",      "gen":"Turing",       "pcie":"3.0","launched":2019,"ram_recommended":"DDR4"},
        "gtx 1660 ti":       {"score_3d":5.0,"gaming_index":26,"vram_gb":6, "tier":"Media",      "gen":"Turing",       "pcie":"3.0","launched":2019,"ram_recommended":"DDR4"},

        # ── NVIDIA RTX 2000 (Turing) ─────────────────────────────────────────
        "rtx 2060":          {"score_3d":5.8,"gaming_index":31,"vram_gb":8, "tier":"Media",      "gen":"Turing",       "pcie":"3.0","launched":2019,"ram_recommended":"DDR4"},
        "rtx 2060 super":    {"score_3d":6.2,"gaming_index":35,"vram_gb":8, "tier":"Media",      "gen":"Turing",       "pcie":"3.0","launched":2019,"ram_recommended":"DDR4"},
        "rtx 2070":          {"score_3d":6.5,"gaming_index":37,"vram_gb":8, "tier":"Media-Alta", "gen":"Turing",       "pcie":"3.0","launched":2018,"ram_recommended":"DDR4"},
        "rtx 2070 super":    {"score_3d":7.0,"gaming_index":42,"vram_gb":8, "tier":"Media-Alta", "gen":"Turing",       "pcie":"3.0","launched":2019,"ram_recommended":"DDR4"},
        "rtx 2080":          {"score_3d":7.4,"gaming_index":46,"vram_gb":8, "tier":"Media-Alta", "gen":"Turing",       "pcie":"3.0","launched":2018,"ram_recommended":"DDR4"},
        "rtx 2080 super":    {"score_3d":7.6,"gaming_index":48,"vram_gb":8, "tier":"Media-Alta", "gen":"Turing",       "pcie":"3.0","launched":2019,"ram_recommended":"DDR4"},
        "rtx 2080 ti":       {"score_3d":8.0,"gaming_index":54,"vram_gb":11,"tier":"Alta",       "gen":"Turing",       "pcie":"3.0","launched":2018,"ram_recommended":"DDR4"},

        # ── NVIDIA RTX 3000 (Ampere) ─────────────────────────────────────────
        "rtx 3050":          {"score_3d":5.5,"gaming_index":30,"vram_gb":8, "tier":"Media",      "gen":"Ampere",       "pcie":"4.0","launched":2022,"ram_recommended":"DDR4"},
        "rtx 3060":          {"score_3d":6.8,"gaming_index":42,"vram_gb":12,"tier":"Media-Alta", "gen":"Ampere",       "pcie":"4.0","launched":2021,"ram_recommended":"DDR4"},
        "rtx 3060 ti":       {"score_3d":7.6,"gaming_index":51,"vram_gb":8, "tier":"Alta",       "gen":"Ampere",       "pcie":"4.0","launched":2020,"ram_recommended":"DDR4"},
        "rtx 3070":          {"score_3d":8.2,"gaming_index":59,"vram_gb":8, "tier":"Alta",       "gen":"Ampere",       "pcie":"4.0","launched":2020,"ram_recommended":"DDR4"},
        "rtx 3070 ti":       {"score_3d":8.4,"gaming_index":62,"vram_gb":8, "tier":"Alta",       "gen":"Ampere",       "pcie":"4.0","launched":2021,"ram_recommended":"DDR4"},
        "rtx 3080 10gb":     {"score_3d":8.9,"gaming_index":71,"vram_gb":10,"tier":"Entusiasta", "gen":"Ampere",       "pcie":"4.0","launched":2020,"ram_recommended":"DDR4"},
        "rtx 3080 12gb":     {"score_3d":9.0,"gaming_index":73,"vram_gb":12,"tier":"Entusiasta", "gen":"Ampere",       "pcie":"4.0","launched":2021,"ram_recommended":"DDR4"},
        "rtx 3080 ti":       {"score_3d":9.2,"gaming_index":76,"vram_gb":12,"tier":"Entusiasta", "gen":"Ampere",       "pcie":"4.0","launched":2021,"ram_recommended":"DDR4"},
        "rtx 3090":          {"score_3d":9.3,"gaming_index":78,"vram_gb":24,"tier":"Entusiasta", "gen":"Ampere",       "pcie":"4.0","launched":2020,"ram_recommended":"DDR4"},
        "rtx 3090 ti":       {"score_3d":9.4,"gaming_index":80,"vram_gb":24,"tier":"Entusiasta", "gen":"Ampere",       "pcie":"4.0","launched":2022,"ram_recommended":"DDR4"},

        # ── NVIDIA RTX 4000 (Ada Lovelace) ───────────────────────────────────
        "rtx 4060":          {"score_3d":7.2,"gaming_index":47,"vram_gb":8, "tier":"Media-Alta", "gen":"Ada Lovelace", "pcie":"4.0","launched":2023,"ram_recommended":"DDR4"},
        "rtx 4060 ti 8gb":   {"score_3d":7.8,"gaming_index":55,"vram_gb":8, "tier":"Alta",       "gen":"Ada Lovelace", "pcie":"4.0","launched":2023,"ram_recommended":"DDR4"},
        "rtx 4060 ti 16gb":  {"score_3d":7.9,"gaming_index":56,"vram_gb":16,"tier":"Alta",       "gen":"Ada Lovelace", "pcie":"4.0","launched":2023,"ram_recommended":"DDR4"},
        "rtx 4070":          {"score_3d":8.6,"gaming_index":67,"vram_gb":12,"tier":"Alta",       "gen":"Ada Lovelace", "pcie":"4.0","launched":2023,"ram_recommended":"DDR4"},
        "rtx 4070 super":    {"score_3d":8.9,"gaming_index":73,"vram_gb":12,"tier":"Entusiasta", "gen":"Ada Lovelace", "pcie":"4.0","launched":2024,"ram_recommended":"DDR4"},
        "rtx 4070 ti":       {"score_3d":9.0,"gaming_index":76,"vram_gb":12,"tier":"Entusiasta", "gen":"Ada Lovelace", "pcie":"4.0","launched":2023,"ram_recommended":"DDR4"},
        "rtx 4070 ti super": {"score_3d":9.2,"gaming_index":80,"vram_gb":16,"tier":"Entusiasta", "gen":"Ada Lovelace", "pcie":"4.0","launched":2024,"ram_recommended":"DDR5"},
        "rtx 4080":          {"score_3d":9.4,"gaming_index":85,"vram_gb":16,"tier":"Entusiasta", "gen":"Ada Lovelace", "pcie":"4.0","launched":2022,"ram_recommended":"DDR5"},
        "rtx 4080 super":    {"score_3d":9.5,"gaming_index":87,"vram_gb":16,"tier":"Entusiasta", "gen":"Ada Lovelace", "pcie":"4.0","launched":2024,"ram_recommended":"DDR5"},
        "rtx 4090":          {"score_3d":9.7,"gaming_index":93,"vram_gb":24,"tier":"Entusiasta", "gen":"Ada Lovelace", "pcie":"4.0","launched":2022,"ram_recommended":"DDR5"},

        # ── NVIDIA RTX 5000 (Blackwell) [2025] ───────────────────────────────
        "rtx 5060":          {"score_3d":7.8,"gaming_index":55,"vram_gb":8, "tier":"Alta",       "gen":"Blackwell",    "pcie":"5.0","launched":2025,"ram_recommended":"DDR5"},
        "rtx 5060 ti 8gb":   {"score_3d":8.4,"gaming_index":63,"vram_gb":8, "tier":"Alta",       "gen":"Blackwell",    "pcie":"5.0","launched":2025,"ram_recommended":"DDR5"},
        "rtx 5060 ti 16gb":  {"score_3d":8.5,"gaming_index":65,"vram_gb":16,"tier":"Alta",       "gen":"Blackwell",    "pcie":"5.0","launched":2025,"ram_recommended":"DDR5"},
        "rtx 5070":          {"score_3d":9.1,"gaming_index":77,"vram_gb":12,"tier":"Entusiasta", "gen":"Blackwell",    "pcie":"5.0","launched":2025,"ram_recommended":"DDR5"},
        "rtx 5070 ti":       {"score_3d":9.4,"gaming_index":84,"vram_gb":16,"tier":"Entusiasta", "gen":"Blackwell",    "pcie":"5.0","launched":2025,"ram_recommended":"DDR5"},
        "rtx 5080":          {"score_3d":9.6,"gaming_index":90,"vram_gb":16,"tier":"Entusiasta", "gen":"Blackwell",    "pcie":"5.0","launched":2025,"ram_recommended":"DDR5"},
        "rtx 5090":          {"score_3d":9.9,"gaming_index":100,"vram_gb":32,"tier":"Entusiasta","gen":"Blackwell",    "pcie":"5.0","launched":2025,"ram_recommended":"DDR5"},

        # ── AMD RX 5000 (RDNA 1) ─────────────────────────────────────────────
        "rx 5600 xt":        {"score_3d":5.4,"gaming_index":29,"vram_gb":6, "tier":"Media",      "gen":"RDNA 1",       "pcie":"4.0","launched":2020,"ram_recommended":"DDR4"},
        "rx 5700":           {"score_3d":6.0,"gaming_index":34,"vram_gb":8, "tier":"Media",      "gen":"RDNA 1",       "pcie":"4.0","launched":2019,"ram_recommended":"DDR4"},
        "rx 5700 xt":        {"score_3d":6.5,"gaming_index":38,"vram_gb":8, "tier":"Media-Alta", "gen":"RDNA 1",       "pcie":"4.0","launched":2019,"ram_recommended":"DDR4"},

        # ── AMD RX 6000 (RDNA 2) ─────────────────────────────────────────────
        "rx 6500 xt":        {"score_3d":3.8,"gaming_index":18,"vram_gb":4, "tier":"Entrada",    "gen":"RDNA 2",       "pcie":"4.0","launched":2022,"ram_recommended":"DDR4"},
        "rx 6600":           {"score_3d":6.4,"gaming_index":39,"vram_gb":8, "tier":"Media",      "gen":"RDNA 2",       "pcie":"4.0","launched":2021,"ram_recommended":"DDR4"},
        "rx 6600 xt":        {"score_3d":6.8,"gaming_index":43,"vram_gb":8, "tier":"Media-Alta", "gen":"RDNA 2",       "pcie":"4.0","launched":2021,"ram_recommended":"DDR4"},
        "rx 6650 xt":        {"score_3d":7.0,"gaming_index":45,"vram_gb":8, "tier":"Media-Alta", "gen":"RDNA 2",       "pcie":"4.0","launched":2022,"ram_recommended":"DDR4"},
        "rx 6700":           {"score_3d":7.4,"gaming_index":49,"vram_gb":10,"tier":"Media-Alta", "gen":"RDNA 2",       "pcie":"4.0","launched":2022,"ram_recommended":"DDR4"},
        "rx 6700 xt":        {"score_3d":7.8,"gaming_index":54,"vram_gb":12,"tier":"Alta",       "gen":"RDNA 2",       "pcie":"4.0","launched":2021,"ram_recommended":"DDR4"},
        "rx 6750 xt":        {"score_3d":8.0,"gaming_index":56,"vram_gb":12,"tier":"Alta",       "gen":"RDNA 2",       "pcie":"4.0","launched":2022,"ram_recommended":"DDR4"},
        "rx 6800":           {"score_3d":8.5,"gaming_index":64,"vram_gb":16,"tier":"Alta",       "gen":"RDNA 2",       "pcie":"4.0","launched":2020,"ram_recommended":"DDR4"},
        "rx 6800 xt":        {"score_3d":8.8,"gaming_index":69,"vram_gb":16,"tier":"Entusiasta", "gen":"RDNA 2",       "pcie":"4.0","launched":2020,"ram_recommended":"DDR4"},
        "rx 6900 xt":        {"score_3d":9.0,"gaming_index":73,"vram_gb":16,"tier":"Entusiasta", "gen":"RDNA 2",       "pcie":"4.0","launched":2020,"ram_recommended":"DDR4"},
        "rx 6950 xt":        {"score_3d":9.1,"gaming_index":75,"vram_gb":16,"tier":"Entusiasta", "gen":"RDNA 2",       "pcie":"4.0","launched":2022,"ram_recommended":"DDR4"},

        # ── AMD RX 7000 (RDNA 3) ─────────────────────────────────────────────
        "rx 7600":           {"score_3d":6.8,"gaming_index":43,"vram_gb":8, "tier":"Media-Alta", "gen":"RDNA 3",       "pcie":"4.0","launched":2023,"ram_recommended":"DDR4"},
        "rx 7600 xt":        {"score_3d":7.2,"gaming_index":47,"vram_gb":16,"tier":"Media-Alta", "gen":"RDNA 3",       "pcie":"4.0","launched":2024,"ram_recommended":"DDR4"},
        "rx 7700 xt":        {"score_3d":7.7,"gaming_index":53,"vram_gb":12,"tier":"Alta",       "gen":"RDNA 3",       "pcie":"4.0","launched":2023,"ram_recommended":"DDR4"},
        "rx 7800 xt":        {"score_3d":8.4,"gaming_index":63,"vram_gb":16,"tier":"Alta",       "gen":"RDNA 3",       "pcie":"4.0","launched":2023,"ram_recommended":"DDR4"},
        "rx 7900 gre":       {"score_3d":8.8,"gaming_index":69,"vram_gb":16,"tier":"Entusiasta", "gen":"RDNA 3",       "pcie":"4.0","launched":2023,"ram_recommended":"DDR4"},
        "rx 7900 xt":        {"score_3d":9.1,"gaming_index":75,"vram_gb":20,"tier":"Entusiasta", "gen":"RDNA 3",       "pcie":"4.0","launched":2022,"ram_recommended":"DDR5"},
        "rx 7900 xtx":       {"score_3d":9.3,"gaming_index":80,"vram_gb":24,"tier":"Entusiasta", "gen":"RDNA 3",       "pcie":"4.0","launched":2022,"ram_recommended":"DDR5"},

        # ── AMD RX 9000 (RDNA 4) [2025] ──────────────────────────────────────
        "rx 9060 xt":        {"score_3d":8.0,"gaming_index":59,"vram_gb":16,"tier":"Alta",       "gen":"RDNA 4",       "pcie":"5.0","launched":2025,"ram_recommended":"DDR5"},
        "rx 9070":           {"score_3d":8.8,"gaming_index":70,"vram_gb":16,"tier":"Entusiasta", "gen":"RDNA 4",       "pcie":"5.0","launched":2025,"ram_recommended":"DDR5"},
        "rx 9070 xt":        {"score_3d":9.1,"gaming_index":76,"vram_gb":16,"tier":"Entusiasta", "gen":"RDNA 4",       "pcie":"5.0","launched":2025,"ram_recommended":"DDR5"},
        "rx 9080":           {"score_3d":9.5,"gaming_index":86,"vram_gb":32,"tier":"Entusiasta", "gen":"RDNA 4",       "pcie":"5.0","launched":2025,"ram_recommended":"DDR5"},
    }

    RAM_TYPES = {
        "DDR3":    {"max_speed_mhz":2133, "typical_bw_mbs":17000, "score_max":5.5, "note":"Plataformas pre-2015"},
        "DDR4":    {"max_speed_mhz":4800, "typical_bw_mbs":38400, "score_max":8.5, "note":"Estándar 2016-2023"},
        "DDR5":    {"max_speed_mhz":8000, "typical_bw_mbs":76800, "score_max":9.9, "note":"Estándar 2022+"},
        "LPDDR5":  {"max_speed_mhz":6400, "typical_bw_mbs":51200, "score_max":9.0, "note":"Laptops"},
        "LPDDR5X": {"max_speed_mhz":8533, "typical_bw_mbs":68000, "score_max":9.5, "note":"Laptops premium"},
    }

    POPULAR_CONFIGS = [
        {"name": "i3-10100F + GTX 1650",          "score": 4.8},
        {"name": "Ryzen 5 3600 + RTX 2060",       "score": 6.2},
        {"name": "Ryzen 5 5600 + RTX 3060",       "score": 7.4},
        {"name": "i5-12400F + RTX 3060 Ti",       "score": 7.9},
        {"name": "Ryzen 7 5700X3D + RTX 3080",    "score": 8.5},
        {"name": "i5-13600K + RTX 4070",          "score": 8.8},
        {"name": "Ryzen 7 7800X3D + RTX 4080",    "score": 9.2},
        {"name": "Ryzen 9 9950X + RTX 5090",      "score": 9.9},
    ]

    def get_cpu_list(self) -> list[str]:
        return sorted([k.title() for k in self.CPUS.keys()])

    def get_gpu_list(self) -> list[str]:
        return sorted([k.title() for k in self.GPUS.keys()])

    def find_cpu(self, name: str) -> dict | None:
        if not name:
            return None
        name_l = name.lower().strip()
        if name_l in self.CPUS:
            return {**self.CPUS[name_l], "_key": name_l}
        best, best_len = None, 0
        for key, val in self.CPUS.items():
            if key in name_l or name_l in key:
                if len(key) > best_len:
                    best, best_len = {**val, "_key": key}, len(key)
        return best

    def find_gpu(self, name: str) -> dict | None:
        if not name:
            return None
        name_l = name.lower().strip()
        if name_l in self.GPUS:
            return {**self.GPUS[name_l], "_key": name_l}
        best, best_len = None, 0
        for key, val in self.GPUS.items():
            if key in name_l or name_l in key:
                if len(key) > best_len:
                    best, best_len = {**val, "_key": key}, len(key)
        return best

    def get_comparison_configs(self, analysis: dict) -> list[dict]:
        user_score = analysis["overall_score"]
        configs = [dict(c) for c in self.POPULAR_CONFIGS]
        configs.append({"name": "⭐ Tu PC", "score": round(user_score, 2), "is_user": True})
        configs.sort(key=lambda c: c["score"])
        return configs

    def get_socket_info(self, socket: str) -> str:
        info = {
            "AM4":     "AMD AM4 — Ryzen 1000 a 5000. Solo DDR4.",
            "AM5":     "AMD AM5 — Ryzen 7000 y 9000. Solo DDR5. Plataforma activa.",
            "LGA1200": "Intel LGA1200 — 10ª y 11ª gen. Solo DDR4.",
            "LGA1700": "Intel LGA1700 — 12ª, 13ª y 14ª gen. DDR4 o DDR5.",
            "LGA1851": "Intel LGA1851 — Core Ultra (Arrow Lake). Solo DDR5.",
        }
        return info.get(socket, socket)
