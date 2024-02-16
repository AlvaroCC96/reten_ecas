from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404


def usuariosSatra(request):
    return render(request, 'usuariosSatra.html')
