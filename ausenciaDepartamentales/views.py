from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_protect
from datetime import datetime


def ausencia(request):
    asignaturas = None
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, cod_asig, cod_asig_des FROM tb_asignaturas")
        asignaturas = cursor.fetchall()
        
    alumnos = None
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, rut, nombres + ' ' + apellido_p + ' ' + apellido_m as nombre FROM tb_alumnos order by rut asc")
        alumnos = cursor.fetchall()
    
    
    data = {'asignaturas': asignaturas, 
            'alumnos' : alumnos}
    return render(request, 'ausencia.html',data)


@csrf_protect
def postAusencia(request):
    if request.method == 'POST':
        try:
            id_alumno = request.POST.get('id_alumno')
            fecha = request.POST.get('fecha')
            departamental = request.POST.get('departamental')
            codigos = request.POST.get('codigos').split(',')

            result = None
            for codigo in codigos:  
                with connection.cursor() as cursor:
                    query = """
                        SELECT id
                        from tb_ausencia_departamentales
                        where id_asignatura = %s and id_alumno = %s and fecha_ausencia = %s and departamental = %s
                    """
                    cursor.execute(query,( int(codigo), id_alumno, fecha, departamental))
                    result = cursor.fetchone()
            
                if result is not None:
                    return JsonResponse({'message': 'Error al guardar la información, la información ya fue ingresada anteriormente'}, status=500)
            
                with connection.cursor() as cursor:
                    query = "INSERT INTO [tb_ausencia_departamentales] ([id_asignatura], [id_alumno], [fecha_ausencia], [departamental], [created_at], [updated_at]) VALUES (%s, %s, %s, %s, GETDATE(), GETDATE())"
                    cursor.execute(query,( int(codigo), id_alumno, fecha, departamental))
                    
                connection.commit()
            
            return JsonResponse({'message': 'Registros guardados exitosamente'})
        except Exception as e:
            #print(e)
            return JsonResponse({'message': 'Error al guardar la información', 'error': e}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

@csrf_protect
def listadoAusencias(request):
    if request.method == 'POST':
        result = None
        with connection.cursor() as cursor:
            query = """
                select tad.fecha_ausencia, tb.nombres + ' ' + tb.apellido_p + ' ' + tb.apellido_m as nombre, ta.cod_asig, tad.departamental
                from tb_ausencia_departamentales tad
                left join tb_alumnos tb on tad.id_alumno = tb.id
                left join tb_asignaturas ta on tad.id_asignatura = ta.id
                order by tad.fecha_ausencia desc
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
        data = []
        if result is not None:
            for row in result:
                registro = {
                    'fecha':row[0],
                    'nombre':row[1],
                    'cod_asig':row[2],
                    'departamental':row[3],
                }
                data.append(registro)
        return JsonResponse({'data': data})
        
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)