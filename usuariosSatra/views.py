from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def usuariosSatra(request):
    return render(request, 'usuariosSatra.html')
