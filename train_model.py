# train_model.py
# ---------------------------------------
# Trains an AI model to cluster Indian foods
# based on nutrition values (Calories, Protein, Carbs, Fats)
# and saves the model for use in your Flask app.

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib

# 1️⃣ Load dataset
df = pd.read_csv("Indian_Food_Nutrition_Processed.csv")

# 2️⃣ Check essential columns (you can adjust names if slightly different)
nutrition_cols = ['Calories', 'Protein', 'Carbs', 'Fat']

for col in nutrition_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Column '{col}' not found in dataset. Please verify column names.")

# 3️⃣ Select only the nutrition features
X = df[nutrition_cols]

# 4️⃣ Normalize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5️⃣ Apply K-Means Clustering (3 clusters → weight loss, maintain, muscle gain)
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# 6️⃣ Label clusters meaningfully (based on average calories/protein)
cluster_summary = df.groupby('Cluster')[['Calories', 'Protein']].mean().sort_values(by='Calories')
mapping = {i: label for i, label in enumerate(['Weight Loss', 'Maintain', 'Muscle Gain'])}
df['Goal_Label'] = df['Cluster'].map(mapping)

# 7️⃣ Save model + scaler + clustered dataset
joblib.dump(scaler, "scaler.joblib")
joblib.dump(kmeans, "kmeans_model.joblib")
df.to_csv("Indian_Food_Clustered.csv", index=False)

print("✅ Model training complete!")
print("📁 Saved files: scaler.joblib, kmeans_model.joblib, Indian_Food_Clustered.csv")
print(df[['Calories', 'Protein', 'Goal_Label']].head(10))
