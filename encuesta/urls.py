from django.urls import path
from . import views


urlpatterns = [
    path('encuestas/', views.homeEncuestas),
    path('entrevista/', views.entrevista),
    path('analisis_entrevista/', views.analisis_entrevista),
]
