from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
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

@csrf_protect
def listadoUsuariosSatra(request):
    if request.method == 'POST':
        result = None
        with connection.cursor() as cursor:
            query = """
                select id,usuario, persona, cargo, fecha_ini , fecha_fin , activo, fecha_ult, usuario_cre
                from tbr_usuarios
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
        data = []
        if result is not None:
            for row in result:
                registro = {
                    'id': row[0],
                    'usuario': row[1],
                    'persona': row[2],
                    'cargo': row[3],
                    'fecha_ini': row[4],
                    'fecha_fin': row[5],
                    'activo': row[6],
                    'fecha_ult': row[7],
                    'usuario_cre': row[8]
                }
                data.append(registro)
        return JsonResponse({'data': data})
        
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)   
