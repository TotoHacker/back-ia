from django.contrib import admin
from django.urls import path,include  
from api.views import formulario_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', formulario_view, name='formulario'),
    path('', include('predictor.urls')),
]
