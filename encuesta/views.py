from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404


def homeEncuestas(request):
    return render(request, 'encuesta.html')

def entrevista(request):
    return render(request, 'entrevista.html')

def analisis_entrevista(request):
    return render(request, 'analisis.html')
