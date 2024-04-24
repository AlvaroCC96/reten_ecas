from django.urls import path
from . import views
from .views import login_with_microsoft


urlpatterns = [
    path('configuracion/', views.configuracion),
    path('home/', views.homeview),
    path('login/', views.custom_login),
    path('', views.login_view),
    path('login-with-microsoft/', login_with_microsoft, name='login_with_microsoft'),
]
