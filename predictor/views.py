from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import StudentInput
from api.ml_model import predict_all, train_models_from_csv
import os
import json

# Rutas de los 8 modelos que usas
MODEL_PATHS = [
    "infrastructure/model1.pkl",
    "infrastructure/model2.pkl",
    "infrastructure/model3.pkl",
    "infrastructure/model4.pkl",
    "infrastructure/model5.pkl",
    "infrastructure/model6.pkl",
    "infrastructure/model7.pkl",
    "infrastructure/model8.pkl",
]

@csrf_exempt
def predictor_api(request):
    # Entrenar modelos si no existen
    if not all(os.path.exists(path) for path in MODEL_PATHS):
        ()

    if request.method == 'POST':
        try:
            # Leer JSON del body
            data = json.loads(request.body)

            # Extraer y validar datos de entrada
            input_data = {
                "age": int(data['age']),
                "avg_daily_usage_hours": float(data['avg_daily_usage_hours']),
                "sleep_hours_per_night": float(data['sleep_hours_per_night']),
                # agrega aquí más features si tu modelo las requiere
            }

            # Obtener las 8 predicciones (tu función debe devolverlas)
            preds = predict_all(input_data)  # ej: (p1, p2, p3, ..., p8)

            # Guardar en base de datos
            StudentInput.objects.create(
                age=input_data['age'],
                gender=int(data['gender']),
                academic_level=int(data['academic_level']),
                country=int(data['country']),
                avg_daily_usage_hours=input_data['avg_daily_usage_hours'],
                most_used_platform=int(data['most_used_platform']),
                affects_academic_performance=(data['affects_academic_performance'] == "1"),
                sleep_hours_per_night=input_data['sleep_hours_per_night'],
                mental_health_score=int(round(preds[1])),  # ejemplo pred2
                relationship_status=int(data['relationship_status']),
                conflicts_over_social_media=(data['conflicts_over_social_media'] == "1"),
                addicted_score=int(round(preds[0])),  # ejemplo pred1
                # si quieres guardar más predicciones, agrega campos en el modelo y aquí
            )

            # Respuesta JSON con las 8 predicciones
            return JsonResponse({
                "status": "ok",
                "predictions": {
                    "pred1": preds[0],
                    "pred2": preds[1],
                    "pred3": preds[2],
                    "pred4": preds[3],
                    "pred5": preds[4],
                    "pred6": preds[5],
                    "pred7": preds[6],
                    "pred8": preds[7],
                }
            })

        except KeyError as ke:
            return JsonResponse({"error": f"Falta el campo: {str(ke)}"}, status=400)
        except ValueError as ve:
            return JsonResponse({"error": f"Error en formato de dato: {str(ve)}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido, usa POST"}, status=405)
