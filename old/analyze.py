import os
import json
import pandas as pd
import matplotlib.pyplot as plt

result_data_path = r'result_data'

# Funkcja do wczytania danych z plików JSON
def load_results(base_path):
    results = []
    for method in os.listdir(base_path):
        method_path = os.path.join(base_path, method)
        for k_value in os.listdir(method_path):
            k_path = os.path.join(method_path, k_value)
            for json_file in os.listdir(k_path):
                json_path = os.path.join(k_path, json_file)
                with open(json_path, 'r') as f:
                    data = json.load(f)
                    results.append(data)
    return pd.DataFrame(results)

# Wczytanie danych do DataFrame
df = load_results(result_data_path)

# Przykładowa analiza danych
# 1. Porównanie SSIM dla różnych metod i wartości k
plt.figure(figsize=(10, 6))
for method in df['method'].unique():
    subset = df[df['method'] == method]
    plt.plot(subset['k'], subset['SSIM'], marker='o', label=method)
plt.xlabel('Liczba klastrów (k)')
plt.ylabel('SSIM')
plt.title('Porównanie SSIM dla różnych metod i wartości k')
plt.legend()
plt.grid(True)
plt.show()

# 2. MSE dla różnych metod
plt.figure(figsize=(10, 6))
for method in df['method'].unique():
    subset = df[df['method'] == method]
    plt.plot(subset['k'], subset['MSE'], marker='o', label=method)
plt.xlabel('Liczba klastrów (k)')
plt.ylabel('MSE')
plt.title('Porównanie MSE dla różnych metod i wartości k')
plt.legend()
plt.grid(True)
plt.show()

# 3. Liczba unikalnych kolorów po kwantyzacji
plt.figure(figsize=(10, 6))
for method in df['method'].unique():
    subset = df[df['method'] == method]
    plt.plot(subset['k'], subset['quantized_unique_colors'], marker='o', label=method)
plt.xlabel('Liczba klastrów (k)')
plt.ylabel('Liczba unikalnych kolorów po kwantyzacji')
plt.title('Porównanie liczby unikalnych kolorów dla różnych metod i wartości k')
plt.legend()
plt.grid(True)
plt.show()

# 4. Porównanie SSIM w zależności od liczby unikalnych kolorów
plt.figure(figsize=(10, 6))
plt.scatter(df['quantized_unique_colors'], df['SSIM'], c='blue', label='SSIM', alpha=0.7)
plt.xlabel('Liczba unikalnych kolorów po kwantyzacji')
plt.ylabel('SSIM')
plt.title('SSIM w zależności od liczby unikalnych kolorów')
plt.grid(True)
plt.show()
