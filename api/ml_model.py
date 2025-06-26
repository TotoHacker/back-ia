import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
import numpy as np

MODEL_PATH = "infrastructure/model.pkl"

def train_model(csv_path='infrastructure/Data/students_social_media_cleaned.csv'):
    df = pd.read_csv(csv_path)

    # Verificamos que las columnas necesarias estén
    required_cols = [
        "age", "avg_daily_usage_hours", "sleep_hours_per_night", 
        "mental_health_score", "addicted_score"
    ]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Falta la columna requerida: {col}")
    
    # Si no hay performance_score, lo simulamos para pruebas
    if "performance_score" not in df.columns:
        df["performance_score"] = np.random.randint(60, 100, size=len(df))

    features = df[required_cols]
    target = df["performance_score"]

    model = RandomForestRegressor()
    model.fit(features, target)

    joblib.dump(model, MODEL_PATH)
    print("✅ Modelo entrenado y guardado en:", MODEL_PATH)
    return model

def predict_from_input(data_dict):
    model = joblib.load(MODEL_PATH)
    X = pd.DataFrame([data_dict])
    return model.predict(X)[0]
