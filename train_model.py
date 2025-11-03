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

# 2️⃣ Correct column names from dataset
nutrition_cols = ['Calories (kcal)', 'Protein (g)', 'Carbohydrates (g)', 'Fats (g)']

# 3️⃣ Verify columns exist
for col in nutrition_cols:
    if col not in df.columns:
        print("⚠️ Column not found:", col)
print("✅ Columns verified!")

# 4️⃣ Select only the nutrition features
X = df[nutrition_cols]

# 5️⃣ Normalize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6️⃣ Apply K-Means Clustering (3 clusters → Weight Loss, Maintain, Muscle Gain)
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# 7️⃣ Label clusters meaningfully (based on average Calories/Protein)
cluster_summary = df.groupby('Cluster')[['Calories (kcal)', 'Protein (g)']].mean().sort_values(by='Calories (kcal)')
mapping = {cluster_summary.index[0]: 'Weight Loss',
           cluster_summary.index[1]: 'Maintain',
           cluster_summary.index[2]: 'Muscle Gain'}
df['Goal_Label'] = df['Cluster'].map(mapping)

# 8️⃣ Save model + scaler + clustered dataset
joblib.dump(scaler, "scaler.joblib")
joblib.dump(kmeans, "kmeans_model.joblib")
df.to_csv("Indian_Food_Clustered.csv", index=False)

print("✅ Model training complete!")
print("📁 Saved files: scaler.joblib, kmeans_model.joblib, Indian_Food_Clustered.csv")
print(df[['Dish Name', 'Calories (kcal)', 'Protein (g)', 'Goal_Label']].head(10))
