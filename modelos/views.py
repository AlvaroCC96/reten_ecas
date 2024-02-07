from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def modelos(request):
    return render(request, 'index.html')

def primerAnio(request):
    return render(request, 'primer_anio.html')

def carrera(request):
    return render(request, 'carrera.html')

def tomaRamos(request):
    return render(request, 'toma_ramos.html')

def asistenciaClases(request):
    return render(request, 'asistencia_clases.html')

def inasistenciaDepartamentales(request):
    return render(request, 'inasistencia_departamentales.html')

def notasDepartamentales(request):
    return render(request, 'notas_departamentales.html')

def notasParciales(request):
    return render(request, 'notas_parciales.html')

def rendimientoSemestrePrevio(request):
    return render(request, 'rendimiento_semestre_previo.html')

def inasistenciaControles(request):
    return render(request, 'inasistencia_controles.html')
