from django.urls import path
from .views import predictor_form

urlpatterns = [
    path('', predictor_form, name='formulario'),
]
