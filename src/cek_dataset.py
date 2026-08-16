import pandas as pd

laptop = pd.read_csv("dataset/laptop.csv")
cpu = pd.read_csv("dataset/CPU_benchmark_v4.csv")
gpu = pd.read_csv("dataset/GPU_benchmarks_v7.csv")

print("=== DATASET LAPTOP ===")
print("Jumlah baris dan kolom:", laptop.shape)
print("Nama kolom:")
print(laptop.columns)
print(laptop.head())

print("\n=== DATASET CPU ===")
print("Jumlah baris dan kolom:", cpu.shape)
print("Nama kolom:")
print(cpu.columns)
print(cpu.head())

print("\n=== DATASET GPU ===")
print("Jumlah baris dan kolom:", gpu.shape)
print("Nama kolom:")
print(gpu.columns)
print(gpu.head())