from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def modelos(request):
    return render(request, 'index.html')

def primerAnio(request):
    return render(request, 'primer_anio.html')

def carrera(request):
    return render(request, 'carrera.html')
