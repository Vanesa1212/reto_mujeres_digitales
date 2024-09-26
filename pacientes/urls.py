from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from .views import listar_pacientes  # Asegúrate de importar la función correctamente


urlpatterns = [
    path('pacientes/', listar_pacientes, name='listar_pacientes'),
]

