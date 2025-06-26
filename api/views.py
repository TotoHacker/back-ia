from django.shortcuts import render
from .models import StudentInput
import joblib
import numpy as np

from django.shortcuts import render
from .models import StudentInput
import joblib
import numpy as np

def formulario_view(request):
    if request.method == 'POST':
        data = request.POST
        
        # Convertir inputs numéricos adecuadamente
        age = int(data['age'])
        avg_daily_usage_hours = float(data['avg_daily_usage_hours'])
        sleep_hours_per_night = float(data['sleep_hours_per_night'])
        mental_health_score = int(data['mental_health_score'])
        addicted_score = int(data['addicted_score'])

        # Guardar en BD
        entrada = StudentInput.objects.create(
            student_id=data['student_id'],
            age=age,
            gender=data['gender'],
            academic_level=data['academic_level'],
            country=data['country'],
            avg_daily_usage_hours=avg_daily_usage_hours,
            most_used_platform=data['most_used_platform'],
            affects_academic_performance=(data['affects_academic_performance'] == 'Yes'),
            sleep_hours_per_night=sleep_hours_per_night,
            mental_health_score=mental_health_score,
            relationship_status=data['relationship_status'],
            conflicts_over_social_media=(data.get('conflicts_over_social_media') == 'Yes'),
            addicted_score=addicted_score,
        )

        # Cargar modelo
        modelo = joblib.load('infrastructure/modelo_entrenado.pkl')

        # Ejemplo: Generar 5 predicciones variando ligeramente un parámetro (por ejemplo uso diario)
        base_features = np.array([
            age,
            avg_daily_usage_hours,
            sleep_hours_per_night,
            mental_health_score,
            addicted_score
        ])

        predicciones = []
        for delta in [-1, 0, 1, 2, 3]:
            features = base_features.copy()
            features[1] = max(0, features[1] + delta)  # modifica avg_daily_usage_hours variando ± delta
            pred = modelo.predict(features.reshape(1, -1))[0]
            predicciones.append(round(pred, 2))

        return render(request, 'index.html', {
            'predicciones': predicciones,
            'input': entrada
        })

    return render(request, 'index.html')
