import os
import pandas as pd

from scoring_utils import (
    cpu_score_input,
    gpu_score_input,
    ram_score_input,
    storage_score_input
)

# ===== LOAD DATASET LAPTOP =====

laptop = pd.read_csv("dataset/laptop.csv")

os.makedirs("processed", exist_ok=True)

# ===== SCORING SPESIFIKASI =====

laptop = laptop.copy()

laptop["cpu_score"] = laptop["processor_name"].apply(cpu_score_input)
laptop["gpu_score"] = laptop["graphics"].apply(gpu_score_input)
laptop["ram_score"] = laptop["ram(GB)"].apply(ram_score_input)


# ===== STORAGE PROCESSING =====

def get_storage_type(row):
    ssd = pd.to_numeric(row["ssd(GB)"], errors="coerce")
    hdd = pd.to_numeric(row["Hard Disk(GB)"], errors="coerce")

    if pd.isna(ssd):
        ssd = 0
    if pd.isna(hdd):
        hdd = 0

    if ssd > 0:
        return "SSD"
    elif hdd > 0:
        return "HDD"
    else:
        return "SSD"


def get_storage_size(row):
    ssd = pd.to_numeric(row["ssd(GB)"], errors="coerce")
    hdd = pd.to_numeric(row["Hard Disk(GB)"], errors="coerce")

    if pd.isna(ssd):
        ssd = 0
    if pd.isna(hdd):
        hdd = 0

    if ssd > 0:
        return int(ssd)
    elif hdd > 0:
        return int(hdd)
    else:
        return 0


laptop["storage_type"] = laptop.apply(get_storage_type, axis=1)
laptop["storage_size"] = laptop.apply(get_storage_size, axis=1)

laptop["storage_score"] = laptop.apply(
    lambda row: storage_score_input(row["storage_size"], row["storage_type"]),
    axis=1
)

# ===== HITUNG SKOR KATEGORI =====

laptop["gaming_score"] = (
    0.25 * laptop["cpu_score"] +
    0.45 * laptop["gpu_score"] +
    0.15 * laptop["ram_score"] +
    0.15 * laptop["storage_score"]
)

laptop["editing_score"] = (
    0.35 * laptop["cpu_score"] +
    0.25 * laptop["gpu_score"] +
    0.25 * laptop["ram_score"] +
    0.15 * laptop["storage_score"]
)

laptop["daily_score"] = (
    0.30 * laptop["cpu_score"] +
    0.10 * laptop["gpu_score"] +
    0.25 * laptop["ram_score"] +
    0.35 * laptop["storage_score"]
)

laptop["all_rounder_score"] = (
    0.30 * laptop["cpu_score"] +
    0.25 * laptop["gpu_score"] +
    0.25 * laptop["ram_score"] +
    0.20 * laptop["storage_score"]
)

laptop["performance_score"] = (
    0.35 * laptop["cpu_score"] +
    0.30 * laptop["gpu_score"] +
    0.20 * laptop["ram_score"] +
    0.15 * laptop["storage_score"]
)

# ===== DETEKSI GPU DEDICATED GAMING =====

def is_dedicated_gaming_gpu(gpu_name):
    """
    Mendeteksi apakah GPU termasuk GPU dedicated/discrete yang umum dipakai
    pada laptop gaming.

    Fungsi ini dipakai agar label training konsisten dengan validasi
    pada predict_recommendation.py.
    """
    gpu_name = str(gpu_name).lower().strip()

    integrated_keywords = [
        "intel arc graphics",
        "intel iris",
        "intel uhd",
        "intel hd",
        "iris xe",
        "uhd graphics",
        "hd graphics",
        "radeon 890m",
        "radeon 880m",
        "radeon 780m",
        "radeon 760m",
        "radeon 740m",
        "radeon 680m",
        "radeon 660m",
        "radeon 610m",
        "radeon graphics",
        "vega",
        "apple",
        "snapdragon",
        "adreno"
    ]

    dedicated_keywords = [
        "nvidia geforce rtx",
        "geforce rtx",
        "rtx ",
        "nvidia rtx",
        "nvidia geforce gtx",
        "geforce gtx",
        "gtx ",
        "nvidia gtx",
        "radeon rx",
        "amd radeon rx",
        "rx "
    ]

    if any(keyword in gpu_name for keyword in integrated_keywords):
        return False

    return any(keyword in gpu_name for keyword in dedicated_keywords)


# ===== LABEL KATEGORI FINAL =====

def assign_usage_category(row):
    cpu_s = row["cpu_score"]
    gpu_s = row["gpu_score"]
    ram_s = row["ram_score"]
    storage_s = row["storage_score"]

    gaming_s = row["gaming_score"]
    editing_s = row["editing_score"]
    performance_s = row["performance_score"]

    gpu_name = row.get("graphics", "")
    dedicated_gaming_gpu = is_dedicated_gaming_gpu(gpu_name)
    gaming_editing_gap = abs(gaming_s - editing_s)

    # ===== ALL-ROUNDER =====

    if (
        cpu_s >= 75 and
        gpu_s >= 70 and
        ram_s >= 80 and
        storage_s >= 75 and
        gaming_s >= 70 and
        editing_s >= 70 and
        performance_s >= 70
    ):
        return "All-Rounder"

    # ===== GAMING DEDICATED =====

    elif (
        dedicated_gaming_gpu and
        gpu_s >= 70 and
        cpu_s >= 60 and
        ram_s >= 55 and
        storage_s >= 60 and
        gaming_s >= 70 and
        (
            gaming_s >= editing_s or
            gaming_editing_gap <= 5
        )
    ):
        return "Gaming"

    # ===== EDITING =====

    elif (
        cpu_s >= 65 and
        gpu_s >= 35 and
        ram_s >= 80 and
        storage_s >= 75 and
        editing_s >= 65
    ):
        return "Editing"

    # ===== GAMING =====

    elif (
        gpu_s >= 58 and
        ram_s >= 55 and
        storage_s >= 60 and
        gaming_s >= 58
    ):
        return "Gaming"

    # ===== DAILY USE =====

    else:
        return "Daily Use"

