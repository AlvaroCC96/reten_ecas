from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomLoginForm
import random
import string

def homeview(request):
    return render(request, 'home.html')

def configuracion(request):
    return render(request, 'configuracion.html')

def encuesta(request):
    return render(request, 'encuesta.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'login.html')
    

def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Redirigir a la página de inicio o a donde sea necesario
                return redirect('gestion')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

def login_with_microsoft(request):
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    client_id = 'e96ab2bc-cf81-43b9-a0b3-dc665b7b88c0'  # Reemplaza con tu client_id
    redirect_uri = 'http://127.0.0.1:8000/home/'  # Reemplaza con tu URL de redirección
    login_url = f'https://login.microsoftonline.com/adc11501-d885-4fea-a7ff-96723b15d25b/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=openid%20email%20profile&state={state}'
    return render(request, 'login_with_microsoft.html', {'login_url': login_url})
