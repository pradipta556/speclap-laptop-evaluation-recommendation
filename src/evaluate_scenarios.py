"""Menjalankan empat skenario hold-out XGBoost tanpa menimpa model utama.

Jalankan dari folder utama proyek:
    python src/evaluate_scenarios.py

Output disimpan ke:
    results/scenario_evaluation/
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_sample_weight
from xgboost import XGBClassifier


# Lokasi proyek dihitung dari posisi file ini: <project>/src/evaluate_scenarios.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "processed" / "model_training_dataset.csv"
OUTPUT_DIR = PROJECT_ROOT / "results" / "scenario_evaluation"

FEATURE_COLUMNS = [
    "cpu_score",
    "gpu_score",
    "ram_score",
    "storage_score",
]
TARGET_COLUMN = "usage_category"
RANDOM_STATE = 42

# Nama skenario dan proporsi data uji.
SCENARIOS = {
    "90_10": 0.10,
    "80_20": 0.20,
    "70_30": 0.30,
    "60_40": 0.40,
}


def build_model(number_of_classes: int) -> XGBClassifier:
    """Membentuk model dengan hyperparameter yang sama seperti model utama."""
    return XGBClassifier(
        objective="multi:softprob",
        num_class=number_of_classes,
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="mlogloss",
        random_state=RANDOM_STATE,
    )


def main() -> None:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan: {DATASET_PATH}\n"
            "Pastikan perintah dijalankan dari proyek Skripsi-laptop yang lengkap."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(DATASET_PATH)
    missing_columns = [
        column
        for column in FEATURE_COLUMNS + [TARGET_COLUMN]
        if column not in data.columns
    ]
    if missing_columns:
        raise ValueError(
            "Kolom berikut tidak ditemukan pada dataset: "
            + ", ".join(missing_columns)
        )

    X = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMN]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    class_names = list(label_encoder.classes_)
    class_labels = list(range(len(class_names)))

    summary_rows = []
    combined_text_report = [
        "HASIL EMPAT SKENARIO PENGUJIAN XGBOOST",
        f"Jumlah dataset: {len(data)}",
        f"Fitur: {', '.join(FEATURE_COLUMNS)}",
        f"Kelas: {', '.join(class_names)}",
        f"Random state: {RANDOM_STATE}",
        "=" * 72,
    ]

    for scenario_name, test_size in SCENARIOS.items():
        train_ratio = int(round((1 - test_size) * 100))
        test_ratio = int(round(test_size * 100))
        display_name = f"{train_ratio}:{test_ratio}"

        print(f"\nMenjalankan skenario {display_name} ...")

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y_encoded,
            test_size=test_size,
            random_state=RANDOM_STATE,
            stratify=y_encoded,
        )

        sample_weights = compute_sample_weight(
            class_weight="balanced",
            y=y_train,
        )

        model = build_model(number_of_classes=len(class_names))
        model.fit(X_train, y_train, sample_weight=sample_weights)
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        macro_precision, macro_recall, macro_f1, _ = (
            precision_recall_fscore_support(
                y_test,
                y_pred,
                average="macro",
                zero_division=0,
            )
        )
        weighted_precision, weighted_recall, weighted_f1, _ = (
            precision_recall_fscore_support(
                y_test,
                y_pred,
                average="weighted",
                zero_division=0,
            )
        )

        report_dict = classification_report(
            y_test,
            y_pred,
            labels=class_labels,
            target_names=class_names,
            output_dict=True,
            zero_division=0,
        )
        report_text = classification_report(
            y_test,
            y_pred,
            labels=class_labels,
            target_names=class_names,
            zero_division=0,
        )

        # Simpan classification report tiap skenario sebagai CSV.
        report_dataframe = pd.DataFrame(report_dict).transpose()
        report_dataframe.to_csv(
            OUTPUT_DIR / f"classification_report_{scenario_name}.csv",
            index=True,
        )

        # Simpan confusion matrix tiap skenario sebagai PNG.
        figure, axis = plt.subplots(figsize=(8, 6))
        ConfusionMatrixDisplay.from_predictions(
            y_test,
            y_pred,
            labels=class_labels,
            display_labels=class_names,
            cmap="Blues",
            colorbar=False,
            values_format="d",
            ax=axis,
        )
        axis.set_title(f"Confusion Matrix XGBoost - Skenario {display_name}")
        figure.tight_layout()
        figure.savefig(
            OUTPUT_DIR / f"confusion_matrix_{scenario_name}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.close(figure)

        summary_rows.append(
            {
                "skenario": display_name,
                "jumlah_dataset": len(data),
                "jumlah_data_latih": len(X_train),
                "jumlah_data_uji": len(X_test),
                "accuracy": accuracy,
                "macro_precision": macro_precision,
                "macro_recall": macro_recall,
                "macro_f1_score": macro_f1,
                "weighted_precision": weighted_precision,
                "weighted_recall": weighted_recall,
                "weighted_f1_score": weighted_f1,
            }
        )

        combined_text_report.extend(
            [
                "",
                f"SKENARIO {display_name}",
                f"Data latih: {len(X_train)}",
                f"Data uji: {len(X_test)}",
                f"Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)",
                f"Macro precision: {macro_precision:.4f}",
                f"Macro recall: {macro_recall:.4f}",
                f"Macro F1-score: {macro_f1:.4f}",
                "",
                "Classification Report:",
                report_text,
                "-" * 72,
            ]
        )

        print(
            f"Selesai: data latih={len(X_train)}, "
            f"data uji={len(X_test)}, accuracy={accuracy * 100:.2f}%"
        )

    summary_dataframe = pd.DataFrame(summary_rows)
    summary_dataframe.to_csv(
        OUTPUT_DIR / "summary_scenarios.csv",
        index=False,
    )

    with open(
        OUTPUT_DIR / "report_all_scenarios.txt",
        "w",
        encoding="utf-8",
    ) as report_file:
        report_file.write("\n".join(combined_text_report))

    print("\nSemua skenario selesai.")
    print(f"Hasil tersimpan di: {OUTPUT_DIR}")
    print("File utama: summary_scenarios.csv dan report_all_scenarios.txt")


if __name__ == "__main__":
    main()
