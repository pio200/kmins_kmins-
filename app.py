import os
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time

# Funkcja do wczytywania danych z plików JSON
def load_metrics(result_data_path):
    data = []
    for method in os.listdir(result_data_path):
        method_path = os.path.join(result_data_path, method)
        for k in os.listdir(method_path):
            k_path = os.path.join(method_path, k)
            for file_name in os.listdir(k_path):
                file_path = os.path.join(k_path, file_name)
                with open(file_path, 'r') as f:
                    data.append(json.load(f))
    return pd.DataFrame(data)

# Ścieżka do danych wynikowych
result_data_path = "result_data"

# Wczytaj dane
st.title("Analiza Kwantyzacji Obrazów")
if os.path.exists(result_data_path):
    st.sidebar.header("Opcje filtrowania")

    # Wczytywanie danych
    metrics_df = load_metrics(result_data_path)

    # Filtry
    k_values = metrics_df['k'].unique()
    selected_k = st.sidebar.selectbox("Wybierz wartość k:", sorted(k_values))

    image_names = sorted(metrics_df['image_name'].unique())
    selected_range = st.sidebar.slider(
        "Zakres obrazów:", 1, len(image_names), (1, len(image_names))
    )
    start_image, end_image = selected_range

    compare_methods = st.sidebar.radio("Porównanie metod:", ["Obie", "Tylko k-means", "Tylko k-means++"])

    chart_type = st.sidebar.radio("Wybierz typ wykresu:", ["Słupkowy", "Liniowy"])

    # Filtrowanie danych
    filtered_df = metrics_df[(metrics_df['k'] == selected_k)]
    filtered_df = filtered_df[filtered_df['image_name'].isin(image_names[start_image - 1:end_image])]

    if compare_methods == "Tylko k-means":
        filtered_df = filtered_df[filtered_df['method'] == 'km']
    elif compare_methods == "Tylko k-means++":
        filtered_df = filtered_df[filtered_df['method'] == 'km++']

    # Sumowanie czasu przetwarzania dla metod
    method_times = filtered_df.groupby('method')['processing_time'].sum()

    # Wykres SSIM
    st.header("Wykres SSIM dla poszczególnych obrazów")
    plt.figure(figsize=(14, 8))
    for method in filtered_df['method'].unique():
        subset = filtered_df[filtered_df['method'] == method]
        if chart_type == "Słupkowy":
            plt.bar(subset['image_name'], subset['SSIM'], label=method)
        else:
            plt.plot(subset['image_name'], subset['SSIM'], marker='o', label=method)
    plt.title(f"SSIM dla obrazów przy k = {selected_k}", fontsize=16)
    plt.xlabel("Obraz", fontsize=14)
    plt.ylabel("SSIM", fontsize=14)
    plt.xticks(rotation=45)
    plt.legend(fontsize=12)
    st.pyplot(plt)

    # Wykres MSE
    st.header("Wykres MSE dla poszczególnych obrazów")
    plt.figure(figsize=(14, 8))
    for method in filtered_df['method'].unique():
        subset = filtered_df[filtered_df['method'] == method]
        if chart_type == "Słupkowy":
            plt.bar(subset['image_name'], subset['MSE'], label=method)
        else:
            plt.plot(subset['image_name'], subset['MSE'], marker='o', label=method)
    plt.title(f"MSE dla obrazów przy k = {selected_k}", fontsize=16)
    plt.xlabel("Obraz", fontsize=14)
    plt.ylabel("MSE", fontsize=14)
    plt.xticks(rotation=45)
    plt.legend(fontsize=12)
    st.pyplot(plt)

    # Wykres czasu przetwarzania
    st.header("Wykres czasu przetwarzania dla poszczególnych obrazów")
    plt.figure(figsize=(14, 8))
    for method in filtered_df['method'].unique():
        subset = filtered_df[filtered_df['method'] == method]
        if chart_type == "Słupkowy":
            plt.bar(subset['image_name'], subset['processing_time'], label=method)
        else:
            plt.plot(subset['image_name'], subset['processing_time'], marker='o', label=method)
    plt.title(f"Czas przetwarzania dla obrazów przy k = {selected_k}", fontsize=16)
    plt.xlabel("Obraz", fontsize=14)
    plt.ylabel("Czas przetwarzania [s]", fontsize=14)
    plt.xticks(rotation=45)
    plt.legend(fontsize=12)
    st.pyplot(plt)

    # Wyświetlenie czasów
    st.sidebar.header("Sumaryczny czas przetwarzania metod")
    for method, total_time in method_times.items():
        st.sidebar.write(f"{method}: {total_time:.2f} sekundy")

else:
    st.error("Nie znaleziono folderu 'result_data'. Upewnij się, że ścieżka jest poprawna.")