from django.shortcuts import render
from .models import StudentInput
import joblib
import numpy as np
def formulario_view(request):
    if request.method == 'POST':
        data = request.POST

        entrada = StudentInput.objects.create(
            student_id=data['student_id'],
            age=int(data['age']),
            gender=data['gender'],
            academic_level=data['academic_level'],
            country=data['country'],
            avg_daily_usage_hours=float(data['avg_daily_usage_hours']),
            most_used_platform=data['most_used_platform'],
            affects_academic_performance=(data['affects_academic_performance'] == "Yes"),
            sleep_hours_per_night=float(data['sleep_hours_per_night']),
            mental_health_score=int(data['mental_health_score']),
            relationship_status=data.get('relationship_status', ''),
            conflicts_over_social_media=(data.get('conflicts_over_social_media', '') == "Yes"),
            addicted_score=int(data['addicted_score']),
        )

        modelo = joblib.load('infrastructure/model.pkl')
        X = np.array([[
            entrada.age,
            entrada.avg_daily_usage_hours,
            entrada.sleep_hours_per_night,
            entrada.mental_health_score,
            entrada.addicted_score
        ]])
        prediccion = modelo.predict(X)[0]

        return render(request, 'index.html', {
            'prediction': prediccion,
            'input': entrada
        })

    return render(request, 'index.html')
