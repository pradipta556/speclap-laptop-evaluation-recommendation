import os
import pandas as pd

CSV_PATH = "processed/marketplace_catalog.csv"
IMAGE_FOLDER = "static/img/laptops"

df = pd.read_csv(CSV_PATH)

missing_files = []

for image_file in df["image_file"]:
    image_path = os.path.join(IMAGE_FOLDER, image_file)

    if not os.path.exists(image_path):
        missing_files.append(image_file)

print("=== CEK GAMBAR LAPTOP ===")
print(f"Total data CSV: {len(df)}")
print(f"Total gambar yang dicek: {len(df['image_file'])}")

if missing_files:
    print("\nGAMBAR YANG BELUM ADA / NAMA TIDAK SAMA:")
    for file in missing_files:
        print("-", file)
else:
    print("\nSemua gambar sudah lengkap dan nama file sudah sesuai.")