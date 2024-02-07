from django.urls import path
from . import views


urlpatterns = [
    path('ausencia/', views.ausencia),
]
