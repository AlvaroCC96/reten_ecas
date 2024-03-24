from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db import connection

def usuariosSatra(request):
    modulos = None
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, titulo_modulo FROM tbr_modulos")
        modulos = cursor.fetchall()
    
    usuarios = None
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tbr_usuarios")
        usuarios = cursor.fetchall()
    
    data = {
        'modulos': modulos,
        'usuarios': usuarios
    }
    return render(request, 'usuariosSatra.html' , data)
