from django.shortcuts import render
from api.ml_model import predict_all, train_models
from django.views.decorators.csrf import csrf_exempt
import os
import json

MODEL_PATH_ADIC = "infrastructure/model_adiccion.pkl"
MODEL_PATH_SALUD = "infrastructure/model_salud.pkl"

@csrf_exempt
def predictor_form(request):
    prediction_adic = None
    prediction_salud = None
    error = None

    if not os.path.exists(MODEL_PATH_ADIC) or not os.path.exists(MODEL_PATH_SALUD):
        train_models()  # Entrena ambos modelos

    if request.method == 'POST':
        try:
            data = {
                "age": int(request.POST["age"]),
                "avg_daily_usage_hours": float(request.POST["avg_daily_usage_hours"]),
                "sleep_hours_per_night": float(request.POST["sleep_hours_per_night"]),
            }
            prediction_adic, prediction_salud = predict_all(data)
        except Exception as e:
            error = f"Error: {str(e)}"

    return render(request, 'formulario.html', {
        "prediction_adic": prediction_adic,
        "prediction_salud": prediction_salud,
        "error": error,
        "prediction_json": json.dumps({
            "adiccion": prediction_adic,
            "salud": prediction_salud
        }) if prediction_adic is not None else None,
    })
