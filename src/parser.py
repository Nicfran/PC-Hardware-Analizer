"""
parser.py — Extrae métricas del XML de WinSAT formal.
Soporta UTF-16 (BOM) y UTF-8. Maneja campos opcionales con gracia.
"""
import xml.etree.ElementTree as ET
import re


def _safe_float(el, xpath, default=0.0):
    node = el.find(xpath)
    if node is None or node.text is None:
        return default
    try:
        return float(node.text.strip())
    except ValueError:
        return default


def _safe_text(el, xpath, default=""):
    node = el.find(xpath)
    if node is None:
        return default
    return (node.text or "").strip()


def parse_winsat_xml(content: bytes) -> dict:
    """
    Parsea el XML de WinSAT y devuelve un dict con todas las métricas.
    content: bytes del archivo XML (UTF-16 con BOM o UTF-8).
    """
    # Decodificar — WinSAT usa UTF-16 con BOM
    try:
        text = content.decode("utf-16")
    except (UnicodeDecodeError, Exception):
        try:
            text = content.decode("utf-8")
        except Exception:
            text = content.decode("latin-1")

    # Limpiar BOM residual
    text = text.lstrip("\ufeff")

    root = ET.fromstring(text)

    # ── WinSPR scores ────────────────────────────────────────────────────────
    spr = root.find("WinSPR")
    scores_spr = {}
    if spr is not None:
        for child in spr:
            try:
                if child.text:
                    scores_spr[child.tag] = float(child.text.strip())
            except (TypeError, ValueError):
                pass

    # ── CPU Metrics ──────────────────────────────────────────────────────────
    cpu_m = root.find(".//CPUMetrics")
    cpu_compression    = _safe_float(cpu_m, "CompressionMetric")   if cpu_m is not None else 0
    cpu_encryption     = _safe_float(cpu_m, "EncryptionMetric")    if cpu_m is not None else 0
    cpu_compression2   = _safe_float(cpu_m, "CPUCompression2Metric") if cpu_m is not None else 0
    cpu_encryption2    = _safe_float(cpu_m, "Encryption2Metric")   if cpu_m is not None else 0

    # ── Memory Metrics ───────────────────────────────────────────────────────
    mem_m = root.find(".//MemoryMetrics")
    mem_bandwidth = _safe_float(mem_m, "Bandwidth") if mem_m is not None else 0

    # ── Graphics Metrics ─────────────────────────────────────────────────────
    gfx_m = root.find(".//GraphicsMetrics")
    dwm_fps       = _safe_float(gfx_m, "DWMFps")            if gfx_m is not None else 0
    video_mem_bw  = _safe_float(gfx_m, "VideoMemBandwidth") if gfx_m is not None else 0

    # ── Disk Metrics ─────────────────────────────────────────────────────────
    disk_metrics = root.findall(".//DiskMetrics")
    disk_seq_read  = 0.0
    disk_rand_read = 0.0
    for dm in disk_metrics:
        for thr in dm.findall("AvgThroughput"):
            kind = thr.get("kind", "")
            val  = float(thr.text.strip()) if thr.text else 0.0
            score = float(thr.get("score", 0))
            if "Sequential Read" in kind:
                disk_seq_read  = max(disk_seq_read, val)
            elif "Random Read" in kind:
                disk_rand_read = max(disk_rand_read, val)

    # ── Disk drives individuales ─────────────────────────────────────────────
    disk_drives = []
    for da in root.findall(".//DiskAssessment"):
        per_disk = da.find("PerDiskData")
        if per_disk is None:
            continue
        disk_id = _safe_text(per_disk, "Disk")
        zones   = per_disk.findall("Zone")
        for zone in zones:
            mode  = zone.find("ModeFlags")
            thr_el = zone.find("Throughput")
            if thr_el is None:
                continue
            try:
                thr = float(thr_el.text.strip())
            except (TypeError, ValueError):
                continue
            mode_name = mode.get("friendlyName", "") if mode is not None else ""
            disk_drives.append({
                "disk": disk_id,
                "mode": mode_name,
                "throughput_mbs": thr,
            })

    # Clasificar discos: >=100 MB/s rand → SSD, <10 → HDD
    drives_summary = {}
    for d in disk_drives:
        key = d["disk"]
        if key not in drives_summary:
            drives_summary[key] = {"seq": 0, "rand": 0}
        if "Secuencial" in d["mode"] or "Sequential" in d["mode"]:
            drives_summary[key]["seq"] = max(drives_summary[key]["seq"], d["throughput_mbs"])
        elif "Aleatoria" in d["mode"] or "Random" in d["mode"]:
            drives_summary[key]["rand"] = max(drives_summary[key]["rand"], d["throughput_mbs"])

    drives_classified = {}
    for drive, vals in drives_summary.items():
        rand = vals["rand"]
        seq  = vals["seq"]
        if rand >= 300:
            kind = "NVMe SSD"
        elif rand >= 50:
            kind = "SATA SSD"
        elif rand > 0:
            kind = "HDD"
        else:
            kind = "Desconocido"
        drives_classified[drive] = {"seq": seq, "rand": rand, "type": kind}

    # ── System Config ────────────────────────────────────────────────────────
    sys_cfg = root.find("SystemConfig")

    # OS
    os_el   = sys_cfg.find("OSVersion") if sys_cfg is not None else None
    os_name = _safe_text(os_el, "OSName") if os_el is not None else "Windows"
    if not os_name:
        os_name = _safe_text(os_el, "ProductName") if os_el is not None else "Windows"

    # Motherboard
    mb_el  = sys_cfg.find(".//MotherBoard") if sys_cfg is not None else None
    mb_mfr = _safe_text(mb_el, "Manufacturer") if mb_el is not None else ""
    mb_prd = _safe_text(mb_el, "Product")       if mb_el is not None else ""
    motherboard = f"{mb_mfr} {mb_prd}".strip()

    # BIOS
    bios_el  = sys_cfg.find(".//BIOS") if sys_cfg is not None else None
    bios_ver = _safe_text(bios_el, "Version")     if bios_el is not None else ""
    bios_date= _safe_text(bios_el, "ReleaseDate") if bios_el is not None else ""

    # CPU info from processor element
    proc_el = sys_cfg.find(".//Processor/Instance") if sys_cfg is not None else None
    cpu_name_xml = ""
    cpu_cores    = 0
    cpu_threads  = 0
    cpu_freq_mhz = 0
    if proc_el is not None:
        cpu_name_xml = _safe_text(proc_el, "Name")
        try: cpu_cores   = int(_safe_text(proc_el, "NumberOfCores", "0"))
        except: pass
        try: cpu_threads = int(_safe_text(proc_el, "NumberOfLogicalProcessors", "0"))
        except: pass
        try: cpu_freq_mhz= int(_safe_text(proc_el, "MaxClockSpeed", "0"))
        except: pass

    # GPU info
    gpu_els = sys_cfg.findall(".//VideoAdapter") if sys_cfg is not None else []
    gpu_entries = []
    for g in gpu_els:
        gname  = _safe_text(g, "Name")
        vram_b = 0
        try: vram_b = int(_safe_text(g, "AdapterRAM", "0"))
        except: pass
        if gname:
            gpu_entries.append({"name": gname, "vram_mb": vram_b // (1024*1024)})

    # RAM
    ram_els = sys_cfg.findall(".//Memory") if sys_cfg is not None else []
    total_ram_mb = 0
    ram_speed    = 0
    ram_type_str = "DDR4"
    for r in ram_els:
        try: total_ram_mb += int(_safe_text(r, "Capacity", "0")) // (1024*1024)
        except: pass
        try:
            spd = int(_safe_text(r, "Speed", "0"))
            if spd > ram_speed: ram_speed = spd
        except: pass
        mt = _safe_text(r, "MemoryType")
        if mt == "26":   ram_type_str = "DDR4"
        elif mt == "34": ram_type_str = "DDR5"
        elif mt == "24": ram_type_str = "DDR3"

    # Inferir RAM DDR desde bandwidth si no viene en XML
    if mem_bandwidth > 50000:
        ram_type_str = "DDR5"
    elif mem_bandwidth > 20000:
        ram_type_str = "DDR4"

    return {
        # WinSPR scores
        "spr": scores_spr,
        "system_score":   scores_spr.get("SystemScore",     0),
        "cpu_score":      scores_spr.get("CpuScore",        0),
        "cpu_sub_score":  scores_spr.get("CPUSubAggScore",  0),
        "mem_score":      scores_spr.get("MemoryScore",     0),
        "gpu_score":      scores_spr.get("GraphicsScore",   0),
        "gaming_score":   scores_spr.get("GamingScore",     0),
        "disk_score":     scores_spr.get("DiskScore",       0),

        # CPU raw metrics
        "cpu_compression":  cpu_compression,
        "cpu_encryption":   cpu_encryption,
        "cpu_compression2": cpu_compression2,
        "cpu_encryption2":  cpu_encryption2,

        # Memory
        "mem_bandwidth_mbs": mem_bandwidth,
        "ram_type": ram_type_str,
        "total_ram_mb": total_ram_mb,
        "ram_speed_mhz": ram_speed,

        # GPU
        "dwm_fps": dwm_fps,
        "video_mem_bandwidth_mbs": video_mem_bw,
        "gpu_entries": gpu_entries,

        # Disk
        "disk_seq_read_mbs":  disk_seq_read,
        "disk_rand_read_mbs": disk_rand_read,
        "drives": drives_classified,

        # System info
        "os_name":     os_name,
        "motherboard": motherboard,
        "bios_version": bios_ver,
        "bios_date":    bios_date,
        "cpu_name_xml": cpu_name_xml,
        "cpu_cores":    cpu_cores,
        "cpu_threads":  cpu_threads,
        "cpu_freq_mhz": cpu_freq_mhz,
    }
