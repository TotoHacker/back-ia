from django.shortcuts import render
from api.ml_model import predict_from_input, train_model
from django.views.decorators.csrf import csrf_exempt
import os

MODEL_PATH = "infrastructure/modelo_entrenado.pkl"

@csrf_exempt
def predictor_form(request):
    prediction = None
    
    # Verificar si el modelo existe, si no, entrenar y guardarlo
    if not os.path.exists(MODEL_PATH):
        train_model()  # Entrena y guarda el modelo en la ruta MODEL_PATH

    if request.method == 'POST':
        data = {
            "age": int(request.POST["age"]),
            "avg_daily_usage_hours": float(request.POST["avg_daily_usage_hours"]),
            "sleep_hours_per_night": float(request.POST["sleep_hours_per_night"]),
            "mental_health_score": int(request.POST["mental_health_score"]),
            "addicted_score": int(request.POST["addicted_score"]),
        }
        prediction = predict_from_input(data)

    return render(request, 'formulario.html', {
        "prediction": prediction
    })
