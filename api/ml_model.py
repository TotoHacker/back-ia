# api/ml_model.py

import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from api.models import StudentInput
import os

MODEL_PATH_ADIC = "infrastructure/model_adiccion.pkl"
MODEL_PATH_SALUD = "infrastructure/model_salud.pkl"

def train_models():
    qs = StudentInput.objects.all().values()
    df = pd.DataFrame(qs)

    # Modelo de adicción
    df_adic = df.dropna(subset=['addicted_score'])
    X_adic = df_adic[["age", "avg_daily_usage_hours", "sleep_hours_per_night"]]
    y_adic = df_adic["addicted_score"]

    model_adic = LinearRegression()
    model_adic.fit(X_adic, y_adic)
    joblib.dump(model_adic, MODEL_PATH_ADIC)

    # Modelo de salud mental
    df_salud = df.dropna(subset=['mental_health_score'])
    X_salud = df_salud[["age", "avg_daily_usage_hours", "sleep_hours_per_night"]]
    y_salud = df_salud["mental_health_score"]

    model_salud = LinearRegression()
    model_salud.fit(X_salud, y_salud)
    joblib.dump(model_salud, MODEL_PATH_SALUD)

def predict_all(data: dict):
    if not os.path.exists(MODEL_PATH_ADIC) or not os.path.exists(MODEL_PATH_SALUD):
        train_models()

    model_adic = joblib.load(MODEL_PATH_ADIC)
    model_salud = joblib.load(MODEL_PATH_SALUD)

    df = pd.DataFrame([data])
    addicted_score = round(model_adic.predict(df)[0], 2)
    mental_health_score = round(model_salud.predict(df)[0], 2)

    return addicted_score, mental_health_score
