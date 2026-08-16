import os
import pandas as pd
import joblib

from scoring_utils import get_component_scores


# ===== LOAD MODEL DAN DATA =====

model = joblib.load("model/xgboost_laptop_model.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

# Katalog referensi
catalog = pd.read_csv("processed/recommendation_catalog.csv")

# Katalog rekomendasi marketplace
MARKETPLACE_CATALOG_PATH = "processed/marketplace_catalog.csv"

if os.path.exists(MARKETPLACE_CATALOG_PATH):
    marketplace_catalog = pd.read_csv(MARKETPLACE_CATALOG_PATH)
else:
    marketplace_catalog = pd.DataFrame()


# ===== HITUNG SKOR KATEGORI =====

def calculate_category_scores(cpu_score, gpu_score, ram_score, storage_score):
    gaming_score = (
        0.25 * cpu_score +
        0.45 * gpu_score +
        0.15 * ram_score +
        0.15 * storage_score
    )

    editing_score = (
        0.35 * cpu_score +
        0.25 * gpu_score +
        0.25 * ram_score +
        0.15 * storage_score
    )

    daily_score = (
        0.30 * cpu_score +
        0.10 * gpu_score +
        0.25 * ram_score +
        0.35 * storage_score
    )

    all_rounder_score = (
        0.30 * cpu_score +
        0.25 * gpu_score +
        0.25 * ram_score +
        0.20 * storage_score
    )

    performance_score = (
        0.35 * cpu_score +
        0.30 * gpu_score +
        0.20 * ram_score +
        0.15 * storage_score
    )

    return {
        "Gaming": round(gaming_score, 2),
        "Editing": round(editing_score, 2),
        "Daily Use": round(daily_score, 2),
        "All-Rounder": round(all_rounder_score, 2),
        "Performance": round(performance_score, 2)
    }


# ===== DETEKSI GPU DEDICATED GAMING =====

def is_dedicated_gaming_gpu(gpu_name):
    """
    Mendeteksi apakah GPU termasuk GPU dedicated/discrete yang umum dipakai
    pada laptop gaming.

    Fungsi ini dipakai untuk kasus laptop dengan GPU gaming kuat
    seperti RTX/GTX/Radeon RX agar tidak otomatis masuk Editing hanya
    karena RAM dan storage besar.

    Catatan:
    - Integrated GPU modern seperti Intel Arc Graphics, Iris Xe,
      Radeon 780M/890M, dan Vega tetap dianggap bukan dedicated GPU.
    - Validasi akhir tetap memakai gpu_score, bukan keyword saja.
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


# ===== FORMAT HARGA =====

def format_price(price):
    try:
        price = float(price)
        return "Rp {:,.0f}".format(price).replace(",", ".")
    except (TypeError, ValueError):
        return "-"


# ===== KATEGORI FINAL =====

def determine_final_category(
    model_category,
    cpu_score,
    gpu_score,
    ram_score,
    storage_score,
    gpu_name=""
):
    category_scores = calculate_category_scores(
        cpu_score,
        gpu_score,
        ram_score,
        storage_score
    )

    gaming_s = category_scores["Gaming"]
    editing_s = category_scores["Editing"]
    performance_s = category_scores["Performance"]

    dedicated_gaming_gpu = is_dedicated_gaming_gpu(gpu_name)
    gaming_editing_gap = abs(gaming_s - editing_s)
    model_category = str(model_category).strip()

    # ===== VALIDASI KATEGORI =====

    all_rounder_valid = (
        cpu_score >= 75 and
        gpu_score >= 70 and
        ram_score >= 80 and
        storage_score >= 75 and
        gaming_s >= 70 and
        editing_s >= 70 and
        performance_s >= 70
    )

    gaming_dedicated_valid = (
        dedicated_gaming_gpu and
        gpu_score >= 70 and
        cpu_score >= 60 and
        ram_score >= 55 and
        storage_score >= 60 and
        gaming_s >= 70 and
        (
            gaming_s >= editing_s or
            gaming_editing_gap <= 5
        )
    )

    editing_valid = (
        cpu_score >= 65 and
        gpu_score >= 35 and
        ram_score >= 80 and
        storage_score >= 75 and
        editing_s >= 65
    )

    gaming_general_valid = (
        gpu_score >= 58 and
        ram_score >= 55 and
        storage_score >= 60 and
        gaming_s >= 58
    )

    # Validasi hasil XGBoost

    if model_category == "All-Rounder" and all_rounder_valid:
        return "All-Rounder"

    if model_category == "Gaming":
        if gaming_dedicated_valid or gaming_general_valid:
            return "Gaming"

    if model_category == "Editing":
        # Prioritaskan GPU gaming dedicated
        if gaming_dedicated_valid:
            return "Gaming"

        if editing_valid:
            return "Editing"

    if model_category == "Daily Use":
        if not (
            all_rounder_valid or
            gaming_dedicated_valid or
            editing_valid or
            gaming_general_valid
        ):
            return "Daily Use"

    # Kategori alternatif berdasarkan threshold

    if all_rounder_valid:
        return "All-Rounder"

    if gaming_dedicated_valid:
        return "Gaming"

    if editing_valid:
        return "Editing"

    if gaming_general_valid:
        return "Gaming"

    return "Daily Use"


# ===== CONFIDENCE / KEJELASAN HASIL =====

def calculate_result_confidence(final_category, category_scores, cpu_score, gpu_score, ram_score, storage_score):
    filtered_scores = {
        key: value
        for key, value in category_scores.items()
        if key != "Performance"
    }

    selected_score = filtered_scores[final_category]

    other_scores = {
        key: value
        for key, value in filtered_scores.items()
        if key != final_category
    }

    closest_category, closest_score = max(
        other_scores.items(),
        key=lambda x: x[1]
    )

    gap = abs(selected_score - closest_score)

    if final_category == "Daily Use":
        blocking_reasons = []

        if cpu_score < 65:
            blocking_reasons.append("CPU belum memenuhi ambang Editing")
        if gpu_score < 58:
            blocking_reasons.append("GPU belum memenuhi ambang Gaming")
        if ram_score < 55:
            blocking_reasons.append("RAM belum memenuhi ambang Gaming")
        if storage_score < 60:
            blocking_reasons.append("storage belum memenuhi ambang Gaming")

        if blocking_reasons:
            return {
                "top_category": final_category,
                "top_score": round(selected_score, 2),
                "second_category": closest_category,
                "second_score": round(closest_score, 2),
                "gap": round(gap, 2),
                "confidence": "Tinggi",
                "message": (
                    "Spesifikasi tidak memenuhi ambang minimum untuk kategori Gaming, Editing, "
                    "atau All-Rounder karena " + ", ".join(blocking_reasons) + ". "
                    "Hasil Daily Use menjadi cukup tegas karena laptop lebih sesuai untuk penggunaan ringan."
                )
            }

        return {
            "top_category": final_category,
            "top_score": round(selected_score, 2),
            "second_category": closest_category,
            "second_score": round(closest_score, 2),
            "gap": round(gap, 2),
            "confidence": "Sedang",
            "message": (
                "Laptop dikategorikan sebagai Daily Use karena belum memenuhi ambang kategori berat. "
                "Beberapa skor masih cukup berdekatan, sehingga hasil dibaca sebagai kecenderungan penggunaan yang paling sesuai."
            )
        }

    if final_category == "Gaming":
        if gpu_score >= 70 and ram_score >= 80 and storage_score >= 75:
            confidence = "Tinggi"
            message = "GPU, RAM, dan storage sudah kuat untuk mendukung kategori Gaming secara tegas."
        elif gpu_score >= 58 and ram_score >= 55 and storage_score >= 60:
            confidence = "Sedang"
            message = (
                "Spesifikasi sudah memenuhi ambang Gaming, tetapi beberapa komponen masih berada pada level menengah. "
                "Hasil tetap valid karena GPU menjadi komponen utama pada kategori ini."
            )
        else:
            confidence = "Rendah"
            message = (
                "Kategori Gaming dapat terbaca, tetapi beberapa komponen berada dekat batas minimum sehingga hasil perlu ditinjau ulang."
            )

        return {
            "top_category": final_category,
            "top_score": round(selected_score, 2),
            "second_category": closest_category,
            "second_score": round(closest_score, 2),
            "gap": round(gap, 2),
            "confidence": confidence,
            "message": message
        }

    if final_category == "Editing":
        if cpu_score >= 75 and gpu_score >= 45 and ram_score >= 80 and storage_score >= 75:
            confidence = "Tinggi"
            message = "CPU, RAM, storage, dan GPU pendukung sudah kuat untuk mendukung kategori Editing secara tegas."
        elif cpu_score >= 65 and gpu_score >= 35 and ram_score >= 80 and storage_score >= 75:
            confidence = "Sedang"
            message = (
                "Spesifikasi sudah memenuhi ambang Editing. CPU, RAM, dan storage menjadi faktor utama, "
                "sedangkan GPU berada pada batas yang masih cukup untuk kebutuhan editing ringan hingga menengah."
            )
        else:
            confidence = "Rendah"
            message = (
                "Kategori Editing dapat terbaca, tetapi beberapa komponen masih dekat batas minimum sehingga hasil perlu ditinjau ulang."
            )

        return {
            "top_category": final_category,
            "top_score": round(selected_score, 2),
            "second_category": closest_category,
            "second_score": round(closest_score, 2),
            "gap": round(gap, 2),
            "confidence": confidence,
            "message": message
        }

    if final_category == "All-Rounder":
        if cpu_score >= 80 and gpu_score >= 78 and ram_score >= 80 and storage_score >= 80:
            confidence = "Tinggi"
            message = (
                "CPU, GPU, RAM, dan storage berada pada level tinggi, sehingga laptop sangat layak "
                "dikategorikan sebagai All-Rounder."
            )
        else:
            confidence = "Sedang"
            message = (
                "Spesifikasi memenuhi ambang All-Rounder karena mampu mendukung kebutuhan Gaming dan Editing. "
                "Kejelasan hasil dibaca cukup kuat karena laptop juga memiliki karakteristik yang relevan dengan beberapa kategori lain."
            )

        return {
            "top_category": final_category,
            "top_score": round(selected_score, 2),
            "second_category": closest_category,
            "second_score": round(closest_score, 2),
            "gap": round(gap, 2),
            "confidence": confidence,
            "message": message
        }

    return {
        "top_category": final_category,
        "top_score": round(selected_score, 2),
        "second_category": closest_category,
        "second_score": round(closest_score, 2),
        "gap": round(gap, 2),
        "confidence": "Sedang",
        "message": "Kejelasan hasil dihitung berdasarkan ambang minimum spesifikasi dan kedekatan karakteristik antar kategori."
    }


# ===== PENJELASAN HASIL KLASIFIKASI =====

def generate_explanation(category, confidence_info, component_details):
    confidence = confidence_info["confidence"]

    base_note = (
        "Hasil ini menunjukkan kecenderungan penggunaan laptop berdasarkan skor spesifikasi "
        "yang diinputkan, bukan keputusan mutlak."
    )

    if category == "Gaming":
        explanation = (
            "Laptop ini cenderung cocok untuk kebutuhan gaming karena memiliki GPU yang cukup kuat. "
            "Kategori Gaming menekankan kemampuan grafis, RAM yang memadai, dan storage yang layak "
            "untuk menjalankan game serta aktivitas visual."
        )

    elif category == "Editing":
        explanation = (
            "Laptop ini cenderung cocok untuk kebutuhan editing karena memiliki CPU, RAM, dan storage "
            "yang mendukung proses editing, desain grafis, pengolahan file, serta rendering ringan-menengah. "
            "GPU juga dinilai cukup untuk membantu proses grafis."
        )

    elif category == "Daily Use":
        explanation = (
            "Laptop ini cenderung cocok untuk penggunaan harian seperti browsing, mengetik dokumen, "
            "meeting online, pembelajaran, dan pekerjaan ringan. Spesifikasi belum memenuhi ambang minimum "
            "untuk kategori Gaming, Editing, atau All-Rounder."
        )

    elif category == "All-Rounder":
        explanation = (
            "Laptop ini cenderung termasuk kategori All-Rounder karena memiliki spesifikasi tinggi yang "
            "mendukung kebutuhan Gaming dan Editing sekaligus. Kategori ini ditujukan untuk laptop yang "
            "memiliki CPU kuat, GPU kuat, RAM besar, dan storage yang layak sehingga dapat digunakan "
            "untuk berbagai kebutuhan berat maupun harian."
        )

    else:
        explanation = "Kategori penggunaan laptop berhasil ditentukan berdasarkan evaluasi spesifikasi."

    if confidence == "Tinggi":
        explanation += (
            " Kejelasan hasil tergolong sangat kuat karena spesifikasi cukup tegas mendukung kategori akhir."
        )
    elif confidence == "Sedang":
        explanation += (
            " Kejelasan hasil tergolong cukup kuat karena spesifikasi mendukung kategori akhir, "
            "meskipun sebagian komponennya juga masih relevan untuk kategori lain."
        )
    else:
        explanation += (
            " Kejelasan hasil perlu ditinjau lebih lanjut karena beberapa komponen berada dekat dengan batas antar kategori."
        )

    warning_notes = []

    cpu_status = component_details["cpu"]["status"]
    gpu_status = component_details["gpu"]["status"]

    if cpu_status == "unknown":
        warning_notes.append(
            "CPU tidak dikenali secara spesifik sehingga skor CPU menggunakan estimasi default."
        )
    elif cpu_status == "estimated":
        warning_notes.append(
            "CPU dikenali secara umum sehingga skor CPU dihitung berdasarkan estimasi kelas/generasi."
        )

    if gpu_status == "unknown":
        warning_notes.append(
            "GPU tidak dikenali secara spesifik sehingga skor GPU menggunakan estimasi default."
        )
    elif gpu_status == "estimated":
        warning_notes.append(
            "GPU dikenali secara umum sehingga skor GPU dihitung berdasarkan estimasi kelas GPU."
        )

    if warning_notes:
        explanation += " Catatan: " + " ".join(warning_notes)

    explanation += " " + base_note

    return explanation


# ===== CONTOH APLIKASI / GAME BERDASARKAN KATEGORI =====

def get_supported_apps(category):
    supported_apps = {
        "Daily Use": [
            {
                "name": "Microsoft Word",
                "type": "Dokumen",
                "note": "Mengetik dokumen, laporan, dan tugas ringan",
                "logo_file": "word.png",
                "initial": "W"
            },
            {
                "name": "Microsoft Excel",
                "type": "Spreadsheet",
                "note": "Pengolahan data ringan hingga menengah",
                "logo_file": "excel.png",
                "initial": "X"
            },
            {
                "name": "Microsoft PowerPoint",
                "type": "Presentasi",
                "note": "Membuat slide presentasi dan materi visual",
                "logo_file": "powerpoint.png",
                "initial": "P"
            },
            {
                "name": "Google Chrome",
                "type": "Browser",
                "note": "Browsing, riset, akses website, dan aplikasi web",
                "logo_file": "chrome.png",
                "initial": "C"
            },
            {
                "name": "Zoom",
                "type": "Meeting Online",
                "note": "Kelas online, meeting, dan video conference",
                "logo_file": "zoom.png",
                "initial": "Z"
            },
            {
                "name": "Canva",
                "type": "Desain Ringan",
                "note": "Desain poster, presentasi, dan konten sederhana",
                "logo_file": "canva.png",
                "initial": "C"
            }
        ],

        "Editing": [
            {
                "name": "Adobe Premiere Pro",
                "type": "Video Editing",
                "note": "Editing video, timeline, color, dan export konten",
                "logo_file": "premiere-pro.png",
                "initial": "Pr"
            },
            {
                "name": "Adobe After Effects",
                "type": "Motion Graphic",
                "note": "Compositing, motion graphic, dan visual effect",
                "logo_file": "after-effects.png",
                "initial": "Ae"
            },
            {
                "name": "Adobe Photoshop",
                "type": "Image Editing",
                "note": "Editing foto, manipulasi gambar, dan desain visual",
                "logo_file": "photoshop.png",
                "initial": "Ps"
            },
            {
                "name": "DaVinci Resolve",
                "type": "Video Editing",
                "note": "Editing, color grading, audio, dan post-production",
                "logo_file": "davinci-resolve.png",
                "initial": "DR"
            },
            {
                "name": "Blender",
                "type": "3D Creation",
                "note": "Modeling, animasi 3D, rendering, dan visualisasi",
                "logo_file": "blender.png",
                "initial": "B"
            },
            {
                "name": "CapCut Desktop",
                "type": "Creator Editing",
                "note": "Editing video cepat untuk konten sosial media",
                "logo_file": "capcut.png",
                "initial": "CC"
            }
        ],

        "Gaming": [
            {
                "name": "VALORANT",
                "type": "FPS Kompetitif",
                "note": "Game tactical shooter kompetitif",
                "logo_file": "valorant.png",
                "initial": "V"
            },
            {
                "name": "Counter-Strike 2",
                "type": "FPS Kompetitif",
                "note": "Game FPS kompetitif berbasis aim dan strategi",
                "logo_file": "counter-strike-2.png",
                "initial": "CS"
            },
            {
                "name": "Dota 2",
                "type": "MOBA",
                "note": "Game MOBA kompetitif berbasis strategi tim",
                "logo_file": "dota-2.png",
                "initial": "D2"
            },
            {
                "name": "Apex Legends",
                "type": "Battle Royale",
                "note": "Game battle royale cepat dengan kemampuan karakter",
                "logo_file": "apex-legends.png",
                "initial": "A"
            },
            {
                "name": "Fortnite",
                "type": "Battle Royale",
                "note": "Game battle royale populer dengan mode kreatif",
                "logo_file": "fortnite.png",
                "initial": "F"
            },
            {
                "name": "HELLDIVERS 2",
                "type": "Co-op Shooter",
                "note": "Game co-op action shooter populer",
                "logo_file": "helldivers-2.png",
                "initial": "H2"
            }
        ],

        "All-Rounder": [
            {
                "name": "Adobe Premiere Pro",
                "type": "Editing",
                "note": "Editing video dan produksi konten",
                "logo_file": "premiere-pro.png",
                "initial": "Pr"
            },
            {
                "name": "Adobe After Effects",
                "type": "Motion Graphic",
                "note": "Motion graphic dan visual effect",
                "logo_file": "after-effects.png",
                "initial": "Ae"
            },
            {
                "name": "DaVinci Resolve",
                "type": "Post Production",
                "note": "Editing, color grading, dan audio post-production",
                "logo_file": "davinci-resolve.png",
                "initial": "DR"
            },
            {
                "name": "Blender",
                "type": "3D Creation",
                "note": "Modeling, animasi, dan rendering 3D",
                "logo_file": "blender.png",
                "initial": "B"
            },
            {
                "name": "VALORANT",
                "type": "Gaming",
                "note": "Game FPS kompetitif",
                "logo_file": "valorant.png",
                "initial": "V"
            },
            {
                "name": "Counter-Strike 2",
                "type": "Gaming",
                "note": "Game FPS kompetitif",
                "logo_file": "counter-strike-2.png",
                "initial": "CS"
            },
            {
                "name": "Apex Legends",
                "type": "Gaming",
                "note": "Game battle royale cepat",
                "logo_file": "apex-legends.png",
                "initial": "A"
            },
            {
                "name": "Fortnite",
                "type": "Gaming",
                "note": "Game battle royale dan creative mode",
                "logo_file": "fortnite.png",
                "initial": "F"
            }
        ]
    }

    return supported_apps.get(category, supported_apps["Daily Use"])


# ===== REFERENSI LAPTOP =====

def get_reference_laptops(category, top_n=5):
    data = catalog[catalog["usage_category"] == category].copy()

    if data.empty:
        return pd.DataFrame()

    data["price"] = pd.to_numeric(data["price"], errors="coerce")
    data = data.sort_values(by="price", ascending=True)

    columns = [
        "model_name",
        "brand",
        "processor_name",
        "ram(GB)",
        "ssd(GB)",
        "Hard Disk(GB)",
        "graphics",
        "price",
        "performance_score",
        "usage_category"
    ]

    result = data[columns].head(top_n).copy()
    result["price_formatted"] = result["price"].apply(format_price)

    return result


# ===== REKOMENDASI MARKETPLACE =====

def get_marketplace_recommendations(category, top_n=6, price_range=None):
    if marketplace_catalog.empty:
        return []

    data = marketplace_catalog.copy()

    required_columns = [
        "category",
        "price_range",
        "name",
        "brand",
        "cpu",
        "gpu",
        "ram",
        "storage",
        "price_idr",
        "marketplace",
        "product_url",
        "image_url",
        "image_file",
        "last_checked",
        "notes"
    ]

    for column in required_columns:
        if column not in data.columns:
            data[column] = ""

    data["category"] = data["category"].astype(str).str.strip()
    data["price_range"] = data["price_range"].astype(str).str.strip()

    data = data[data["category"].str.lower() == str(category).strip().lower()]

    if price_range:
        data = data[data["price_range"].str.lower() == str(price_range).strip().lower()]

    if data.empty:
        return []

    data["price_idr"] = pd.to_numeric(data["price_idr"], errors="coerce").fillna(0)

    price_range_order = {
        "Low Range": 1,
        "Mid Range": 2,
        "High Range": 3
    }

    data["price_range_order"] = data["price_range"].map(price_range_order).fillna(99)

    data = data.sort_values(
        by=["price_range_order", "price_idr"],
        ascending=[True, True]
    )

    result = data.head(top_n).copy()
    result["price_formatted"] = result["price_idr"].apply(format_price)

    recommendations = []

    for _, row in result.iterrows():
        image_file = str(row.get("image_file", "")).strip()
        image_url = str(row.get("image_url", "")).strip()

        price_value = row.get("price_idr", 0)
        try:
            price_value = int(price_value)
        except (TypeError, ValueError):
            price_value = 0

        recommendations.append({
            "category": str(row.get("category", "")).strip(),
            "price_range": str(row.get("price_range", "")).strip(),
            "name": str(row.get("name", "")).strip(),
            "brand": str(row.get("brand", "")).strip(),
            "cpu": str(row.get("cpu", "")).strip(),
            "gpu": str(row.get("gpu", "")).strip(),
            "ram": str(row.get("ram", "")).strip(),
            "storage": str(row.get("storage", "")).strip(),
            "price_idr": price_value,
            "price_formatted": str(row.get("price_formatted", "-")).strip(),
            "marketplace": str(row.get("marketplace", "")).strip(),
            "product_url": str(row.get("product_url", "")).strip(),
            "image_url": image_url,
            "image_file": image_file,
            "local_image_path": "img/laptops/" + image_file if image_file else "",
            "last_checked": str(row.get("last_checked", "")).strip(),
            "notes": str(row.get("notes", "")).strip()
        })

    return recommendations


# ===== REKOMENDASI MARKETPLACE PER KATEGORI =====

def get_all_marketplace_recommendations(top_n_each=6):
    categories = ["Daily Use", "Gaming", "Editing", "All-Rounder"]
    result = {}

    for category in categories:
        result[category] = get_marketplace_recommendations(
            category=category,
            top_n=top_n_each
        )

    return result


# ===== REFERENSI PER KATEGORI =====

def get_all_category_references(top_n_each=5):
    categories = ["Gaming", "Editing", "Daily Use", "All-Rounder"]
    result = {}

    for category in categories:
        result[category] = get_reference_laptops(category, top_n=top_n_each)

    return result


# ===== FUNGSI UTAMA EVALUASI LAPTOP =====

def evaluate_laptop(cpu_name, gpu_name, ram, storage, storage_type="SSD"):
    component_result = get_component_scores(
        cpu_name=cpu_name,
        gpu_name=gpu_name,
        ram=ram,
        storage_size=storage,
        storage_type=storage_type
    )

    cpu_s = component_result["cpu_score"]
    gpu_s = component_result["gpu_score"]
    ram_s = component_result["ram_score"]
    storage_s = component_result["storage_score"]
    component_details = component_result["details"]

    X_input = pd.DataFrame([{
        "cpu_score": cpu_s,
        "gpu_score": gpu_s,
        "ram_score": ram_s,
        "storage_score": storage_s
    }])

    prediction_encoded = model.predict(X_input)[0]
    model_predicted_category = label_encoder.inverse_transform([prediction_encoded])[0]

    probabilities = model.predict_proba(X_input)[0]

    xgboost_probability = {}
    for label, probability in zip(label_encoder.classes_, probabilities):
        xgboost_probability[label] = round(probability * 100, 2)

    category_scores = calculate_category_scores(
        cpu_s,
        gpu_s,
        ram_s,
        storage_s
    )

    formula_top_category = max(
        {k: v for k, v in category_scores.items() if k != "Performance"}.items(),
        key=lambda x: x[1]
    )[0]

    final_category = determine_final_category(
        model_category=model_predicted_category,
        cpu_score=cpu_s,
        gpu_score=gpu_s,
        ram_score=ram_s,
        storage_score=storage_s,
        gpu_name=gpu_name
    )

    confidence_info = calculate_result_confidence(
        final_category=final_category,
        category_scores=category_scores,
        cpu_score=cpu_s,
        gpu_score=gpu_s,
        ram_score=ram_s,
        storage_score=storage_s
    )

    explanation = generate_explanation(
        final_category,
        confidence_info,
        component_details
    )

    validation_note = (
        " Hasil akhir telah divalidasi menggunakan ambang minimum spesifikasi agar laptop "
        "berspesifikasi rendah tidak salah masuk ke kategori berat seperti Gaming, Editing, "
        "atau All-Rounder."
    )

    explanation += validation_note

    reference_laptops = get_reference_laptops(
        category=final_category,
        top_n=5
    )

    all_references = get_all_category_references(top_n_each=5)

    marketplace_recommendations = get_marketplace_recommendations(
        category=final_category,
        top_n=6
    )

    all_marketplace_recommendations = get_all_marketplace_recommendations(
        top_n_each=6
    )

    supported_apps = get_supported_apps(final_category)

    return {
        "cpu_score": cpu_s,
        "gpu_score": gpu_s,
        "ram_score": ram_s,
        "storage_score": storage_s,
        "component_details": component_details,
        "category_scores": category_scores,
        "xgboost_probability": xgboost_probability,
        "predicted_category": final_category,
        "model_predicted_category": model_predicted_category,
        "formula_top_category": formula_top_category,
        "confidence": confidence_info,
        "explanation": explanation,
        "supported_apps": supported_apps,

        "reference_laptops": reference_laptops,
        "all_references": all_references,

        "marketplace_recommendations": marketplace_recommendations,
        "all_marketplace_recommendations": all_marketplace_recommendations
    }


# ===== TEST VIA TERMINAL =====

if __name__ == "__main__":
    print("=== SISTEM EVALUASI SPESIFIKASI LAPTOP ===")
    print("Masukkan spesifikasi laptop yang ingin dicek.\n")

    cpu_input = input("Jenis CPU: ")
    gpu_input = input("Jenis GPU/VGA: ")
    ram_input = input("Ukuran RAM dalam GB: ")
    storage_input = input("Ukuran storage dalam GB: ")

    print("\nPilih jenis storage:")
    print("1. HDD")
    print("2. SATA SSD")
    print("3. NVMe SSD")

    storage_type_choice = input("Pilihan jenis storage: ")

    if storage_type_choice == "1":
        storage_type = "HDD"
    elif storage_type_choice == "2":
        storage_type = "SATA SSD"
    elif storage_type_choice == "3":
        storage_type = "NVMe SSD"
    else:
        storage_type = "SSD"

    result = evaluate_laptop(
        cpu_name=cpu_input,
        gpu_name=gpu_input,
        ram=ram_input,
        storage=storage_input,
        storage_type=storage_type
    )

    print("\n=== HASIL SKOR SPESIFIKASI ===")
    print("CPU Score:", result["cpu_score"])
    print("GPU Score:", result["gpu_score"])
    print("RAM Score:", result["ram_score"])
    print("Storage Score:", result["storage_score"])

    print("\n=== STATUS INPUT KOMPONEN ===")
    print("CPU:", result["component_details"]["cpu"]["message"])
    print("GPU:", result["component_details"]["gpu"]["message"])
    print("RAM:", result["component_details"]["ram"]["message"])
    print("Storage:", result["component_details"]["storage"]["message"])

    print("\n=== SKOR KATEGORI PENGGUNAAN ===")
    for category, score in result["category_scores"].items():
        print(category + ":", score)

    print("\n=== PROBABILITAS XGBOOST ===")
    for category, probability in result["xgboost_probability"].items():
        print(category + ":", str(probability) + "%")

    print("\n=== HASIL KLASIFIKASI ===")
    print("Kategori Penggunaan Laptop:", result["predicted_category"])
    print("Kategori XGBoost Awal:", result["model_predicted_category"])
    print("Kategori Tertinggi Formula:", result["formula_top_category"])

    print("\n=== KEJELASAN HASIL ===")
    print("Kejelasan:", result["confidence"]["confidence"])
    print("Selisih skor internal:", result["confidence"]["gap"])
    print("Catatan:", result["confidence"]["message"])

    print("\n=== PENJELASAN HASIL ===")
    print(result["explanation"])

    print("\n=== CONTOH APLIKASI / GAME SESUAI KATEGORI ===")
    for app in result["supported_apps"]:
        print(f"- {app['name']} ({app['type']}): {app['note']}")

    print("\n=== 5 REFERENSI LAPTOP LAMA DARI DATASET ===")
    reference_columns = [
        "model_name",
        "brand",
        "processor_name",
        "ram(GB)",
        "ssd(GB)",
        "Hard Disk(GB)",
        "graphics",
        "price_formatted",
        "performance_score",
        "usage_category"
    ]

    if result["reference_laptops"].empty:
        print("Tidak ada data referensi lama.")
    else:
        print(result["reference_laptops"][reference_columns].to_string(index=False))

    print("\n=== 6 REKOMENDASI LAPTOP MARKETPLACE ===")
    if not result["marketplace_recommendations"]:
        print("Tidak ada rekomendasi marketplace.")
    else:
        for laptop in result["marketplace_recommendations"]:
            print(
                f"- {laptop['name']} | {laptop['price_range']} | "
                f"{laptop['price_formatted']} | {laptop['marketplace']} | "
                f"{laptop['image_file']}"
            )