import re
import pandas as pd


# ===== CLEANING FUNCTION =====

def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = text.replace("+", " plus ")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ===== CPU SCORE =====

CPU_MODEL_SCORES = {
    # ===== Intel Core Ultra Series 2 / 2025-2026 mobile =====
    "Intel Core Ultra 9 290HX Plus": 100,
    "Intel Core Ultra 7 270HX Plus": 96,
    "Intel Core Ultra 9 285HX": 100,
    "Intel Core Ultra 9 275HX": 98,
    "Intel Core Ultra 9 285H": 97,
    "Intel Core Ultra 9 288V": 86,

    "Intel Core Ultra 7 265HX": 95,
    "Intel Core Ultra 7 255HX": 93,
    "Intel Core Ultra 7 265H": 92,
    "Intel Core Ultra 7 255H": 90,
    "Intel Core Ultra 7 268V": 82,
    "Intel Core Ultra 7 258V": 80,
    "Intel Core Ultra 7 256V": 78,
    "Intel Core Ultra 7 255U": 76,

    "Intel Core Ultra 5 245HX": 88,
    "Intel Core Ultra 5 235HX": 86,
    "Intel Core Ultra 5 245H": 84,
    "Intel Core Ultra 5 235H": 82,
    "Intel Core Ultra 5 225H": 78,
    "Intel Core Ultra 5 238V": 74,
    "Intel Core Ultra 5 228V": 72,
    "Intel Core Ultra 5 226V": 70,
    "Intel Core Ultra 5 225U": 68,

    # ===== Intel Core Ultra Series 1 / Meteor Lake =====
    "Intel Core Ultra 9 185H": 96,
    "Intel Core Ultra 7 165H": 90,
    "Intel Core Ultra 7 155H": 88,
    "Intel Core Ultra 7 155U": 76,
    "Intel Core Ultra 5 135H": 78,
    "Intel Core Ultra 5 125H": 76,
    "Intel Core Ultra 5 135U": 68,
    "Intel Core Ultra 5 125U": 66,

    # ===== Intel Core i9 laptop =====
    "Intel Core i9-14900HX": 100,
    "Intel Core i9-13980HX": 99,
    "Intel Core i9-13950HX": 98,
    "Intel Core i9-13900HX": 98,
    "Intel Core i9-13900H": 96,
    "Intel Core i9-12950HX": 97,
    "Intel Core i9-12900HX": 96,
    "Intel Core i9-12900H": 94,
    "Intel Core i9-11980HK": 84,
    "Intel Core i9-11950H": 82,
    "Intel Core i9-10980HK": 78,
    "Intel Core i9-9980HK": 72,
    "Intel Core i9-8950HK": 68,

    # ===== Intel Core i7 laptop =====
    "Intel Core i7-14700HX": 97,
    "Intel Core i7-14650HX": 94,
    "Intel Core i7-13850HX": 96,
    "Intel Core i7-13700HX": 96,
    "Intel Core i7-13700H": 94,
    "Intel Core i7-13650HX": 91,
    "Intel Core i7-13620H": 88,
    "Intel Core i7-1355U": 76,
    "Intel Core i7-1335U": 74,
    "Intel Core i7-12850HX": 93,
    "Intel Core i7-12800HX": 92,
    "Intel Core i7-12800H": 91,
    "Intel Core i7-12700H": 90,
    "Intel Core i7-12650H": 86,
    "Intel Core i7-1260P": 76,
    "Intel Core i7-1255U": 72,
    "Intel Core i7-1250U": 70,
    "Intel Core i7-11850H": 80,
    "Intel Core i7-11800H": 78,
    "Intel Core i7-1165G7": 68,
    "Intel Core i7-11370H": 66,
    "Intel Core i7-10870H": 72,
    "Intel Core i7-10750H": 68,
    "Intel Core i7-1065G7": 60,
    "Intel Core i7-10510U": 58,
    "Intel Core i7-9750H": 64,
    "Intel Core i7-8750H": 60,
    "Intel Core i7-8565U": 54,
    "Intel Core i7-8550U": 52,
    "Intel Core i7-7700HQ": 52,
    "Intel Core i7-7500U": 45,
    "Intel Core i7-6500U": 40,
    "Intel Core i7-5500U": 36,
    "Intel Core i7-4700MQ": 42,
    "Intel Core i7-3630QM": 35,
    "Intel Core i7-2670QM": 30,

    # ===== Intel Core i5 laptop =====
    "Intel Core i5-14500HX": 92,
    "Intel Core i5-14450HX": 88,
    "Intel Core i5-13500HX": 90,
    "Intel Core i5-13500H": 88,
    "Intel Core i5-13450HX": 86,
    "Intel Core i5-13420H": 82,
    "Intel Core i5-1340P": 78,
    "Intel Core i5-1335U": 74,
    "Intel Core i5-1334U": 73,
    "Intel Core i5-12450HX": 82,
    "Intel Core i5-12500H": 83,
    "Intel Core i5-12450H": 78,
    "Intel Core i5-1240P": 74,
    "Intel Core i5-1235U": 70,
    "Intel Core i5-1230U": 68,
    "Intel Core i5-11400H": 72,
    "Intel Core i5-11320H": 66,
    "Intel Core i5-11300H": 65,
    "Intel Core i5-1135G7": 64,
    "Intel Core i5-10300H": 62,
    "Intel Core i5-1035G1": 56,
    "Intel Core i5-1035G4": 57,
    "Intel Core i5-10210U": 55,
    "Intel Core i5-9300H": 58,
    "Intel Core i5-8300H": 55,
    "Intel Core i5-8265U": 50,
    "Intel Core i5-8250U": 48,
    "Intel Core i5-7300HQ": 45,
    "Intel Core i5-7200U": 42,
    "Intel Core i5-6200U": 38,
    "Intel Core i5-5200U": 34,
    "Intel Core i5-4210U": 30,
    "Intel Core i5-3320M": 28,
    "Intel Core i5-2520M": 25,

    # ===== Intel Core i3 laptop =====
    "Intel Core i3-1315U": 58,
    "Intel Core i3-1305U": 54,
    "Intel Core i3-1220P": 58,
    "Intel Core i3-1215U": 55,
    "Intel Core i3-1125G4": 52,
    "Intel Core i3-1115G4": 48,
    "Intel Core i3-1005G1": 42,
    "Intel Core i3-10110U": 40,
    "Intel Core i3-8145U": 38,
    "Intel Core i3-8130U": 36,
    "Intel Core i3-7020U": 32,
    "Intel Core i3-6006U": 28,
    "Intel Core i3-5005U": 25,
    "Intel Core i3-4005U": 22,
    "Intel Core i3-3110M": 22,
    "Intel Core i3-2310M": 18,

    # ===== Intel Core 3 / 5 / 7 tanpa huruf i, generasi baru non-Ultra =====
    "Intel Core 7 150U": 72,
    "Intel Core 5 120U": 64,
    "Intel Core 3 100U": 52,

    # ===== Intel N-Series, Pentium, Celeron, Atom, Core M, lawas =====
    "Intel Core i3-N305": 45,
    "Intel Core i3-N300": 42,
    "Intel Processor N200": 40,
    "Intel Processor N100": 35,
    "Intel Processor N95": 32,
    "Intel Pentium Gold 8505": 42,
    "Intel Pentium Gold 7505": 38,
    "Intel Pentium Silver N6005": 32,
    "Intel Pentium Silver N6000": 30,
    "Intel Pentium Silver N5030": 27,
    "Intel Pentium Silver N5000": 25,
    "Intel Pentium N4200": 22,
    "Intel Pentium N3710": 19,
    "Intel Pentium N3700": 18,
    "Intel Celeron N5105": 28,
    "Intel Celeron N5095": 27,
    "Intel Celeron N4500": 25,
    "Intel Celeron N4020": 22,
    "Intel Celeron N4000": 20,
    "Intel Celeron N3350": 16,
    "Intel Celeron 5205U": 24,
    "Intel Celeron 4205U": 22,
    "Intel Celeron 3865U": 18,
    "Intel Celeron 2957U": 15,
    "Intel Atom x5-Z8350": 12,
    "Intel Atom x5-Z8300": 10,
    "Intel Core m3-8100Y": 34,
    "Intel Core m3-7Y30": 28,
    "Intel Core M-5Y10": 20,
    "Intel Core 2 Duo P8600": 10,
    "Intel Core 2 Duo T6600": 8,

    # ===== AMD Ryzen 9000 / Fire Range laptop =====
    "AMD Ryzen 9 9955HX3D": 100,
    "AMD Ryzen 9 9955HX": 99,
    "AMD Ryzen 9 9850HX": 97,

    # ===== AMD Ryzen AI / Ryzen AI Max =====
    "AMD Ryzen AI Max+ 395": 100,
    "AMD Ryzen AI Max 390": 96,
    "AMD Ryzen AI Max 385": 92,

    # Ryzen AI 400 Series
    "AMD Ryzen AI 9 465": 94,
    "AMD Ryzen AI 7 450": 88,
    "AMD Ryzen AI 5 340": 78,
    "AMD Ryzen AI 5 330": 72,

    # Ryzen AI 300 Series
    "AMD Ryzen AI 9 HX 375": 98,
    "AMD Ryzen AI 9 HX 370": 96,
    "AMD Ryzen AI 9 365": 91,
    "AMD Ryzen AI 7 350": 88,

    # ===== AMD Ryzen 9 laptop =====
    "AMD Ryzen 9 8945HS": 97,
    "AMD Ryzen 9 7945HX": 100,
    "AMD Ryzen 9 7940HX": 96,
    "AMD Ryzen 9 7940HS": 95,
    "AMD Ryzen 9 7845HX": 94,
    "AMD Ryzen 9 6900HX": 90,
    "AMD Ryzen 9 6900HS": 88,
    "AMD Ryzen 9 5980HX": 86,
    "AMD Ryzen 9 5900HX": 84,
    "AMD Ryzen 9 5900HS": 82,
    "AMD Ryzen 9 4900HS": 76,
    "AMD Ryzen 9 4900H": 75,

    # ===== AMD Ryzen 7 laptop =====
    "AMD Ryzen 7 8845HS": 91,
    "AMD Ryzen 7 8840HS": 89,
    "AMD Ryzen 7 8840U": 78,
    "AMD Ryzen 7 7840HS": 89,
    "AMD Ryzen 7 7840U": 76,
    "AMD Ryzen 7 7735HS": 84,
    "AMD Ryzen 7 7735U": 72,
    "AMD Ryzen 7 7730U": 70,
    "AMD Ryzen 7 6800H": 82,
    "AMD Ryzen 7 6800HS": 82,
    "AMD Ryzen 7 6800U": 70,
    "AMD Ryzen 7 5825U": 72,
    "AMD Ryzen 7 5800H": 78,
    "AMD Ryzen 7 5800HS": 77,
    "AMD Ryzen 7 5800U": 70,
    "AMD Ryzen 7 5700U": 68,
    "AMD Ryzen 7 4800H": 72,
    "AMD Ryzen 7 4800HS": 72,
    "AMD Ryzen 7 4800U": 65,
    "AMD Ryzen 7 4700U": 62,
    "AMD Ryzen 7 3750H": 50,
    "AMD Ryzen 7 3700U": 48,
    "AMD Ryzen 7 2700U": 40,

    # ===== AMD Ryzen 5 laptop =====
    "AMD Ryzen 5 8645HS": 82,
    "AMD Ryzen 5 8640HS": 80,
    "AMD Ryzen 5 8640U": 70,
    "AMD Ryzen 5 7640HS": 78,
    "AMD Ryzen 5 7640U": 68,
    "AMD Ryzen 5 7535HS": 72,
    "AMD Ryzen 5 7535U": 66,
    "AMD Ryzen 5 7530U": 65,
    "AMD Ryzen 5 7520U": 52,
    "AMD Ryzen 5 6600H": 74,
    "AMD Ryzen 5 6600HS": 74,
    "AMD Ryzen 5 6600U": 64,
    "AMD Ryzen 5 5625U": 66,
    "AMD Ryzen 5 5600H": 72,
    "AMD Ryzen 5 5600HS": 72,
    "AMD Ryzen 5 5600U": 64,
    "AMD Ryzen 5 5500U": 62,
    "AMD Ryzen 5 4600H": 65,
    "AMD Ryzen 5 4600U": 60,
    "AMD Ryzen 5 4500U": 58,
    "AMD Ryzen 5 3550H": 47,
    "AMD Ryzen 5 3500U": 45,
    "AMD Ryzen 5 2500U": 38,

    # ===== AMD Ryzen 3 laptop =====
    "AMD Ryzen 3 8440U": 58,
    "AMD Ryzen 3 7330U": 50,
    "AMD Ryzen 3 7320U": 48,
    "AMD Ryzen 3 5425U": 48,
    "AMD Ryzen 3 5300U": 45,
    "AMD Ryzen 3 4300U": 42,
    "AMD Ryzen 3 3250U": 32,
    "AMD Ryzen 3 3200U": 30,
    "AMD Ryzen 3 2200U": 25,

    # ===== AMD Athlon / A-Series lawas =====
    "AMD Athlon Gold 7220U": 32,
    "AMD Athlon Silver 7120U": 28,
    "AMD Athlon Gold 3150U": 26,
    "AMD Athlon Silver 3050U": 22,
    "AMD Athlon 300U": 24,
    "AMD A12-9720P": 22,
    "AMD A10-9620P": 20,
    "AMD A9-9425": 16,
    "AMD A8-7410": 14,
    "AMD A6-9225": 12,
    "AMD E2-9000": 8,

    # ===== Apple Silicon =====
    "Apple M4 Max": 100,
    "Apple M4 Pro": 98,
    "Apple M4": 96,
    "Apple M3 Max": 98,
    "Apple M3 Pro": 95,
    "Apple M3": 92,
    "Apple M2 Max": 94,
    "Apple M2 Pro": 90,
    "Apple M2": 85,
    "Apple M1 Max": 90,
    "Apple M1 Pro": 86,
    "Apple M1": 75,

    # ===== Qualcomm Snapdragon X =====
    "Qualcomm Snapdragon X Elite X1E-84-100": 84,
    "Qualcomm Snapdragon X Elite X1E-80-100": 82,
    "Qualcomm Snapdragon X Elite X1E-78-100": 80,
    "Qualcomm Snapdragon X Plus X1P-64-100": 72,
    "Qualcomm Snapdragon X Plus X1P-42-100": 68,
}


