from django.urls import path
from . import views


urlpatterns = [
    path('encuestas/', views.homeEncuestas),
    path('entrevista/', views.entrevista),
    path('analisis_entrevista/', views.analisis_entrevista),
    path('postEntrevista/', views.postEntrevista),
    path('obtener_datos_grafico/<int:id_categoria>', views.obtenerDatosGrafico),
]
