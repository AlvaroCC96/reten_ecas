from django.urls import path
from . import views


urlpatterns = [
    path('usuarios_satra/', views.usuariosSatra),
    path('usuarios_satra/listadoUsuariosSatra/',views.listadoUsuariosSatra)
]