# ===== GPU SCORE =====
# Batas GPU untuk kategori gaming: 58

GPU_MODEL_SCORES = {
    # ===== NVIDIA RTX 50 Series Laptop GPU =====
    "NVIDIA GeForce RTX 5090 Laptop GPU": 100,
    "NVIDIA GeForce RTX 5080 Laptop GPU": 97,
    "NVIDIA GeForce RTX 5070 Ti Laptop GPU": 94,
    "NVIDIA GeForce RTX 5070 Laptop GPU": 91,
    "NVIDIA GeForce RTX 5060 Laptop GPU": 88,
    "NVIDIA GeForce RTX 5050 Laptop GPU": 82,

    # ===== NVIDIA RTX 40 Series Laptop GPU =====
    "NVIDIA GeForce RTX 4090 Laptop GPU": 100,
    "NVIDIA GeForce RTX 4080 Laptop GPU": 95,
    "NVIDIA GeForce RTX 4070 Laptop GPU": 90,
    "NVIDIA GeForce RTX 4060 Laptop GPU": 85,
    "NVIDIA GeForce RTX 4050 Laptop GPU": 78,

    # ===== NVIDIA RTX 30 Series Laptop GPU =====
    "NVIDIA GeForce RTX 3080 Ti Laptop GPU": 92,
    "NVIDIA GeForce RTX 3080 Laptop GPU": 88,
    "NVIDIA GeForce RTX 3070 Ti Laptop GPU": 86,
    "NVIDIA GeForce RTX 3070 Laptop GPU": 84,
    "NVIDIA GeForce RTX 3060 Laptop GPU": 78,
    "NVIDIA GeForce RTX 3050 Ti Laptop GPU": 73,
    "NVIDIA GeForce RTX 3050 Laptop GPU": 70,
    "NVIDIA GeForce RTX 2050 Laptop GPU": 60,

    # ===== NVIDIA RTX 20 Series =====
    "NVIDIA GeForce RTX 2080 Super Max-Q": 78,
    "NVIDIA GeForce RTX 2080 Laptop GPU": 76,
    "NVIDIA GeForce RTX 2070 Super Max-Q": 72,
    "NVIDIA GeForce RTX 2070 Laptop GPU": 70,
    "NVIDIA GeForce RTX 2060 Laptop GPU": 65,

    # ===== NVIDIA GTX 16 / 10 Series laptop + Max-Q =====
    "NVIDIA GeForce GTX 1080 Laptop GPU": 68,
    "NVIDIA GeForce GTX 1080 Max-Q": 65,
    "NVIDIA GeForce GTX 1070 Laptop GPU": 62,
    "NVIDIA GeForce GTX 1070 Max-Q": 59,
    "NVIDIA GeForce GTX 1660 Ti Laptop GPU": 67,
    "NVIDIA GeForce GTX 1660 Ti Max-Q": 64,
    "NVIDIA GeForce GTX 1660 Laptop GPU": 65,
    "NVIDIA GeForce GTX 1650 Ti Laptop GPU": 60,
    "NVIDIA GeForce GTX 1650 Ti Max-Q": 57,
    "NVIDIA GeForce GTX 1650 Laptop GPU": 58,
    "NVIDIA GeForce GTX 1650 Max-Q": 55,
    "NVIDIA GeForce GTX 1060 Laptop GPU": 55,
    "NVIDIA GeForce GTX 1060 Max-Q": 52,
    "NVIDIA GeForce GTX 1050 Ti Laptop GPU": 48,
    "NVIDIA GeForce GTX 1050 Laptop GPU": 45,

    # ===== NVIDIA lawas =====
    "NVIDIA GeForce GTX 965M": 40,
    "NVIDIA GeForce GTX 960M": 38,
    "NVIDIA GeForce GTX 950M": 35,
    "NVIDIA GeForce GTX 880M": 36,
    "NVIDIA GeForce GTX 870M": 35,
    "NVIDIA GeForce GTX 860M": 34,
    "NVIDIA GeForce GTX 850M": 32,
    "NVIDIA GeForce GT 740M": 24,
    "NVIDIA GeForce GT 720M": 20,

    # ===== NVIDIA MX / entry dedicated laptop =====
    "NVIDIA GeForce MX570": 48,
    "NVIDIA GeForce MX550": 46,
    "NVIDIA GeForce MX450": 44,
    "NVIDIA GeForce MX350": 40,
    "NVIDIA GeForce MX330": 38,
    "NVIDIA GeForce MX250": 36,
    "NVIDIA GeForce MX230": 34,
    "NVIDIA GeForce MX150": 34,
    "NVIDIA GeForce 940MX": 30,
    "NVIDIA GeForce 930MX": 28,
    "NVIDIA GeForce 920MX": 24,

    # ===== Intel Arc / Intel Integrated =====
    "Intel Arc Graphics 140T": 57,
    "Intel Arc Graphics 130T": 54,
    "Intel Arc Graphics 140V": 56,
    "Intel Arc Graphics 130V": 53,
    "Intel Arc A770M": 76,
    "Intel Arc A730M": 72,
    "Intel Arc A550M": 65,
    "Intel Arc A370M": 60,
    "Intel Arc A350M": 56,
    "Intel Iris Xe Graphics": 42,
    "Intel Iris Plus Graphics": 34,
    "Intel UHD Graphics Xe 750": 32,
    "Intel UHD Graphics 770": 30,
    "Intel UHD Graphics 730": 28,
    "Intel UHD Graphics 620": 25,
    "Intel UHD Graphics 605": 20,
    "Intel HD Graphics 620": 18,
    "Intel HD Graphics 520": 16,
    "Intel HD Graphics 4000": 10,

    # ===== AMD Radeon Integrated =====
    "AMD Radeon 890M": 57,
    "AMD Radeon 880M": 54,
    "AMD Radeon 780M": 50,
    "AMD Radeon 760M": 46,
    "AMD Radeon 740M": 42,
    "AMD Radeon 680M": 46,
    "AMD Radeon 660M": 40,
    "AMD Radeon 610M": 25,
    "AMD Radeon Vega 10": 35,
    "AMD Radeon Vega 8": 34,
    "AMD Radeon Vega 7": 31,
    "AMD Radeon Vega 6": 28,
    "AMD Radeon Vega 3": 20,
    "AMD Radeon Graphics": 30,

    # ===== AMD Dedicated Mobile GPU =====
    "AMD Radeon RX 7900M": 94,
    "AMD Radeon RX 7800M": 88,
    "AMD Radeon RX 7700S": 82,
    "AMD Radeon RX 7600M XT": 80,
    "AMD Radeon RX 7600M": 78,
    "AMD Radeon RX 6850M XT": 84,
    "AMD Radeon RX 6800M": 82,
    "AMD Radeon RX 6700M": 76,
    "AMD Radeon RX 6650M": 72,
    "AMD Radeon RX 6600M": 68,
    "AMD Radeon RX 6500M": 58,
    "AMD Radeon RX 5700M": 62,
    "AMD Radeon RX 5600M": 58,
    "AMD Radeon RX 5500M": 52,
    "AMD Radeon RX 5300M": 45,
    "AMD Radeon RX 560X": 38,
    "AMD Radeon RX 550X": 32,

    # ===== Apple integrated GPU class =====
    "Apple M4 Max GPU": 98,
    "Apple M4 Pro GPU": 90,
    "Apple M4 GPU": 78,
    "Apple M3 Max GPU": 94,
    "Apple M3 Pro GPU": 86,
    "Apple M3 GPU": 74,
    "Apple M2 Max GPU": 88,
    "Apple M2 Pro GPU": 80,
    "Apple M2 GPU": 66,
    "Apple M1 Max GPU": 82,
    "Apple M1 Pro GPU": 74,
    "Apple M1 GPU": 58,
}


