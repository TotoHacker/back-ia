import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
import os

MODEL_PATHS = [
    "infrastructure/model_1.pkl",
    "infrastructure/model_2.pkl",
    "infrastructure/model_3.pkl",
    "infrastructure/model_4.pkl",
    "infrastructure/model_5.pkl",
    "infrastructure/model_6.pkl",
    "infrastructure/model_7.pkl",
    "infrastructure/model_8.pkl",
]

CSV_PATH = "infrastructure/Data/1_IDYGS93_cleaned.csv"

def train_models_from_csv():
    df = pd.read_csv(CSV_PATH)

    features = ["age", "avg_daily_usage_hours", "sleep_hours_per_night"]
    targets = [
        "mental_health_score",
        "relationship_status",
        "conflicts_over_social_media",
        "addicted_score",
        "gender",
        "academic_level",
        "country",
        "most_used_platform",
    ]

    for i, target in enumerate(targets):
        if target not in df.columns:
            print(f"Columna {target} no existe en CSV, saltando...")
            continue

        df_target = df.dropna(subset=[target])
        if df_target.empty:
            print(f"No hay datos para {target}, saltando...")
            continue

        X = df_target[features]
        y = df_target[target]

        model = LinearRegression()
        model.fit(X, y)
        joblib.dump(model, MODEL_PATHS[i])
        print(f"Modelo {i+1} entrenado para {target}")

def predict_all(data: dict):
    if any(not os.path.exists(p) for p in MODEL_PATHS):
        train_models_from_csv()

    df = pd.DataFrame([data])
    preds = []
    for path in MODEL_PATHS:
        model = joblib.load(path)
        preds.append(round(model.predict(df)[0], 2))

    return tuple(preds)
