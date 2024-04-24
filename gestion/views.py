from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.db import connection
from django import forms


class CitaForm(forms.Form):
    fecha_consulta = forms.DateField()
    hora_consulta_ini = forms.TimeField()
    hora_consulta_fin = forms.TimeField()
    id_alumno = forms.IntegerField()
    comentario = forms.CharField(max_length=255)
    motivo = forms.IntegerField()

def homeGestion(request):
    return render(request, 'gestion.html')

def getDatosNuevaCita(request, id_estudiante):
    query = """
        SELECT id, rut , nombres + ' ' + apellido_p + ' ' + apellido_m as nombre 
        FROM tb_alumnos
        WHERE id = %s;
    """
    resultado = None
    with connection.cursor() as cursor:
        cursor.execute(query,(id_estudiante,))
        resultado = cursor.fetchone()
    
    datos = {}
    id = None
    nombre = None
    if resultado:
        id = resultado[0]
        rut = resultado[1]
        nombre = resultado[2]
    
    if id is None:
        raise ValueError("No se encontró ningún estudiante con el ID proporcionado")
    
    query = """
        SELECT id, descripcion from tbr_motivos_citas;
    """
    motivos = []
    resultados = None
    with connection.cursor() as cursor:
        cursor.execute(query)
        resultados = cursor.fetchall()
    
    motivos = resultados
    
    datos = {
        'id': id,
        'nombre': nombre,
        'rut': rut,
        'motivos': motivos
    }
    
    return JsonResponse({'datos': datos})