# ===== OPTIONS DROPDOWN WEBSITE =====

CPU_OPTIONS = sorted(CPU_MODEL_SCORES.keys(), key=lambda x: x.lower())
GPU_OPTIONS = sorted(GPU_MODEL_SCORES.keys(), key=lambda x: x.lower())

RAM_OPTIONS = [4, 8, 12, 16, 24, 32, 64]
STORAGE_SIZE_OPTIONS = [128, 256, 512, 1024, 2048]
STORAGE_TYPE_OPTIONS = ["HDD", "SATA SSD", "NVMe SSD"]


# ===== ALIAS GENERATOR =====

def generate_aliases(display_name):
    aliases = set()
    base = clean_text(display_name)

    if not base:
        return aliases

    aliases.add(base)

    compact = base

    # Buang vendor/label umum supaya input pendek tetap match.
    remove_words = [
        "intel",
        "amd",
        "nvidia",
        "geforce",
        "qualcomm",
        "processor",
        "graphics",
        "laptop gpu",
        "gpu",
    ]

    for word in remove_words:
        compact = re.sub(rf"\b{re.escape(word)}\b", " ", compact)
        compact = re.sub(r"\s+", " ", compact).strip()

    if compact:
        aliases.add(compact)

    # Intel Core i7 12700H -> i7 12700h
    intel_match = re.search(
        r"\bcore\s+(i3|i5|i7|i9)\s+(\d{4,5}\s*[a-z]{0,3})\b",
        base
    )
    if intel_match:
        aliases.add(f"{intel_match.group(1)} {intel_match.group(2)}".strip())

    # Intel Core Ultra 7 155H -> core ultra 7 155h / ultra 7 155h
    ultra_match = re.search(
        r"\bcore\s+ultra\s+(3|5|7|9)\s+(\d{3,4}\s*[a-z]{0,5}(?:\s+plus)?)\b",
        base
    )
    if ultra_match:
        aliases.add(f"core ultra {ultra_match.group(1)} {ultra_match.group(2)}".strip())
        aliases.add(f"ultra {ultra_match.group(1)} {ultra_match.group(2)}".strip())

    # AMD Ryzen 7 5800H -> Ryzen 7 5800H
    ryzen_match = re.search(r"\bryzen\s+(3|5|7|9)\s+(\d{4}\s*[a-z0-9]{0,5})\b", base)
    if ryzen_match:
        aliases.add(f"ryzen {ryzen_match.group(1)} {ryzen_match.group(2)}".strip())

    # Ryzen AI / Ryzen AI Max
    ryzen_ai_match = re.search(r"\bryzen\s+ai\s+(.+)\b", base)
    if ryzen_ai_match:
        aliases.add(f"ryzen ai {ryzen_ai_match.group(1)}".strip())

    # Alias variasi suffix Ryzen AI
    ryzen_ai_model_match = re.search(
        r"\bryzen\s+ai\s+(3|5|7|9)\s*(hx|h|hs|pro)?\s*(\d{3})\b",
        base
    )
    if ryzen_ai_model_match:
        tier = ryzen_ai_model_match.group(1)
        suffix = ryzen_ai_model_match.group(2) or ""
        model = ryzen_ai_model_match.group(3)

        aliases.add(f"ryzen ai {tier} {model}".strip())
        aliases.add(f"ryzen ai {tier} h {model}".strip())
        aliases.add(f"ryzen ai {tier} hx {model}".strip())
        aliases.add(f"ryzen ai {tier} hs {model}".strip())
        aliases.add(f"ryzen ai {tier} pro {model}".strip())
        if suffix:
            aliases.add(f"ryzen ai {tier} {suffix} {model}".strip())

    # RTX/GTX/MX/RX pendek.
    gpu_short_match = re.search(
        r"\b(rtx|gtx|mx|rx)\s+\d{3,4}(?:m|s|x)?(\s*ti|\s*super|\s*xt)?(?:\s*max\s*q)?\b",
        base
    )
    if gpu_short_match:
        aliases.add(gpu_short_match.group(0).strip())

    # Radeon RX 6600M -> RX 6600M
    radeon_rx_match = re.search(r"\bradeon\s+(rx\s+\d{4}(?:m|s|x)?(?:\s*xt)?)\b", base)
    if radeon_rx_match:
        aliases.add(radeon_rx_match.group(1).strip())

    # Radeon 780M / Vega 8 / Arc A370M / Intel iGPU.
    for pattern in [
        r"\bradeon\s+\d{3}m\b",
        r"\bradeon\s+vega\s+\d+\b",
        r"\barc\s+a\d{3}m\b",
        r"\barc\s+graphics\s+\d{3}[tv]\b",
        r"\biris\s+xe\b",
        r"\buhd\s+graphics\s+\d+\b",
        r"\bhd\s+graphics\s+\d+\b",
    ]:
        m = re.search(pattern, base)
        if m:
            aliases.add(m.group(0).strip())

    # Apple M4 Max -> M4 Max, Apple M4 Max GPU -> M4 Max GPU
    apple_match = re.search(r"\bapple\s+(m\d(?:\s+(?:pro|max))?)(?:\s+gpu)?\b", base)
    if apple_match:
        aliases.add(apple_match.group(1).strip())
        aliases.add((apple_match.group(1) + " gpu").strip())

    cleaned_aliases = set()
    for alias in aliases:
        alias = clean_text(alias)
        if alias:
            cleaned_aliases.add(alias)

    return cleaned_aliases