laptop["usage_category"] = laptop.apply(assign_usage_category, axis=1)

# ===== BUDGET CATEGORY UNTUK REFERENSI LAPTOP =====

laptop["price"] = pd.to_numeric(laptop["price"], errors="coerce")

try:
    laptop["budget_category"] = pd.qcut(
        laptop["price"],
        q=3,
        labels=["Low Budget", "Mid Budget", "High Budget"]
    )
except ValueError:
    low_limit = laptop["price"].quantile(0.33)
    high_limit = laptop["price"].quantile(0.66)

    def assign_budget(price):
        if pd.isna(price):
            return "Unknown"
        elif price <= low_limit:
            return "Low Budget"
        elif price <= high_limit:
            return "Mid Budget"
        else:
            return "High Budget"

    laptop["budget_category"] = laptop["price"].apply(assign_budget)

# ===== REKOMENDASI TAMBAHAN =====

def recommendation_note(row):
    notes = []

    if row["usage_category"] == "Gaming":
        notes.append("Cocok untuk gaming karena memiliki GPU yang cukup kuat")

    if row["usage_category"] == "Editing":
        notes.append("Cocok untuk editing karena memiliki CPU, RAM, dan storage yang mendukung")

    if row["usage_category"] == "All-Rounder":
        notes.append("Cocok untuk penggunaan serbaguna karena kuat untuk gaming dan editing sekaligus")

    if row["usage_category"] == "Daily Use":
        notes.append("Cocok untuk penggunaan harian seperti browsing, mengetik, meeting online, dan tugas ringan")

    if row["cpu_score"] >= 75 and row["ram_score"] >= 80:
        notes.append("Cocok untuk programming dan multitasking")

    if row["cpu_score"] >= 80 and row["gpu_score"] >= 70:
        notes.append("Cocok untuk AI ringan dan image processing")

    if row["storage_score"] >= 75:
        notes.append("Memiliki storage yang mendukung workflow lebih cepat")

    return "; ".join(notes)


laptop["recommendation_note"] = laptop.apply(recommendation_note, axis=1)

# ===== ROUNDING SCORE =====

score_cols = [
    "cpu_score",
    "gpu_score",
    "ram_score",
    "storage_score",
    "gaming_score",
    "editing_score",
    "daily_score",
    "all_rounder_score",
    "performance_score"
]

laptop.loc[:, score_cols] = laptop[score_cols].round(2)

# ===== DATASET 1: MODEL TRAINING DATASET =====

model_training_columns = [
    "processor_name",
    "graphics",
    "ram(GB)",
    "storage_size",
    "storage_type",
    "cpu_score",
    "gpu_score",
    "ram_score",
    "storage_score",
    "gaming_score",
    "editing_score",
    "daily_score",
    "all_rounder_score",
    "performance_score",
    "usage_category"
]

model_training_dataset = laptop[model_training_columns].copy()

model_training_path = "processed/model_training_dataset.csv"
model_training_dataset.to_csv(model_training_path, index=False)

# ===== DATASET 2: RECOMMENDATION CATALOG =====

recommendation_columns = [
    "model_name",
    "brand",
    "processor_name",
    "ram(GB)",
    "ssd(GB)",
    "Hard Disk(GB)",
    "storage_size",
    "storage_type",
    "graphics",
    "Operating System",
    "screen_size(inches)",
    "resolution (pixels)",
    "price",
    "cpu_score",
    "gpu_score",
    "ram_score",
    "storage_score",
    "gaming_score",
    "editing_score",
    "daily_score",
    "all_rounder_score",
    "performance_score",
    "usage_category",
    "budget_category",
    "recommendation_note"
]

recommendation_catalog = laptop[recommendation_columns].copy()

recommendation_path = "processed/recommendation_catalog.csv"
recommendation_catalog.to_csv(recommendation_path, index=False)

# ===== OUTPUT CHECK =====

print("=== PREPROCESSING SELESAI ===")
print("File training XGBoost dibuat:", model_training_path)
print("File katalog rekomendasi dibuat:", recommendation_path)

print("\nJumlah data training:", model_training_dataset.shape)
print("Jumlah data rekomendasi:", recommendation_catalog.shape)

print("\nDistribusi kategori penggunaan:")
print(model_training_dataset["usage_category"].value_counts())

print("\nDistribusi budget rekomendasi:")
print(recommendation_catalog["budget_category"].value_counts())

print("\nContoh data training XGBoost:")
print(model_training_dataset.head())

print("\nContoh katalog rekomendasi:")
print(recommendation_catalog.head())