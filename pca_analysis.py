# pca_analysis.py

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pickle

# Load dataset
df = pd.read_csv('survey_data/mental_health_survey.csv')

# Select only numeric features
features = ['Sleep_Hours', 'Screen_Time_Hrs', 'Stress_Level', 'Junk_Food_Freq',
            'Exercise_Days', 'Social_Hours', 'Mood_Score']
X = df[features]

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Save PCA model and scaler
with open('pca_model.pkl', 'wb') as f:
    pickle.dump((pca, scaler), f)

# Save the PCA results (for visualization/testing)
df['PCA1'] = X_pca[:, 0]
df['PCA2'] = X_pca[:, 1]
df.to_csv('survey_data/pca_output.csv', index=False)

print("PCA model saved as pca_model.pkl")