# ===== HELPER: MATCH MANUAL SCORE =====

def get_manual_score(text, score_dict):
    text = clean_text(text)

    if not text:
        return None, None

    alias_items = []
    for display_name, score in score_dict.items():
        aliases = generate_aliases(display_name)
        for alias in aliases:
            alias_items.append((alias, display_name, score))

    # Prioritaskan alias paling spesifik
    alias_items = sorted(alias_items, key=lambda x: len(x[0]), reverse=True)

    for alias, display_name, score in alias_items:
        if alias in text:
            return score, display_name

    return None, None


# ===== HELPER: DETEKSI MODEL CPU INTEL =====

def extract_intel_generation_and_suffix(text):
    text = clean_text(text)

    model_match = re.search(
        r"\b(i3|i5|i7|i9|core i3|core i5|core i7|core i9)\s*(\d{4,5})([a-z]{0,3})\b",
        text
    )

    if not model_match:
        return None, ""

    model_number = model_match.group(2)
    suffix = model_match.group(3)

    if len(model_number) >= 5:
        generation = int(model_number[:2])
    else:
        generation = int(model_number[0])

    return generation, suffix


# ===== HELPER: DETEKSI MODEL AMD RYZEN NON-AI =====

def extract_ryzen_generation_and_suffix(text):
    text = clean_text(text)

    model_match = re.search(r"\bryzen\s*(3|5|7|9)\s*(\d{4})([a-z0-9]{0,5})\b", text)

    if not model_match:
        return None, ""

    model_number = model_match.group(2)
    suffix = model_match.group(3)

    generation = int(model_number[0])

    return generation, suffix


