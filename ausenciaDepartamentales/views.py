from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def ausencia(request):
    return render(request, 'ausencia.html')
