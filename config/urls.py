from django.contrib import admin
from django.urls import path,include  
from api.views import formulario_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('formulario/', formulario_view),  # esta es la ruta de tu POST
    path('', include('predictor.urls')),
]