# ===== HELPER: DETEKSI AMD RYZEN AI =====

def extract_ryzen_ai_tier_suffix_model(text):
    text = clean_text(text)

    model_match = re.search(
        r"\bryzen\s+ai\s+(3|5|7|9)\s*(hx|h|hs|pro)?\s*(\d{3})\b",
        text
    )

    if not model_match:
        return None, "", None

    tier = int(model_match.group(1))
    suffix = model_match.group(2) or ""
    model_number = int(model_match.group(3))

    return tier, suffix, model_number


# ===== HELPER: DETEKSI INTEL CORE ULTRA =====

def extract_core_ultra_class(text):
    text = clean_text(text)
    model_match = re.search(r"\b(core\s+ultra|ultra)\s*(3|5|7|9)\b", text)

    if not model_match:
        return None

    return int(model_match.group(2))


# ===== CPU SCORE DETAIL =====

def cpu_score_detail(cpu_name):
    text = clean_text(cpu_name)

    if text == "":
        return {
            "score": 35,
            "status": "unknown",
            "matched_name": None,
            "message": "CPU tidak diisi, sistem menggunakan skor default."
        }

    manual_score, matched_name = get_manual_score(text, CPU_MODEL_SCORES)
    if manual_score is not None:
        return {
            "score": manual_score,
            "status": "recognized",
            "matched_name": matched_name,
            "message": f"CPU dikenali sebagai {matched_name}."
        }

    score = 35
    recognized = False

    # Fallback AMD Ryzen AI

    ryzen_ai_tier, ryzen_ai_suffix, ryzen_ai_model = extract_ryzen_ai_tier_suffix_model(text)

    if ryzen_ai_tier is not None:
        recognized = True

        if ryzen_ai_tier == 9:
            score = 88
        elif ryzen_ai_tier == 7:
            score = 80
        elif ryzen_ai_tier == 5:
            score = 70
        else:
            score = 58

        # Penyesuaian skor berdasarkan model Ryzen AI
        if ryzen_ai_model >= 475:
            score += 10
        elif ryzen_ai_model >= 470:
            score += 9
        elif ryzen_ai_model >= 465:
            score += 6
        elif ryzen_ai_model >= 450:
            score += 8
        elif ryzen_ai_model >= 395:
            score += 12
        elif ryzen_ai_model >= 390:
            score += 8
        elif ryzen_ai_model >= 385:
            score += 6
        elif ryzen_ai_model >= 375:
            score += 10
        elif ryzen_ai_model >= 370:
            score += 8
        elif ryzen_ai_model >= 365:
            score += 3
        elif ryzen_ai_model >= 350:
            score += 8
        elif ryzen_ai_model >= 340:
            score += 8
        elif ryzen_ai_model >= 330:
            score += 2

        if ryzen_ai_suffix == "hx":
            score += 2
        elif ryzen_ai_suffix in ["h", "hs"]:
            score += 1

        final_score = max(1, min(int(round(score)), 100))

        return {
            "score": final_score,
            "status": "estimated",
            "matched_name": None,
            "message": "CPU Ryzen AI dikenali secara umum, skor dihitung berdasarkan tier, seri model, dan suffix performa."
        }

    # Intel Core Ultra fallback
    ultra_class = extract_core_ultra_class(text)
    if ultra_class is not None:
        recognized = True
        if ultra_class == 9:
            score = 92
        elif ultra_class == 7:
            score = 84
        elif ultra_class == 5:
            score = 74
        else:
            score = 58

    # Skor dasar berdasarkan kelas processor
    elif "celeron" in text:
        score = 20
        recognized = True
    elif "pentium" in text:
        score = 27
        recognized = True
    elif "atom" in text:
        score = 12
        recognized = True
    elif "athlon" in text:
        score = 25
        recognized = True
    elif re.search(r"\ba\d{1,2}\b", text):
        score = 18
        recognized = True
    elif "core m" in text or re.search(r"\bm\d\b", text):
        score = 26
        recognized = True
    elif "core 2 duo" in text:
        score = 10
        recognized = True
    elif "core i3" in text or re.search(r"\bi3\b", text):
        score = 45
        recognized = True
    elif "core i5" in text or re.search(r"\bi5\b", text):
        score = 62
        recognized = True
    elif "core i7" in text or re.search(r"\bi7\b", text):
        score = 72
        recognized = True
    elif "core i9" in text or re.search(r"\bi9\b", text):
        score = 86
        recognized = True
    elif "ryzen 3" in text:
        score = 45
        recognized = True
    elif "ryzen 5" in text:
        score = 62
        recognized = True
    elif "ryzen 7" in text:
        score = 74
        recognized = True
    elif "ryzen 9" in text:
        score = 88
        recognized = True
    elif "snapdragon x elite" in text:
        score = 82
        recognized = True
    elif "snapdragon x plus" in text:
        score = 72
        recognized = True
    elif "apple m4" in text:
        score = 96
        recognized = True
    elif "apple m3" in text:
        score = 92
        recognized = True
    elif "apple m2" in text:
        score = 85
        recognized = True
    elif "apple m1" in text:
        score = 75
        recognized = True

    # Tambahan berdasarkan generasi Intel dari format 11th/12th/13th/14th
    if "14th" in text or "14 gen" in text or "14th gen" in text:
        score += 12
    elif "13th" in text or "13 gen" in text or "13th gen" in text:
        score += 11
    elif "12th" in text or "12 gen" in text or "12th gen" in text:
        score += 9
    elif "11th" in text or "11 gen" in text or "11th gen" in text:
        score += 6
    elif "10th" in text or "10 gen" in text or "10th gen" in text:
        score += 3
    elif "9th" in text or "9 gen" in text or "9th gen" in text:
        score += 1

    # Tambahan berdasarkan nomor model Intel
    intel_generation, intel_suffix = extract_intel_generation_and_suffix(text)
    if intel_generation is not None:
        recognized = True
        if intel_generation >= 14:
            score += 12
        elif intel_generation == 13:
            score += 11
        elif intel_generation == 12:
            score += 9
        elif intel_generation == 11:
            score += 6
        elif intel_generation == 10:
            score += 3
        elif intel_generation <= 8:
            score -= 3

        if "hx" in intel_suffix:
            score += 10
        elif "hk" in intel_suffix:
            score += 9
        elif "h" in intel_suffix:
            score += 7
        elif "p" in intel_suffix:
            score += 3
        elif "g" in intel_suffix:
            score += 2
        elif "u" in intel_suffix or "y" in intel_suffix:
            score -= 4

    # Tambahan berdasarkan nomor model Ryzen non-AI
    ryzen_generation, ryzen_suffix = extract_ryzen_generation_and_suffix(text)
    if ryzen_generation is not None:
        recognized = True
        if ryzen_generation >= 9:
            score += 14
        elif ryzen_generation == 8:
            score += 12
        elif ryzen_generation == 7:
            score += 9
        elif ryzen_generation == 6:
            score += 6
        elif ryzen_generation == 5:
            score += 4
        elif ryzen_generation <= 4:
            score -= 2

        if "x3d" in ryzen_suffix:
            score += 8
        elif "hx" in ryzen_suffix:
            score += 10
        elif "hs" in ryzen_suffix:
            score += 8
        elif "h" in ryzen_suffix:
            score += 7
        elif "u" in ryzen_suffix:
            score -= 4

    # Jika tidak ada nomor model, tetap baca suffix sederhana
    if intel_generation is None and ryzen_generation is None:
        if "x3d" in text:
            score += 8
        elif "hx" in text:
            score += 8
        elif re.search(r"\bhk\b", text):
            score += 8
        elif re.search(r"\bhs\b", text):
            score += 7
        elif re.search(r"\bh\b", text):
            score += 6
        elif re.search(r"\bp\b", text):
            score += 3
        elif re.search(r"\bu\b", text) or re.search(r"\by\b", text):
            score -= 4

    final_score = max(1, min(int(round(score)), 100))

    if recognized:
        status = "estimated"
        message = "CPU dikenali secara umum, skor dihitung berdasarkan kelas, generasi, dan suffix performa."
    else:
        status = "unknown"
        message = "CPU tidak dikenali secara spesifik, sistem menggunakan skor estimasi default."

    return {
        "score": final_score,
        "status": status,
        "matched_name": None,
        "message": message
    }


