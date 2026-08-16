import os
import pandas as pd
import joblib

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_sample_weight

# =========================
# LOAD DATASET TRAINING
# =========================

data = pd.read_csv("processed/model_training_dataset.csv")

os.makedirs("model", exist_ok=True)

print("=== DATASET TRAINING ===")
print("Jumlah data:", data.shape)
print("\nDistribusi kategori:")
print(data["usage_category"].value_counts())

# =========================
# FITUR DAN TARGET
# =========================
# Model hanya memakai skor spesifikasi, bukan nama laptop dan brand

feature_columns = [
    "cpu_score",
    "gpu_score",
    "ram_score",
    "storage_score"
]

X = data[feature_columns]
y = data["usage_category"]

# Encode label kategori menjadi angka
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print("\nLabel kategori:")
for index, label in enumerate(label_encoder.classes_):
    print(index, "=", label)

# =========================
# SPLIT DATA
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

# Mengatasi data yang tidak sepenuhnya seimbang
sample_weights = compute_sample_weight(
    class_weight="balanced",
    y=y_train
)

# =========================
# TRAINING MODEL XGBOOST
# =========================

model = XGBClassifier(
    objective="multi:softprob",
    num_class=len(label_encoder.classes_),
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="mlogloss",
    random_state=42
)

model.fit(
    X_train,
    y_train,
    sample_weight=sample_weights
)

# =========================
# EVALUASI MODEL
# =========================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(
    y_test,
    y_pred,
    target_names=label_encoder.classes_
)
cm = confusion_matrix(y_test, y_pred)

print("\n=== HASIL EVALUASI MODEL ===")
print("Akurasi:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(report)

print("\nConfusion Matrix:")
print(cm)

# =========================
# SIMPAN MODEL
# =========================

joblib.dump(model, "model/xgboost_laptop_model.pkl")
joblib.dump(label_encoder, "model/label_encoder.pkl")

# Simpan laporan evaluasi
with open("model/training_report.txt", "w", encoding="utf-8") as file:
    file.write("=== HASIL EVALUASI MODEL XGBOOST ===\n")
    file.write(f"Akurasi: {round(accuracy * 100, 2)}%\n\n")
    file.write("Classification Report:\n")
    file.write(report)
    file.write("\nConfusion Matrix:\n")
    file.write(str(cm))

print("\n=== MODEL BERHASIL DISIMPAN ===")
print("Model:", "model/xgboost_laptop_model.pkl")
print("Label encoder:", "model/label_encoder.pkl")
print("Report:", "model/training_report.txt")