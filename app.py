from flask import Flask, render_template, request
import os
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        df = pd.read_csv(filepath)
        df.fillna(df.mean(numeric_only=True), inplace=True)

        # PCA Processing
        features = df.select_dtypes(include=['float64', 'int64'])
        scaler = StandardScaler()
        scaled = scaler.fit_transform(features)

        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(scaled)
        explained_var = pca.explained_variance_ratio_

        # Plotting PCA result
        plt.figure(figsize=(6,5))
        plt.scatter(pca_result[:, 0], pca_result[:, 1], c='teal', s=40, alpha=0.7)
        plt.title('PCA Projection')
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.grid(True)
        plot_path = os.path.join('static', 'pca_plot.png')
        plt.savefig(plot_path)
        plt.close()

        return render_template('result.html',
                               explained_var=explained_var,
                               image_path=plot_path)

if __name__ == '__main__':
    app.run(debug=True)
