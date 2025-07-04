import xml.etree.ElementTree as ET
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

MODEL_PATH = "infrastructure/model.pkl"

def leer_xml(ruta_xml):
    tree = ET.parse(ruta_xml)
    root = tree.getroot()

    rows = []
    for alumno in root.findall("alumno"):
        try:
            fila = {
                "age": int(alumno.findtext("age")),
                "avg_daily_usage_hours": float(alumno.findtext("avg_daily_usage_hours")),
                "sleep_hours_per_night": float(alumno.findtext("sleep_hours_per_night")),
                "mental_health_score": float(alumno.findtext("mental_health_score")),
                "addicted_score": float(alumno.findtext("addicted_score")),
            }
            rows.append(fila)
        except Exception as e:
            print(f"Error leyendo alumno: {e}")

    df = pd.DataFrame(rows)
    return df

def train_model_from_xml():
    ruta = r"infrastructure\Data\students_social_media_cleaned.xml"
    df = leer_xml(ruta)

    features = ["age", "avg_daily_usage_hours", "sleep_hours_per_night", "mental_health_score"]
    target = "addicted_score"

    X = df[features]
    y = df[target]

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print("Modelo entrenado y guardado.")

def predict_from_input(data: dict):
    model = joblib.load(MODEL_PATH)
    FEATURES = ["age", "avg_daily_usage_hours", "sleep_hours_per_night", "mental_health_score"]
    filtered_data = {k: data[k] for k in FEATURES}
    df = pd.DataFrame([filtered_data])
    prediction = model.predict(df)[0]
    return round(prediction, 2)
