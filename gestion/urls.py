from django.urls import path
from . import views


urlpatterns = [
    path('gestion/', views.homeGestion),
    path('obtenerDatosNuevaCita/<int:id_estudiante>', views.getDatosNuevaCita),
    path('postCita/', views.postCita),
    path('postEditarCita/', views.postEditarCita),
    path('postEliminarCita/',views.postEliminarCita),
    path('postTerminarCita/',views.postTerminarCita),
    path('getListadoCitas/', views.getListadoCitas),
    path('obtenerDatosEditarCita/<int:id_cita>', views.getDatoEditarCita),
]
