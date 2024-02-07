from django.urls import path
from . import views


urlpatterns = [
    path('modelos/', views.modelos),
    path('primer_anio/', views.primerAnio),
    path('carrera/', views.carrera),
    path('toma_ramos/', views.tomaRamos),
    path('asistencia_clases/', views.asistenciaClases),
    path('notas_parciales/', views.notasParciales),
    path('inasistencia_departamentales/', views.inasistenciaDepartamentales),
    path('notas_departamentales/', views.notasDepartamentales),
    path('rendimiento_previo/', views.rendimientoSemestrePrevio),
    path('inasistencia_controles/', views.inasistenciaControles),
]
