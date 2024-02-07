from django.urls import path
from . import views


urlpatterns = [
    path('usuarios_satra/', views.usuariosSatra),
]
