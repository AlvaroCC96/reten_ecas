from django.urls import path
from . import views


urlpatterns = [
    path('ausencia/', views.ausencia),
    path('postAusencia/', views.postAusencia),
    path('ausencia/listadoAusencias/', views.listadoAusencias)
]
