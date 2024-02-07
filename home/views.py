from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def configuracion(request):
    return render(request, 'configuracion.html')

def encuesta(request):
    return render(request, 'encuesta.html')
