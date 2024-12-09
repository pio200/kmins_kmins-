import os
import cv2
import json
import numpy as np
from skimage import io
from skimage.metrics import structural_similarity as ssim
from sklearn.cluster import KMeans
import time  # Importowanie modułu do pomiaru czasu

dataset_path = r'dataset/'
result_img_path = r'result_img'
result_data_path = r'result_data'

k_values = [8, 64, 256]
methods = ['km', 'km++']
image_count = 24

# Funkcje pomocnicze
def calculate_mse(original, quantized):
    """Oblicza średni błąd kwadratowy (MSE) między dwoma obrazami."""
    return np.mean((original - quantized) ** 2)

def count_unique_colors(image):
    """
    Liczy liczbę unikalnych kolorów w obrazie.
    :param image: Obraz wejściowy jako numpy array.
    :return: Liczba unikalnych kolorów.
    """
    reshaped = image.reshape(-1, image.shape[-1])
    unique_colors = np.unique(reshaped, axis=0)
    return unique_colors.shape[0]

def quantize_image(image, k, method):
    """
    Kwantyzacja obrazu za pomocą K-średnich.
    :param image: Obraz wejściowy w postaci macierzy.
    :param k: Liczba klastrów.
    :param method: Metoda inicjalizacji ('km' lub 'km++').
    :return: Kwantyzowany obraz.
    """
    h, w, c = image.shape
    reshaped = image.reshape(-1, c)
    
    init = 'random' if method == 'km' else 'k-means++'
    kmeans = KMeans(n_clusters=k, init=init, random_state=42, max_iter=300)
    kmeans.fit(reshaped)
    
    quantized = kmeans.cluster_centers_[kmeans.labels_]
    return quantized.reshape(h, w, c).astype(np.uint8)

# Główna pętla
os.makedirs(result_img_path, exist_ok=True)
os.makedirs(result_data_path, exist_ok=True)

for i in range(1, image_count + 1):
    image_name = f"kodim{i:02d}.png"
    image_path = os.path.join(dataset_path, image_name)
    print(image_path)
    if not os.path.exists(image_path):
        print(f"Plik {image_name} nie istnieje, pomijam...")
        continue
    original = io.imread(image_path)
    original_unique_colors = count_unique_colors(original)
    
    for method in methods:
        for k in k_values:
            # Start pomiaru czasu
            start_time = time.time()

            # Kwantyzacja obrazu
            quantized_image = quantize_image(original, k, method)
            
            # Obliczanie metryk
            mse_value = calculate_mse(original, quantized_image)
            ssim_value = ssim(original, quantized_image, channel_axis=-1)
            quantized_unique_colors = count_unique_colors(quantized_image)

            # Koniec pomiaru czasu
            print("machen")
            end_time = time.time()
            processing_time = end_time - start_time  # Obliczenie czasu operacji
            
            # Zapisanie obrazu wynikowego
            method_img_path = os.path.join(result_img_path, method, str(k))
            os.makedirs(method_img_path, exist_ok=True)
            quantized_image_path = os.path.join(method_img_path, image_name)
            io.imsave(quantized_image_path, quantized_image)
            
            # Tworzenie danych wynikowych
            result = {
                'image_name': image_name,
                'method': method,
                'k': k,
                'SSIM': ssim_value,
                'MSE': mse_value,
                'original_unique_colors': original_unique_colors,
                'quantized_unique_colors': quantized_unique_colors,
                'processing_time': processing_time  # Dodanie czasu do danych
            }
            
            # Zapisanie danych w formacie JSON
            method_data_path = os.path.join(result_data_path, method, str(k))
            os.makedirs(method_data_path, exist_ok=True)
            metrics_json_path = os.path.join(method_data_path, f"{image_name}.json")
            with open(metrics_json_path, 'w') as f:
                json.dump(result, f, indent=4)