@csrf_protect 
def postCita(request):
    if request.method == 'POST':
        try:
            form = CitaForm(request.POST)
            if form.is_valid():
                fecha_consulta = form.cleaned_data['fecha_consulta']
                hora_consulta_ini = form.cleaned_data['hora_consulta_ini']
                hora_consulta_fin = form.cleaned_data['hora_consulta_fin']
                id_alumno = form.cleaned_data['id_alumno']
                comentario = form.cleaned_data['comentario']
                motivo = form.cleaned_data['motivo']
                id_usuario = 1 #TODO
                
                if not isValidDates(id_usuario, fecha_consulta, hora_consulta_ini,hora_consulta_fin):
                    return JsonResponse({'message': 'Ya existe una cita en ese horario'}, status=400)
                
                with connection.cursor() as cursor:
                    query = """INSERT INTO [tbr_citas]
                    ([id_alumno]
                    ,[id_usuario]
                    ,[id_motivo]
                    ,[fecha_consulta]
                    ,[hora_inicio]
                    ,[hora_termino]
                    ,[comentario]
                    ,[estado_id]
                    ,[created_at]
                    ,[updated_at]
                    )     
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, GETDATE(), GETDATE())"""
                    cursor.execute(query,( id_alumno,id_usuario, motivo,fecha_consulta,hora_consulta_ini,hora_consulta_fin,comentario,1))
                connection.commit()
                
                id_cita = None
                with connection.cursor() as cursor:
                    query = """
                    SELECT TOP 1 id
                    FROM tbr_citas
                    WHERE id_usuario = %s
                    ORDER BY id DESC
                    """
                    cursor.execute(query,(id_usuario,))
                    id_cita = cursor.fetchone()[0]
                
                return JsonResponse({'message': 'Registros guardados exitosamente', 'id': id_cita})
            else:
                # El formulario no es válido, devolver errores de validación
                errors = form.errors.as_json()
                return JsonResponse({'message': 'Error en los datos del formulario', 'errors': errors}, status=400)
        except Exception as e:
            error_message = str(e)
            return JsonResponse({'message': 'Error al guardar la información', 'error': e}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

def isValidDates(id_usuario, fecha_consulta, hora_consulta_ini, hora_consulta_fin):
    result = None
    with connection.cursor() as cursor:
        query = """
            SELECT 1 AS existe
            FROM tbr_citas 
            WHERE
                id_usuario = %s AND
                fecha_consulta = %s AND
                (
                    (hora_inicio >= %s AND hora_inicio < %s) OR  -- La nueva cita comienza dentro de la cita existente
                    (hora_termino > %s AND hora_termino <= %s) OR  -- La nueva cita termina dentro de la cita existente
                    (hora_inicio <= %s AND hora_termino >= %s)  -- La nueva cita cubre completamente la cita existente
                )
                and deleted_at is null
        """
        cursor.execute(query, (id_usuario, fecha_consulta, hora_consulta_ini, hora_consulta_fin, hora_consulta_ini, hora_consulta_fin, hora_consulta_ini, hora_consulta_fin))
        result = cursor.fetchone()
    return result == None

def getListadoCitas(request):
    if request.method == "GET":
        try:
            citas_info = []
            id_usuario = 1 #TODO
            with connection.cursor() as cursor:
                query = """
                    select 
                    c.id, 
                    rut , 
                    nombres + ' ' + apellido_p + ' ' + apellido_m as nombre,
                    fecha_consulta,
                    hora_inicio,
                    hora_termino
                    from tbr_citas c
                    left join tb_alumnos a on c.id_alumno = a.id
                    where id_usuario = %s
                    and c.deleted_at is null
                """
                cursor.execute(query, (id_usuario,))
                for row in cursor.fetchall():
                    cita_info = {
                        'id': row[0],
                        'rut': row[1],
                        'nombre': row[2],
                        'fecha_consulta': row[3],
                        'hora_inicio': row[4],
                        'hora_termino': row[5],
                    }
                    citas_info.append(cita_info)
            return JsonResponse({'citas': citas_info})
        except Exception as e:
            return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

def getDatoEditarCita(request, id_cita):
    
    query = """
        SELECT 
        c.id,  
        nombres + ' ' + apellido_p + ' ' + apellido_m as nombre,
        rut,
        c.fecha_consulta,
        c.hora_inicio,
        c.hora_termino,
        c.comentario,
        c.id_motivo,
        c.estado_id
        from tbr_citas c
        left join tb_alumnos a on c.id_alumno = a.id
        left join tbr_estado_citas ec on c.estado_id = ec.id
        where c.id = %s;
    """
    resultado = None
    with connection.cursor() as cursor:
        cursor.execute(query,(id_cita,))
        resultado = cursor.fetchone()
    
    datos = {}
    id = None
    nombre = None
    if resultado:
        id = resultado[0]
        nombre = resultado[1]
        rut = resultado[2]
        fecha_consulta = resultado[3]
        hora_inicio = resultado[4]
        hora_termino = resultado[5]
        comentario = resultado[6]
        id_motivo = resultado[7]
        estado_id = resultado[8]
        
    if id is None:
        raise ValueError("No se encontró ningún estudiante con el ID proporcionado")
    
    query = """
        SELECT id, descripcion from tbr_motivos_citas;
    """
    motivos = []
    resultados = None
    with connection.cursor() as cursor:
        cursor.execute(query)
        resultados = cursor.fetchall()
    
    motivos = resultados
    
    datos = {
        'id': id,
        'nombre': nombre,
        'rut': rut,
        'fecha_consulta': fecha_consulta,
        'hora_inicio': hora_inicio,
        'hora_termino': hora_termino,
        'comentario': comentario,
        'id_motivo': id_motivo,
        'motivos': motivos,
        'estado_id': estado_id
    }
    
    return JsonResponse({'datos': datos})

@csrf_protect 
def postEditarCita(request):
    if request.method == 'POST':
        try:
            result = None
            id_cita = request.POST.get('id_cita')
            with connection.cursor() as cursor:
                query = """
                SELECT * FROM tbr_citas
                WHERE id = %s
                """
                cursor.execute(query,(id_cita,))
                result = cursor.fetchone()
                
            if result:
                id_motivo = request.POST.get('motivo')
                comentario = request.POST.get('texto_comentario')
                with connection.cursor() as cursor:
                    query = """
                    UPDATE tbr_citas
                    SET id_motivo = %s, comentario = %s
                    WHERE id = %s;
                    """
                    cursor.execute(query,(id_motivo,comentario,id_cita,))
                return JsonResponse({'message': 'Registro actualizado exitosamente'})
            else:
                return JsonResponse({'message': 'Cita no encontrada'}, status=401)
        except Exception as e:
            error_message = str(e)
            return JsonResponse({'message': 'Error al guardar la información', 'error': e}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    

@csrf_protect 
def postEliminarCita(request):
    if request.method == 'POST':
        try:
            result = None
            id_cita = request.POST.get('id_cita')
            with connection.cursor() as cursor:
                query = """
                SELECT * FROM tbr_citas
                WHERE id = %s
                """
                cursor.execute(query,(id_cita,))
                result = cursor.fetchone()
                
            if result:
                with connection.cursor() as cursor:
                    query = """
                    UPDATE tbr_citas
                    SET deleted_at = GETDATE(), estado_id = 3
                    WHERE id = %s;
                    """
                    cursor.execute(query,(id_cita,))
                return JsonResponse({'message': 'Registro eliminado exitosamente'})
            else:
                return JsonResponse({'message': 'Cita no encontrada'}, status=401)
        except Exception as e:
            error_message = str(e)
            return JsonResponse({'message': 'Error al guardar la información', 'error': e}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
@csrf_protect 
def postTerminarCita(request):
    if request.method == 'POST':
        try:
            result = None
            id_cita = request.POST.get('id_cita')
            with connection.cursor() as cursor:
                query = """
                SELECT * FROM tbr_citas
                WHERE id = %s
                """
                cursor.execute(query,(id_cita,))
                result = cursor.fetchone()
                
            if result:
                with connection.cursor() as cursor:
                    query = """
                    UPDATE tbr_citas
                    SET estado_id = 2
                    WHERE id = %s;
                    """
                    cursor.execute(query,(id_cita,))
                return JsonResponse({'message': 'Cita terminada exitosamente'})
            else:
                return JsonResponse({'message': 'Cita no encontrada'}, status=401)
        except Exception as e:
            error_message = str(e)
            return JsonResponse({'message': 'Error al guardar la información', 'error': e}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)