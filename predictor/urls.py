from django.urls import path
from .views import predictor_api

urlpatterns = [
    path('predictor/', predictor_api, name='predictor_api'),
]