# ===== GPU SCORE DETAIL =====

def gpu_score_detail(gpu_name):
    text = clean_text(gpu_name)

    if text == "":
        return {
            "score": 20,
            "status": "unknown",
            "matched_name": None,
            "message": "GPU tidak diisi, sistem menggunakan skor default."
        }

    manual_score, matched_name = get_manual_score(text, GPU_MODEL_SCORES)
    if manual_score is not None:
        return {
            "score": manual_score,
            "status": "recognized",
            "matched_name": matched_name,
            "message": f"GPU dikenali sebagai {matched_name}."
        }

    # NVIDIA RTX fallback berdasarkan nomor seri
    rtx_match = re.search(r"\brtx\s*(\d{4})(\s*ti)?\b", text)
    if rtx_match:
        model = int(rtx_match.group(1))
        has_ti = bool(rtx_match.group(2))

        if model >= 5090:
            score = 100
        elif model >= 5080:
            score = 97
        elif model >= 5070:
            score = 94 if has_ti else 91
        elif model >= 5060:
            score = 88
        elif model >= 5050:
            score = 82
        elif model >= 4090:
            score = 100
        elif model >= 4080:
            score = 95
        elif model >= 4070:
            score = 90
        elif model >= 4060:
            score = 85
        elif model >= 4050:
            score = 78
        elif model >= 3080:
            score = 92 if has_ti else 88
        elif model >= 3070:
            score = 86 if has_ti else 84
        elif model >= 3060:
            score = 78
        elif model >= 3050:
            score = 73 if has_ti else 70
        elif model >= 2080:
            score = 76
        elif model >= 2070:
            score = 70
        elif model >= 2060:
            score = 65
        elif model >= 2050:
            score = 60
        else:
            score = 55

        return {
            "score": score,
            "status": "estimated",
            "matched_name": None,
            "message": "GPU RTX dikenali secara umum berdasarkan seri, tetapi model spesifik tidak ada di daftar utama."
        }

    # NVIDIA GTX fallback
    gtx_match = re.search(r"\bgtx\s*(\d{3,4})(\s*ti)?\b", text)
    if gtx_match:
        model = int(gtx_match.group(1))
        has_ti = bool(gtx_match.group(2))
        is_max_q = "max q" in text or "maxq" in text

        if model >= 1660:
            score = 67 if has_ti else 65
        elif model >= 1650:
            score = 60 if has_ti else 58
        elif model >= 1080:
            score = 68
        elif model >= 1070:
            score = 62
        elif model >= 1060:
            score = 55
        elif model >= 1050:
            score = 48 if has_ti else 45
        elif model >= 965:
            score = 40
        elif model >= 960:
            score = 38
        elif model >= 950:
            score = 35
        elif model >= 860:
            score = 34
        elif model >= 850:
            score = 32
        else:
            score = 30

        if is_max_q:
            score -= 3

        score = max(1, min(int(round(score)), 100))

        return {
            "score": score,
            "status": "estimated",
            "matched_name": None,
            "message": "GPU GTX dikenali secara umum berdasarkan seri, tetapi model spesifik tidak ada di daftar utama."
        }

    # NVIDIA MX fallback
    mx_match = re.search(r"\bmx\s*(\d{3})\b", text)
    if mx_match:
        model = int(mx_match.group(1))
        if model >= 570:
            score = 48
        elif model >= 550:
            score = 46
        elif model >= 450:
            score = 44
        elif model >= 350:
            score = 40
        else:
            score = 34

        return {
            "score": score,
            "status": "estimated",
            "matched_name": None,
            "message": "GPU NVIDIA MX dikenali secara umum, skor dihitung sebagai GPU entry-level."
        }

    # Radeon RX fallback
    rx_match = re.search(r"\bradeon\s+rx\s*(\d{4})(m|s|x|xt)?\b", text)
    if rx_match:
        model = int(rx_match.group(1))
        if model >= 7900:
            score = 94
        elif model >= 7800:
            score = 88
        elif model >= 7700:
            score = 82
        elif model >= 7600:
            score = 78
        elif model >= 6800:
            score = 82
        elif model >= 6700:
            score = 76
        elif model >= 6600:
            score = 68
        elif model >= 6500:
            score = 58
        elif model >= 5600:
            score = 58
        elif model >= 5500:
            score = 52
        else:
            score = 45

        return {
            "score": score,
            "status": "estimated",
            "matched_name": None,
            "message": "GPU Radeon RX dikenali secara umum, tetapi model spesifik tidak ditemukan."
        }

    # Radeon integrated fallback
    # Kalibrasi iGPU di bawah batas Gaming
    if "radeon" in text:
        if "890m" in text:
            score = 57
        elif "880m" in text:
            score = 54
        elif "780m" in text:
            score = 50
        elif "760m" in text:
            score = 46
        elif "740m" in text:
            score = 42
        elif "680m" in text:
            score = 46
        elif "660m" in text:
            score = 40
        elif "610m" in text:
            score = 25
        elif "vega 10" in text:
            score = 35
        elif "vega 8" in text:
            score = 34
        elif "vega 7" in text:
            score = 31
        elif "vega 6" in text:
            score = 28
        elif "vega 3" in text:
            score = 20
        elif "vega" in text:
            score = 30
        else:
            score = 30

        return {
            "score": score,
            "status": "estimated",
            "matched_name": None,
            "message": "GPU Radeon integrated dikenali. Skor dikalibrasi sebagai iGPU modern/casual gaming, bukan dedicated gaming GPU."
        }

    # Intel integrated fallback
    # Kalibrasi iGPU di bawah batas Gaming
    if "arc" in text:
        return {
            "score": 54,
            "status": "estimated",
            "matched_name": None,
            "message": "GPU Intel Arc integrated dikenali. Skor dikalibrasi untuk gaming ringan/e-sports, bukan dedicated gaming GPU."
        }

    if "iris" in text:
        return {
            "score": 42,
            "status": "estimated",
            "matched_name": None,
            "message": "GPU Intel Iris dikenali sebagai integrated graphics kelas menengah."
        }

    if "integrated" in text or "intel" in text or "uhd" in text or "hd graphics" in text:
        return {
            "score": 25,
            "status": "estimated",
            "matched_name": None,
            "message": "GPU terdeteksi sebagai integrated graphics."
        }

    return {
        "score": 35,
        "status": "unknown",
        "matched_name": None,
        "message": "GPU tidak dikenali secara spesifik, sistem menggunakan skor estimasi default."
    }


