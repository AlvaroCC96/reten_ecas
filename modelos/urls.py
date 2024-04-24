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
    path('obtenerDatosTomaRamos/', views.obtenerDatosTomaRamos),
    path('insertarTomaRamos/',views.insertarTomaRamos),
    path('obtenerDatosAsistencia/', views.obtenerDatosAsistencia),
    path('insertarAsistenciaModelo/',views.insertarAsistenciaModelo),
    path('obtenerDatosNotasParciales/', views.obtenerDatosNotasParciales),
    path('insertarNotasParciales/',views.insertarNotasParciales),
    path('obtenerDatosInasistenciaDepartamentales/', views.obtenerDatosInasistenciaDepartamentales),
    path('insertarInasistenciaDepartamentales/',views.insertarInasistenciaDepartamentales),
    path('obtenerDatosNotasDepartamentales/', views.obtenerDatosNotasDepartamentales),
    path('insertarNotasDepartamentales/',views.insertarNotasDepartamentales),
    path('obtenerDatosRendimientoSemestrePrevio/', views.obtenerDatosRendimientoSemestrePrevio),
    path('insertarRendimientoSemestrePrevio/',views.insertarRendimientoSemestrePrevio),
    path('obtenerDatosInasistenciaControles/',views.obtenerDatosInasistenciaControles),
    path('insertarRendimientoSemestrePrevio/',views.insertarRendimientoSemestrePrevio),
]
