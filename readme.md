# Comparison of the kmeans method with random initialization with the kmeans++ method
This is a project to complete the subject "Przetwarzanie Informacji Wizyjnej" (eng. Vision Information Processing) at the Faculty of Automatics, Electronics, and Computer Science (AEiI) in Gliwice, at the Department of Automation and Robotics.

## Authors
- **Bartłomiej Murmyłowski**
- **Piotr Dinges**

## Purpose of the Project

The goal of this project was to compare two clustering methods: kmeans with random initialization and kmeans++ initialization. The comparison was conducted using the Kodak dataset containing 24 images ([source](https://www.kaggle.com/datasets/sherylmehta/kodak-dataset)). The methods were implemented and tested in Python with 8, 64, and 256 clusters. The metrics used for evaluation were:

- **Structural Similarity Index Measure (SSIM)**  
- **Mean Squared Error (MSE)**  
- **Execution time of the methods**  

## Computer used in the project
The project was carried out on a PC with the following specifications:
- **Processor**: Intel Core i9 9980XE @ 3.00GHz
- **RAM**: 64 GB 3600 MHz
- **Motherboard**: ASRock X299 Taichi (CPUSocket)
- **Graphics Card**: 4095MB NVIDIA GeForce RTX 2080 SUPER
- **Operating System**: Windows 10 Pro 64-bit

For managing background processes, the software **Process Lasso** was used.


## Project Structure

- **`dataset/`**: Contains the Kodak dataset images used for the project.  
- **`old/`**: Contains outdated and unused scripts.  
- **`result_data/`**: Results of the clustering, divided into:
  - Subfolders for each method (kmeans, kmeans++).
  - Within each method, subfolders for 8, 64, and 256 clusters.
  - Each subfolder contains JSON files with the results for each image.  
- **`result_img/`**: Processed images, divided similarly to `result_data/`, containing the images after applying clustering.  
- **`app.py`**: A Streamlit application that displays the statistics of the two methods. 
- **`main.py`**: Contains the core logic for testing both methods, generating processed images, and saving results as JSON files.


- **`requirements.txt`**: List of required Python libraries. Install them using:

    ```bash
        pip install -r requirements.txt
- **`report/`**: In this folder, there is a report (in both Polish and English) about this project and its details.
## Optional: Run the clustering script
While the results have already been generated, you can rerun the clustering process if needed:

    
        py main.py

The main.py script runs both the kmeans and kmeans++ methods, performs clustering on the images, and saves the results in the result_data/ and result_img/ folders. The results include both the images after applying clustering and the performance metrics (SSIM, MSE, and execution time) for each method and cluster configuration.

## View results in the app
To see the results in a more interactive way, you can use the Streamlit app, which provides a graphical view of the statistics and processed images for each clustering method:
Run it with the command:


    cd /path/to/project
    python -m streamlit run app.py

A new browser window will open with an interface where you can view the performance of both methods (kmeans and kmeans++) for 8, 64, and 256 clusters, including SSIM and MSE metrics as well as the execution time.


