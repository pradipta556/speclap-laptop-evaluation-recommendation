import os
import sys

from flask import Flask, render_template, request, redirect, url_for

# Supaya file di dalam folder src bisa di-import
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from predict_recommendation import (
    evaluate_laptop,
    get_marketplace_recommendations,
    get_supported_apps
)

from scoring_utils import (
    CPU_OPTIONS,
    GPU_OPTIONS,
    RAM_OPTIONS,
    STORAGE_SIZE_OPTIONS,
    STORAGE_TYPE_OPTIONS
)

app = Flask(__name__)


# ============================================================
# HALAMAN UTAMA
# ============================================================

@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        cpu_options=CPU_OPTIONS,
        gpu_options=GPU_OPTIONS,
        ram_options=RAM_OPTIONS,
        storage_size_options=STORAGE_SIZE_OPTIONS,
        storage_type_options=STORAGE_TYPE_OPTIONS
    )


# ============================================================
# HALAMAN HASIL EVALUASI SPESIFIKASI LAPTOP
# ============================================================

@app.route("/result", methods=["POST"])
def result():
    try:
        cpu_name = request.form.get("cpu_name")
        gpu_name = request.form.get("gpu_name")
        ram = request.form.get("ram")
        storage = request.form.get("storage")
        storage_type = request.form.get("storage_type")

        if not cpu_name or not gpu_name or not ram or not storage or not storage_type:
            return render_template(
                "index.html",
                error="Semua input spesifikasi wajib diisi.",
                cpu_options=CPU_OPTIONS,
                gpu_options=GPU_OPTIONS,
                ram_options=RAM_OPTIONS,
                storage_size_options=STORAGE_SIZE_OPTIONS,
                storage_type_options=STORAGE_TYPE_OPTIONS
            )

        result_data = evaluate_laptop(
            cpu_name=cpu_name,
            gpu_name=gpu_name,
            ram=ram,
            storage=storage,
            storage_type=storage_type
        )

        reference_laptops = result_data["reference_laptops"].to_dict(orient="records")

        all_references = {}
        for category, dataframe in result_data["all_references"].items():
            all_references[category] = dataframe.to_dict(orient="records")

        return render_template(
            "result.html",
            cpu_name=cpu_name,
            gpu_name=gpu_name,
            ram=ram,
            storage=storage,
            storage_type=storage_type,
            result=result_data,
            reference_laptops=reference_laptops,
            all_references=all_references
        )

    except Exception as e:
        return render_template(
            "index.html",
            error=f"Terjadi kesalahan saat memproses data: {str(e)}",
            cpu_options=CPU_OPTIONS,
            gpu_options=GPU_OPTIONS,
            ram_options=RAM_OPTIONS,
            storage_size_options=STORAGE_SIZE_OPTIONS,
            storage_type_options=STORAGE_TYPE_OPTIONS
        )


# ============================================================
# HALAMAN REKOMENDASI LAPTOP BERDASARKAN KATEGORI
# ============================================================

CATEGORY_SLUG_MAP = {
    "daily-use": "Daily Use",
    "gaming": "Gaming",
    "editing": "Editing",
    "all-rounder": "All-Rounder"
}


@app.route("/recommendation/<category_slug>", methods=["GET"])
def recommendation(category_slug):
    category = CATEGORY_SLUG_MAP.get(category_slug)

    if category is None:
        return redirect(url_for("index"))

    recommendations = get_marketplace_recommendations(
        category=category,
        top_n=6
    )

    supported_apps = get_supported_apps(category)

    return render_template(
        "recommendation.html",
        category=category,
        category_slug=category_slug,
        recommendations=recommendations,
        supported_apps=supported_apps
    )


# ============================================================
# RUN FLASK APP
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)