from django.urls import path
from . import views


urlpatterns = [
    path('modelos/', views.modelos),
    path('primer_anio/', views.primerAnio),
    path('carrera/', views.carrera),
]
