from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("login/", admin.site.urls),
    path('pacientes/', views.listar_pacientes, name='listar_pacientes'),
]

