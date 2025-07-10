from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import StudentInput
from api.ml_model import predict_all
import json

# --- Funciones de mapeo ---
def map_gender(genero):
    return 1 if genero == "Masculino" else 0

def map_academic_level(nivel):
    niveles = {
        "High School": 0,
        "Undergraduate": 1,
        "Graduate": 2
    }
    return niveles.get(nivel, -1)

def map_country(pais):
    paises = {
        "Argentina": 0, "Bolivia": 1, "Brasil": 2, "Chile": 3, "Colombia": 4,
        "Costa Rica": 5, "Cuba": 6, "Ecuador": 7, "El Salvador": 8, "España": 9,
        "Estados Unidos": 10, "Guatemala": 11, "Honduras": 12, "México": 13,
        "Nicaragua": 14, "Panamá": 15, "Paraguay": 16, "Perú": 17, "Puerto Rico": 18,
        "República Dominicana": 19, "Uruguay": 20, "Venezuela": 21
    }
    return paises.get(pais, -1)

def map_platform(platform):
    plataformas = {
        "Facebook": 0,
        "TikTok": 1,
        "YouTube": 2
    }
    return plataformas.get(platform, -1)

def map_relationship_status(estado):
    estados = {
        "Soltero(a)": 0,
        "En una relación": 1,
        "Es complicado": 2
    }
    return estados.get(estado, -1)

def generar_recomendaciones(data, preds):
    recomendaciones = []

    if preds[0] > 7:
        recomendaciones.append("Considera reducir significativamente el tiempo en redes sociales")
    if data['usoDialioHoras'] > 6:
        recomendaciones.append("Establece límites de tiempo diario para redes sociales")
    if data['horasSuenoPorNoche'] < 7:
        recomendaciones.append("Mejora tus hábitos de sueño evitando pantallas antes de dormir")
    if data['conflictosPorRedesSociales'] == "Sí":
        recomendaciones.append("Practica el uso consciente de redes sociales")
    if data['afectaRendimientoAcademico'] == "Sí":
        recomendaciones.append("Crea espacios libres de distracciones digitales para estudiar")

    if not recomendaciones:
        recomendaciones.append("Mantén tus buenos hábitos digitales actuales")

    return recomendaciones

# --- Vista principal ---
@csrf_exempt
def formulario_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # datos requeridos para la predicción
            input_data = {
                "age": int(data['edad']),
                "avg_daily_usage_hours": float(data['usoDialioHoras']),
                "sleep_hours_per_night": float(data['horasSuenoPorNoche']),
            }

            preds = predict_all(input_data)
            if len(preds) != 8:
                return JsonResponse({"error": "predict_all debe devolver 8 predicciones"}, status=500)

            # Guardar en base de datos
            StudentInput.objects.create(
                age=input_data['age'],
                gender=map_gender(data['genero']),
                academic_level=map_academic_level(data['nivelAcademico']),
                country=map_country(data['pais']),
                avg_daily_usage_hours=input_data['avg_daily_usage_hours'],
                most_used_platform=map_platform(data['plataformaMasUsada']),
                affects_academic_performance=(data['afectaRendimientoAcademico'] == "Sí"),
                sleep_hours_per_night=input_data['sleep_hours_per_night'],
                mental_health_score=int(round(preds[1])),
                relationship_status=map_relationship_status(data['estadoSentimental']),
                conflicts_over_social_media=(data['conflictosPorRedesSociales'] == "Sí"),
                addicted_score=int(round(preds[0]))
                # Puedes agregar aquí los otros 6 si están en el modelo
            )

            # Devolver todas las predicciones
            response = {
                "nivelAdiccion": round(preds[0], 1),
                "saludMental": round(preds[1], 1),
                "impactoAcademico": "Alto" if data['afectaRendimientoAcademico'] == "Sí" else (
                    "Medio" if input_data['avg_daily_usage_hours'] > 6 else "Bajo"
                ),
                "plataformaDominante": data['plataformaMasUsada'],
                "recomendaciones": generar_recomendaciones(data, preds),
                "predictions": {
                    "pred1": preds[0],
                    "pred2": preds[1],
                    "pred3": preds[2],
                    "pred4": preds[3],
                    "pred5": preds[4],
                    "pred6": preds[5],
                    "pred7": preds[6],
                    "pred8": preds[7]
                }
            }

            return JsonResponse(response)

        except KeyError as ke:
            return JsonResponse({"error": f"Falta el campo: {str(ke)}"}, status=400)
        except ValueError as ve:
            return JsonResponse({"error": f"Error en el formato de dato: {str(ve)}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido, usa POST"}, status=405)