# ===== FUNGSI SCORE =====

def cpu_score_input(cpu_name):
    return cpu_score_detail(cpu_name)["score"]


def gpu_score_input(gpu_name):
    return gpu_score_detail(gpu_name)["score"]


# ===== RAM SCORE INPUT =====

def ram_score_detail(ram):
    try:
        ram = int(ram)
    except (TypeError, ValueError):
        return {
            "score": 30,
            "status": "unknown",
            "message": "RAM tidak valid, sistem menggunakan skor default."
        }

    if ram <= 4:
        score = 30
    elif ram <= 8:
        score = 55
    elif ram <= 12:
        score = 65
    elif ram <= 16:
        score = 80
    elif ram <= 24:
        score = 88
    elif ram <= 32:
        score = 95
    else:
        score = 100

    return {
        "score": score,
        "status": "recognized",
        "message": f"RAM {ram} GB berhasil dinilai."
    }


def ram_score_input(ram):
    return ram_score_detail(ram)["score"]


# ===== STORAGE SCORE INPUT =====

def storage_score_detail(storage_size, storage_type="SSD"):
    try:
        storage_size = int(storage_size)
    except (TypeError, ValueError):
        return {
            "score": 40,
            "status": "unknown",
            "message": "Ukuran storage tidak valid, sistem menggunakan skor default."
        }

    storage_type_clean = clean_text(storage_type)

    # Skor kapasitas
    if storage_size <= 128:
        capacity_score = 45
    elif storage_size <= 256:
        capacity_score = 60
    elif storage_size <= 512:
        capacity_score = 75
    elif storage_size <= 1024:
        capacity_score = 90
    else:
        capacity_score = 100

    # Skor jenis storage
    if "nvme" in storage_type_clean:
        type_bonus = 10
        storage_status = "recognized"
        storage_message = "Storage NVMe SSD memiliki nilai lebih tinggi karena mendukung akses data lebih cepat."
    elif "ssd" in storage_type_clean:
        type_bonus = 5
        storage_status = "recognized"
        storage_message = "Storage SSD memiliki nilai lebih baik dibanding HDD."
    elif "hdd" in storage_type_clean:
        type_bonus = -20
        storage_status = "recognized"
        storage_message = "Storage HDD memiliki skor lebih rendah karena kecepatan akses data lebih lambat."
    else:
        type_bonus = 0
        storage_status = "estimated"
        storage_message = "Jenis storage tidak dikenali secara spesifik, skor dihitung berdasarkan kapasitas."

    final_score = capacity_score + type_bonus
    final_score = max(1, min(int(round(final_score)), 100))

    return {
        "score": final_score,
        "status": storage_status,
        "message": storage_message
    }


