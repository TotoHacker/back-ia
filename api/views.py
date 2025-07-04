from django.shortcuts import render
from .models import StudentInput
from api.ml_model import predict_all
import numpy as np

def formulario_view(request):
    addicted_prediction = None
    mental_prediction = None
    error = None

    if request.method == 'POST':
        data = request.POST

        try:
            input_data = {
                "age": int(data['age']),
                "avg_daily_usage_hours": float(data['avg_daily_usage_hours']),
                "sleep_hours_per_night": float(data['sleep_hours_per_night']),
            }

            # Obtener predicciones
            addicted_prediction, mental_prediction = predict_all(input_data)

            # Guardar entrada junto con las predicciones
            entrada = StudentInput.objects.create(
                # student_id=int(data['student_id']),
                age=input_data['age'],
                gender=int(data['gender']),
                academic_level=int(data['academic_level']),
                country=int(data['country']),
                avg_daily_usage_hours=input_data['avg_daily_usage_hours'],
                most_used_platform=int(data['most_used_platform']),
                affects_academic_performance=(data['affects_academic_performance'] == "1"),
                sleep_hours_per_night=input_data['sleep_hours_per_night'],
                mental_health_score=int(round(mental_prediction)),
                relationship_status=int(data['relationship_status']),
                conflicts_over_social_media=(data['conflicts_over_social_media'] == "1"),
                addicted_score=int(round(addicted_prediction)),
            )

        except (KeyError, ValueError) as e:
            error = f"Error en los datos enviados: {str(e)}"

    return render(request, 'index.html', {
        'prediction_adic': addicted_prediction,
        'prediction_salud': mental_prediction,
        'error': error,
    })