def storage_score_input(storage_size, storage_type="SSD"):
    return storage_score_detail(storage_size, storage_type)["score"]


# ===== HITUNG SKOR KOMPONEN =====

def get_component_scores(cpu_name, gpu_name, ram, storage_size, storage_type="SSD"):
    cpu_detail = cpu_score_detail(cpu_name)
    gpu_detail = gpu_score_detail(gpu_name)
    ram_detail = ram_score_detail(ram)
    storage_detail = storage_score_detail(storage_size, storage_type)

    return {
        "cpu_score": cpu_detail["score"],
        "gpu_score": gpu_detail["score"],
        "ram_score": ram_detail["score"],
        "storage_score": storage_detail["score"],
        "details": {
            "cpu": cpu_detail,
            "gpu": gpu_detail,
            "ram": ram_detail,
            "storage": storage_detail
        }
    }


# ===== CONFIDENCE LEVEL =====

def calculate_confidence(category_scores):
    """
    category_scores harus berisi:
    {
        "Gaming": nilai,
        "Editing": nilai,
        "Daily Use": nilai,
        "All-Rounder": nilai,
        "Performance": nilai
    }
    """

    filtered_scores = {
        key: value
        for key, value in category_scores.items()
        if key != "Performance"
    }

    sorted_scores = sorted(
        filtered_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_category, top_score = sorted_scores[0]
    second_category, second_score = sorted_scores[1]

    gap = top_score - second_score

    if gap >= 10:
        confidence = "Tinggi"
        message = "Selisih skor kategori cukup besar, sehingga hasil klasifikasi relatif kuat."
    elif gap >= 5:
        confidence = "Sedang"
        message = "Selisih skor kategori sedang, hasil klasifikasi cukup baik tetapi masih memiliki kedekatan dengan kategori lain."
    else:
        confidence = "Rendah"
        message = (
            f"Skor {top_category} cukup dekat dengan {second_category}, "
            "sehingga hasil sebaiknya dibaca sebagai kecenderungan, bukan keputusan mutlak."
        )

    return {
        "top_category": top_category,
        "top_score": round(top_score, 2),
        "second_category": second_category,
        "second_score": round(second_score, 2),
        "gap": round(gap, 2),
        "confidence": confidence,
        "message": message
    }


# ===== QUICK TEST =====

if __name__ == "__main__":
    test_cpu = [
        "AMD Ryzen AI 9 365",
        "AMD Ryzen AI 9 465",
        "AMD Ryzen AI 9 H 465",
        "AMD Ryzen 9 9955HX3D",
        "Intel Pentium Gold 7505",
        "Intel Core i7-12700H",
    ]

    test_gpu = [
        "RTX 4050",
        "NVIDIA GeForce RTX 4050 Laptop GPU",
        "GTX 1660 Ti",
        "GTX 1660 Ti Max-Q",
        "GTX 1050",
        "Intel Iris Xe",
        "Intel Arc Graphics 130T",
        "Intel Arc Graphics 140T",
        "AMD Radeon 890M",
        "AMD Radeon 780M",
    ]

    print("=== TEST CPU ===")
    for cpu in test_cpu:
        detail = cpu_score_detail(cpu)
        print(cpu, "=>", detail["score"], "|", detail["status"], "|", detail["matched_name"])

    print("\n=== TEST GPU ===")
    for gpu in test_gpu:
        detail = gpu_score_detail(gpu)
        print(gpu, "=>", detail["score"], "|", detail["status"], "|", detail["matched_name"])

    print("\nJumlah CPU_OPTIONS:", len(CPU_OPTIONS))
    print("Jumlah GPU_OPTIONS:", len(GPU_OPTIONS))
