from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_protect


def modelos(request):
    return render(request, 'index.html')

def primerAnio(request):
    return render(request, 'primer_anio.html')

def carrera(request):
    return render(request, 'carrera.html')

def tomaRamos(request):
    try:
        data = []
        with connection.cursor() as cursor:
            query = """
                select AÑO,SEMESTRE,CRITERIO=nom_criterio,
                DIAS_PREVIOS=x,DESCRIP_A=des_x,DIAS_ALARMA=y,
                DESCRIP_B=des_y,FECHA_INI,FECHA_FIN,ACTIVO=case 
                when activo=1 then 'SI' else 'NO' end,FECHA_ULTIMA=fecha_ult,USUARIO_ULTIMO=usuario_ult
                from tbr_data_criterios a, tbr_criterios b 
                where a.id=b.id and a.id=1 ORDER BY año,semestre,activo,fecha_ini,fecha_fin 
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                data_info = {
                    'anio': row[0],
                    'SEMESTRE': row[1],
                    'CRITERIO': row[2],
                    'DIAS_PREVIOS': int(row[3]),
                    'DESCRIP_A': row[4],
                    'DIAS_ALARMA': int(row[5]),
                    'DESCRIP_B': row[6],
                    'FECHA_INI': row[7],
                    'FECHA_FIN': row[8],
                    'ACTIVO': row[9],
                    'FECHA_ULTIMA': datetime.strftime(row[10], '%Y-%m-%d'),
                    'USUARIO_ULTIMO': row[11]
                }
                data.append(data_info)
            data_render = {
                'data': data
            }
        return render(request, 'mantenedor_toma_ramos.html', data_render)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)

def obtenerDatosTomaRamos(request):
    try:
        data = {}
        with connection.cursor() as cursor:
            query = """
                select id, nombre_campo, texto from tbr_texto_modulos
                where nombre_campo in ('descripcion_dias_previos_toma_ramos', 'descripcion_dias_alarma_toma_ramos') 
            """
            cursor.execute(query)
            for row in cursor.fetchall():

                data_info = {
                    'id': row[0],
                    'nombre_campo': row[1],
                    'texto': row[2]
                }
                data[row[1]] = data_info
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)
    
@csrf_protect
def insertarTomaRamos(request):
    if request.method == 'POST':
        try:
            anio = request.POST.get('anio')
            semestre = request.POST.get('semestre')
            dias_previo = request.POST.get('dias_previos')
            dias_alarma = request.POST.get('dias_alarma')
            fecha_inicial = request.POST.get('fecha_inicial')
            fecha_fin = request.POST.get('fecha_fin')
            activo = request.POST.get('activo')
            
            user_id = 1 # TODO cambiar
            
            result = None
            with connection.cursor() as cursor:
                query = """
                    select id, usuario 
                    from tbr_usuarios 
                    where id = %s
                """
                cursor.execute(query,(user_id,))
                result = cursor.fetchone()
            if result is None:
                return JsonResponse({'message': 'Usuario no encontrado'}, status=500)
            
            usuario = result[1]
            data = {}
            with connection.cursor() as cursor:
                query = """
                    select id, nombre_campo, texto from tbr_texto_modulos
                    where nombre_campo in ('descripcion_dias_previos_toma_ramos', 'descripcion_dias_alarma_toma_ramos') 
                """
                cursor.execute(query)
                for row in cursor.fetchall():

                    data_info = {
                        'id': row[0],
                        'nombre_campo': row[1],
                        'texto': row[2]
                    }
                    data[row[1]] = data_info
            
            des_x = data['descripcion_dias_previos_toma_ramos']['texto']
            des_y = data['descripcion_dias_alarma_toma_ramos']['texto']
            data_insert =(anio,semestre,dias_previo,des_x,dias_alarma,des_y,fecha_inicial,fecha_fin,activo,usuario,)
            
            #return JsonResponse({'data': data_insert})
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO [tbr_data_criterios]
                    (
                        [id], -- Aquí está el campo [id]
                        [año],
                        [semestre],
                        [x],
                        [des_x],
                        [y],
                        [des_y],
                        [fecha_ini],
                        [fecha_fin],
                        [activo],
                        [fecha_ult],
                        [usuario_ult]
                    )
                    VALUES
                    (
                        1, -- Valor 1 para el campo [id]
                        %s, -- año
                        %s, -- semestre
                        %s, -- x
                        %s, -- des_x
                        %s, -- y
                        %s, -- des_y
                        %s, -- fecha_ini
                        %s, -- fecha_fin
                        %s, -- activo
                        GETDATE(), -- fecha_ult
                        %s -- usuario_ult
                    )
                """
                cursor.execute(query,data_insert)
            connection.commit()
            return JsonResponse({'message': 'Registros guardados exitosamente'})
        except Exception as e:
            return JsonResponse({'message': 'Error al guardar la información', 'error': e}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

def asistenciaClases(request):
    try:
        data = []
        with connection.cursor() as cursor:
            query = """
                select AÑO,SEMESTRE,CRITERIO=nom_criterio,
                DIAS_PREVIOS=x,DESCRIP_A=des_x,DIAS_ALARMA=y,
                DESCRIP_B=des_y,FECHA_INI,FECHA_FIN,ACTIVO=case 
                when activo=1 then 'SI' else 'NO' end,FECHA_ULTIMA=fecha_ult,USUARIO_ULTIMO=usuario_ult
                from tbr_data_criterios a, tbr_criterios b 
                where a.id=b.id and a.id=2 ORDER BY año,semestre,activo,fecha_ini,fecha_fin 
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                data_info = {
                    'anio': row[0],
                    'SEMESTRE': row[1],
                    'CRITERIO': row[2],
                    'DIAS_PREVIOS': int(row[3]),
                    'DESCRIP_A': row[4],
                    'DIAS_ALARMA': int(row[5]),
                    'DESCRIP_B': row[6],
                    'FECHA_INI': row[7],
                    'FECHA_FIN': row[8],
                    'ACTIVO': row[9],
                    'FECHA_ULTIMA': datetime.strftime(row[10], '%Y-%m-%d'),
                    'USUARIO_ULTIMO': row[11]
                }
                data.append(data_info)
            data_render = {
                'data': data
            }
        return render(request, 'mantenedor_asistencia.html', data_render)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)

def obtenerDatosAsistencia(request):
    try:
        data = {}
        with connection.cursor() as cursor:
            query = """
                select id, nombre_campo, texto from tbr_texto_modulos
                where nombre_campo in ('descripcion_dias_previos_asistencia_clases', 'descripcion_dias_alarma_asistencia_clases') 
            """
            cursor.execute(query)
            for row in cursor.fetchall():

                data_info = {
                    'id': row[0],
                    'nombre_campo': row[1],
                    'texto': row[2]
                }
                data[row[1]] = data_info
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)

@csrf_protect
def insertarAsistenciaModelo(request):
    if request.method == 'POST':
        try:
            anio = request.POST.get('anio')
            semestre = request.POST.get('semestre')
            dias_previo = request.POST.get('dias_previos')
            dias_alarma = request.POST.get('dias_alarma')
            fecha_inicial = request.POST.get('fecha_inicial')
            fecha_fin = request.POST.get('fecha_fin')
            activo = request.POST.get('activo')
            
            user_id = 1 # TODO cambiar
            
            result = None
            with connection.cursor() as cursor:
                query = """
                    select id, usuario 
                    from tbr_usuarios 
                    where id = %s
                """
                cursor.execute(query,(user_id,))
                result = cursor.fetchone()
            if result is None:
                return JsonResponse({'message': 'Usuario no encontrado'}, status=500)
            
            usuario = result[1]
            data = {}
            with connection.cursor() as cursor:
                query = """
                    select id, nombre_campo, texto from tbr_texto_modulos
                    where nombre_campo in ('descripcion_dias_previos_asistencia_clases', 'descripcion_dias_alarma_asistencia_clases') 
                """
                cursor.execute(query)
                for row in cursor.fetchall():

                    data_info = {
                        'id': row[0],
                        'nombre_campo': row[1],
                        'texto': row[2]
                    }
                    data[row[1]] = data_info
            
            des_x = data['descripcion_dias_previos_asistencia_clases']['texto']
            des_y = data['descripcion_dias_alarma_asistencia_clases']['texto']
            data_insert =(anio,semestre,dias_previo,des_x,dias_alarma,des_y,fecha_inicial,fecha_fin,activo,usuario,)
            
            #return JsonResponse({'data': data_insert})
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO [tbr_data_criterios]
                    (
                        [id], -- Aquí está el campo [id]
                        [año],
                        [semestre],
                        [x],
                        [des_x],
                        [y],
                        [des_y],
                        [fecha_ini],
                        [fecha_fin],
                        [activo],
                        [fecha_ult],
                        [usuario_ult]
                    )
                    VALUES
                    (
                        2, -- Valor 1 para el campo [id]
                        %s, -- año
                        %s, -- semestre
                        %s, -- x
                        %s, -- des_x
                        %s, -- y
                        %s, -- des_y
                        %s, -- fecha_ini
                        %s, -- fecha_fin
                        %s, -- activo
                        GETDATE(), -- fecha_ult
                        %s -- usuario_ult
                    )
                """
                cursor.execute(query,data_insert)
            connection.commit()
            return JsonResponse({'message': 'Registros guardados exitosamente'})
        except Exception as e:
            return JsonResponse({'message': 'Error al guardar la información', 'error': e}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

def notasParciales(request):
    try:
        data = []
        with connection.cursor() as cursor:
            query = """
                select AÑO,SEMESTRE,CRITERIO=nom_criterio,
                CANTIDAD_CONTROLES=x,DESCRIP_A=des_x,PROMEDIO=y,
                DESCRIP_B=des_y,FECHA_INI,FECHA_FIN,ACTIVO=case 
                when activo=1 then 'SI' else 'NO' end,FECHA_ULTIMA=fecha_ult,USUARIO_ULTIMO=usuario_ult
                from tbr_data_criterios a, tbr_criterios b 
                where a.id=b.id and a.id=3 ORDER BY año,semestre,activo,fecha_ini,fecha_fin 
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                data_info = {
                    'anio': row[0],
                    'SEMESTRE': row[1],
                    'CRITERIO': row[2],
                    'CANTIDAD_CONTROLES': int(row[3]),
                    'DESCRIP_A': row[4],
                    'PROMEDIO': int(row[5]),
                    'DESCRIP_B': row[6],
                    'FECHA_INI': row[7],
                    'FECHA_FIN': row[8],
                    'ACTIVO': row[9],
                    'FECHA_ULTIMA': datetime.strftime(row[10], '%Y-%m-%d'),
                    'USUARIO_ULTIMO': row[11]
                }
                data.append(data_info)
            data_render = {
                'data': data
            }
        return render(request, 'mantenedor_notas_parciales.html', data_render)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)

def obtenerDatosNotasParciales(request):
    try:
        data = {}
        with connection.cursor() as cursor:
            query = """
                select id, nombre_campo, texto from tbr_texto_modulos
                where nombre_campo in ('descripcion_cantidad_controles_notas_parciales', 'descripcion_promedio_notas_parciales') 
            """
            cursor.execute(query)
            for row in cursor.fetchall():

                data_info = {
                    'id': row[0],
                    'nombre_campo': row[1],
                    'texto': row[2]
                }
                data[row[1]] = data_info
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)

@csrf_protect
def insertarNotasParciales(request):
    if request.method == 'POST':
        try:
            anio = request.POST.get('anio')
            semestre = request.POST.get('semestre')
            cantidad_controles = request.POST.get('cantidad_controles')
            promedio = request.POST.get('promedio')
            fecha_inicial = request.POST.get('fecha_inicial')
            fecha_fin = request.POST.get('fecha_fin')
            activo = request.POST.get('activo')
            
            user_id = 1 # TODO cambiar
            
            result = None
            with connection.cursor() as cursor:
                query = """
                    select id, usuario 
                    from tbr_usuarios 
                    where id = %s
                """
                cursor.execute(query,(user_id,))
                result = cursor.fetchone()
            if result is None:
                return JsonResponse({'message': 'Usuario no encontrado'}, status=500)
            
            usuario = result[1]
            data = {}
            with connection.cursor() as cursor:
                query = """
                    select id, nombre_campo, texto from tbr_texto_modulos
                    where nombre_campo in ('descripcion_cantidad_controles_notas_parciales', 'descripcion_promedio_notas_parciales') 
                """
                cursor.execute(query)
                for row in cursor.fetchall():

                    data_info = {
                        'id': row[0],
                        'nombre_campo': row[1],
                        'texto': row[2]
                    }
                    data[row[1]] = data_info
            
            des_x = data['descripcion_cantidad_controles_notas_parciales']['texto']
            des_y = data['descripcion_promedio_notas_parciales']['texto']
            data_insert =(anio,semestre,cantidad_controles,des_x,promedio,des_y,fecha_inicial,fecha_fin,activo,usuario,)
            
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO [tbr_data_criterios]
                    (
                        [id], -- Aquí está el campo [id]
                        [año],
                        [semestre],
                        [x],
                        [des_x],
                        [y],
                        [des_y],
                        [fecha_ini],
                        [fecha_fin],
                        [activo],
                        [fecha_ult],
                        [usuario_ult]
                    )
                    VALUES
                    (
                        3, -- Valor 1 para el campo [id]
                        %s, -- año
                        %s, -- semestre
                        %s, -- x
                        %s, -- des_x
                        %s, -- y
                        %s, -- des_y
                        %s, -- fecha_ini
                        %s, -- fecha_fin
                        %s, -- activo
                        GETDATE(), -- fecha_ult
                        %s -- usuario_ult
                    )
                """
                cursor.execute(query,data_insert)
            connection.commit()
            return JsonResponse({'message': 'Registros guardados exitosamente'})
        except Exception as e:
            return JsonResponse({'message': 'Error al guardar la información', 'error': e}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)


def inasistenciaDepartamentales(request):
    try:
        data = []
        with connection.cursor() as cursor:
            query = """
                select AÑO,SEMESTRE,CRITERIO=nom_criterio,
                AUSENCIA_DEP_1=x,DESCRIP_A=des_x,AUSENCIA_DEP_2=y,
                DESCRIP_B=des_y,FECHA_INI,FECHA_FIN,ACTIVO=case 
                when activo=1 then 'SI' else 'NO' end,FECHA_ULTIMA=fecha_ult,USUARIO_ULTIMO=usuario_ult
                from tbr_data_criterios a, tbr_criterios b 
                where a.id=b.id and a.id=4 ORDER BY año,semestre,activo,fecha_ini,fecha_fin 
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                data_info = {
                    'anio': row[0],
                    'SEMESTRE': row[1],
                    'CRITERIO': row[2],
                    'AUSENCIA_DEP_1': int(row[3]),
                    'DESCRIP_A': row[4],
                    'PROMEDIO': int(row[5]),
                    'DESCRIP_B': row[6],
                    'FECHA_INI': row[7],
                    'FECHA_FIN': row[8],
                    'ACTIVO': row[9],
                    'FECHA_ULTIMA': datetime.strftime(row[10], '%Y-%m-%d'),
                    'USUARIO_ULTIMO': row[11]
                }
                data.append(data_info)
            data_render = {
                'data': data
            }
        return render(request, 'mantenedor_inasistencia_departamentales.html',data_render)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)

def obtenerDatosInasistenciaDepartamentales(request):
    try:
        data = {}
        with connection.cursor() as cursor:
            query = """
                select id, nombre_campo, texto from tbr_texto_modulos
                where nombre_campo in ('descripcion_ausencia_departamental_1', 'descripcion_ausencia_departamental_2') 
            """
            cursor.execute(query)
            for row in cursor.fetchall():

                data_info = {
                    'id': row[0],
                    'nombre_campo': row[1],
                    'texto': row[2]
                }
                data[row[1]] = data_info
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)

@csrf_protect
def insertarInasistenciaDepartamentales(request):
    if request.method == 'POST':
        try:
            anio = request.POST.get('anio')
            semestre = request.POST.get('semestre')
            inasistencia_dep1 = request.POST.get('inasistencia_dep1')
            inasistencia_dep2 = request.POST.get('inasistencia_dep2')
            fecha_inicial = request.POST.get('fecha_inicial')
            fecha_fin = request.POST.get('fecha_fin')
            activo = request.POST.get('activo')
            
            user_id = 1 # TODO cambiar
            
            result = None
            with connection.cursor() as cursor:
                query = """
                    select id, usuario 
                    from tbr_usuarios 
                    where id = %s
                """
                cursor.execute(query,(user_id,))
                result = cursor.fetchone()
            if result is None:
                return JsonResponse({'message': 'Usuario no encontrado'}, status=500)
            
            usuario = result[1]
            data = {}
            with connection.cursor() as cursor:
                query = """
                    select id, nombre_campo, texto from tbr_texto_modulos
                    where nombre_campo in ('descripcion_ausencia_departamental_1', 'descripcion_ausencia_departamental_2') 
                """
                cursor.execute(query)
                for row in cursor.fetchall():

                    data_info = {
                        'id': row[0],
                        'nombre_campo': row[1],
                        'texto': row[2]
                    }
                    data[row[1]] = data_info
            
            des_x = data['descripcion_ausencia_departamental_1']['texto']
            des_y = data['descripcion_ausencia_departamental_2']['texto']
            data_insert =(anio,semestre,inasistencia_dep1,des_x,inasistencia_dep2,des_y,fecha_inicial,fecha_fin,activo,usuario,)
            
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO [tbr_data_criterios]
                    (
                        [id], -- Aquí está el campo [id]
                        [año],
                        [semestre],
                        [x],
                        [des_x],
                        [y],
                        [des_y],
                        [fecha_ini],
                        [fecha_fin],
                        [activo],
                        [fecha_ult],
                        [usuario_ult]
                    )
                    VALUES
                    (
                        4, -- id
                        %s, -- año
                        %s, -- semestre
                        %s, -- x
                        %s, -- des_x
                        %s, -- y
                        %s, -- des_y
                        %s, -- fecha_ini
                        %s, -- fecha_fin
                        %s, -- activo
                        GETDATE(), -- fecha_ult
                        %s -- usuario_ult
                    )
                """
                cursor.execute(query,data_insert)
            connection.commit()
            return JsonResponse({'message': 'Registros guardados exitosamente'})
        except Exception as e:
            return JsonResponse({'message': 'Error al guardar la información', 'error': e}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
    
def notasDepartamentales(request):
    try:
        data = []
        with connection.cursor() as cursor:
            query = """
                select AÑO,SEMESTRE,CRITERIO=nom_criterio,PROMEDIO_DEPARTAMENTALES=x,
                DESCRIP_A=des_x,FECHA_INI,FECHA_FIN,ACTIVO=case when activo=1 then 'SI' else 'NO' end,
                FECHA_ULTIMA=fecha_ult,USUARIO_ULTIMO=usuario_ult
                from tbr_data_criterios a, tbr_criterios b 
                where a.id=b.id and a.id=5 
                ORDER BY año,semestre,activo,fecha_ini,fecha_fin
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                data_info = {
                    'anio': row[0],
                    'SEMESTRE': row[1],
                    'CRITERIO': row[2],
                    'PROMEDIO_DEPARTAMENTALES': round((row[3]),2),
                    'DESCRIP_A': row[4],
                    'FECHA_INI': row[5],
                    'FECHA_FIN': row[6],
                    'ACTIVO': row[7],
                    'FECHA_ULTIMA': datetime.strftime(row[8], '%Y-%m-%d'),
                    'USUARIO_ULTIMO': row[9]
                }
                data.append(data_info)
            data_render = {
                'data': data
            }
        return render(request, 'mantenedor_notas_departamentales.html',data_render)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)

def obtenerDatosNotasDepartamentales(request):
    try:
        data = {}
        with connection.cursor() as cursor:
            query = """
                select id, nombre_campo, texto from tbr_texto_modulos
                where nombre_campo = 'descripcion_promedio_notas_departamentales'
            """
            cursor.execute(query)
            for row in cursor.fetchall():

                data_info = {
                    'id': row[0],
                    'nombre_campo': row[1],
                    'texto': row[2]
                }
                data[row[1]] = data_info
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)

@csrf_protect
def insertarNotasDepartamentales(request):
    if request.method == 'POST':
        try:
            anio = request.POST.get('anio')
            semestre = request.POST.get('semestre')
            rendimiento = request.POST.get('rendimiento')
            fecha_inicial = request.POST.get('fecha_inicial')
            fecha_fin = request.POST.get('fecha_fin')
            activo = request.POST.get('activo')
            
            user_id = 1 # TODO cambiar
            
            result = None
            with connection.cursor() as cursor:
                query = """
                    select id, usuario 
                    from tbr_usuarios 
                    where id = %s
                """
                cursor.execute(query,(user_id,))
                result = cursor.fetchone()
            if result is None:
                return JsonResponse({'message': 'Usuario no encontrado'}, status=500)
            
            usuario = result[1]
            data = {}
            with connection.cursor() as cursor:
                query = """
                    select id, nombre_campo, texto from tbr_texto_modulos
                    where nombre_campo = 'descripcion_promedio_notas_departamentales'
                """
                cursor.execute(query)
                for row in cursor.fetchall():

                    data_info = {
                        'id': row[0],
                        'nombre_campo': row[1],
                        'texto': row[2]
                    }
                    data[row[1]] = data_info
            
            des_x = data['descripcion_promedio_notas_departamentales']['texto']
            data_insert =(anio,semestre,rendimiento,des_x,fecha_inicial,fecha_fin,activo,usuario,)
            
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO [tbr_data_criterios]
                    (
                        [id], -- Aquí está el campo [id]
                        [año],
                        [semestre],
                        [x],
                        [des_x],
                        [fecha_ini],
                        [fecha_fin],
                        [activo],
                        [fecha_ult],
                        [usuario_ult]
                    )
                    VALUES
                    (
                        5, -- id
                        %s, -- año
                        %s, -- semestre
                        %s, -- x
                        %s, -- des_x
                        %s, -- fecha_ini
                        %s, -- fecha_fin
                        %s, -- activo
                        GETDATE(), -- fecha_ult
                        %s -- usuario_ult
                    )
                """
                cursor.execute(query,data_insert)
            connection.commit()
            return JsonResponse({'message': 'Registros guardados exitosamente'})
        except Exception as e:
            return JsonResponse({'message': 'Error al guardar la información', 'error': e}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

def rendimientoSemestrePrevio(request):
    try:
        data = []
        with connection.cursor() as cursor:
            query = """
                select AÑO,SEMESTRE,CRITERIO=nom_criterio,AUSENCIA_DEP_1=x,
                DESCRIP_A=des_x,FECHA_INI,FECHA_FIN,ACTIVO=case when activo=1 then 'SI' else 'NO' end,
                FECHA_ULTIMA=fecha_ult,USUARIO_ULTIMO=usuario_ult
                from tbr_data_criterios a, tbr_criterios b 
                where a.id=b.id and a.id= 6 
                ORDER BY año,semestre,activo,fecha_ini,fecha_fin
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                data_info = {
                    'anio': row[0],
                    'SEMESTRE': row[1],
                    'CRITERIO': row[2],
                    'AUSENCIA_DEP_1': round((row[3]),2),
                    'DESCRIP_A': row[4],
                    'FECHA_INI': row[5],
                    'FECHA_FIN': row[6],
                    'ACTIVO': row[7],
                    'FECHA_ULTIMA': datetime.strftime(row[8], '%Y-%m-%d'),
                    'USUARIO_ULTIMO': row[9]
                }
                data.append(data_info)
            data_render = {
                'data': data
            }
        return render(request, 'mantenedor_rendimiento_semestre_previo.html',data_render)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)
    

def obtenerDatosRendimientoSemestrePrevio(request):
    try:
        data = {}
        with connection.cursor() as cursor:
            query = """
                select id, nombre_campo, texto from tbr_texto_modulos
                where nombre_campo = 'descripcion_rendimiento_semestre_previo'
            """
            cursor.execute(query)
            for row in cursor.fetchall():

                data_info = {
                    'id': row[0],
                    'nombre_campo': row[1],
                    'texto': row[2]
                }
                data[row[1]] = data_info
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)

@csrf_protect
def insertarRendimientoSemestrePrevio(request):
    if request.method == 'POST':
        try:
            anio = request.POST.get('anio')
            semestre = request.POST.get('semestre')
            rendimiento = request.POST.get('rendimiento')
            fecha_inicial = request.POST.get('fecha_inicial')
            fecha_fin = request.POST.get('fecha_fin')
            activo = request.POST.get('activo')
            
            user_id = 1 # TODO cambiar
            
            result = None
            with connection.cursor() as cursor:
                query = """
                    select id, usuario 
                    from tbr_usuarios 
                    where id = %s
                """
                cursor.execute(query,(user_id,))
                result = cursor.fetchone()
            if result is None:
                return JsonResponse({'message': 'Usuario no encontrado'}, status=500)
            
            usuario = result[1]
            data = {}
            with connection.cursor() as cursor:
                query = """
                    select id, nombre_campo, texto from tbr_texto_modulos
                    where nombre_campo = 'descripcion_rendimiento_semestre_previo'
                """
                cursor.execute(query)
                for row in cursor.fetchall():

                    data_info = {
                        'id': row[0],
                        'nombre_campo': row[1],
                        'texto': row[2]
                    }
                    data[row[1]] = data_info
            
            des_x = data['descripcion_rendimiento_semestre_previo']['texto']
            data_insert =(anio,semestre,rendimiento,des_x,fecha_inicial,fecha_fin,activo,usuario,)
            
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO [tbr_data_criterios]
                    (
                        [id], -- Aquí está el campo [id]
                        [año],
                        [semestre],
                        [x],
                        [des_x],
                        [fecha_ini],
                        [fecha_fin],
                        [activo],
                        [fecha_ult],
                        [usuario_ult]
                    )
                    VALUES
                    (
                        6, -- id
                        %s, -- año
                        %s, -- semestre
                        %s, -- x
                        %s, -- des_x
                        %s, -- fecha_ini
                        %s, -- fecha_fin
                        %s, -- activo
                        GETDATE(), -- fecha_ult
                        %s -- usuario_ult
                    )
                """
                cursor.execute(query,data_insert)
            connection.commit()
            return JsonResponse({'message': 'Registros guardados exitosamente'})
        except Exception as e:
            return JsonResponse({'message': 'Error al guardar la información', 'error': e}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)


def inasistenciaControles(request):
    try:
        data = []
        with connection.cursor() as cursor:
            query = """
                select AÑO,SEMESTRE,CRITERIO=nom_criterio,AUSENCIA_DEP_1=x,
                DESCRIP_A=des_x,FECHA_INI,FECHA_FIN,ACTIVO=case when activo=1 then 'SI' else 'NO' end,
                FECHA_ULTIMA=fecha_ult,USUARIO_ULTIMO=usuario_ult
                from tbr_data_criterios a, tbr_criterios b 
                where a.id=b.id and a.id= 7 
                ORDER BY año,semestre,activo,fecha_ini,fecha_fin
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                data_info = {
                    'anio': row[0],
                    'SEMESTRE': row[1],
                    'CRITERIO': row[2],
                    'AUSENCIA_CONTROL': round((row[3]),2),
                    'DESCRIP_A': row[4],
                    'FECHA_INI': row[5],
                    'FECHA_FIN': row[6],
                    'ACTIVO': row[7],
                    'FECHA_ULTIMA': datetime.strftime(row[8], '%Y-%m-%d'),
                    'USUARIO_ULTIMO': row[9]
                }
                data.append(data_info)
            data_render = {
                'data': data
            }
        return render(request, 'mantenedor_inasistencia_controles.html',data_render)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)
    
def obtenerDatosInasistenciaControles(request):
    try:
        data = {}
        with connection.cursor() as cursor:
            query = """
                select id, nombre_campo, texto from tbr_texto_modulos
                where nombre_campo = 'descripcion_ausencia_control_inasistencia_controles'
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                data_info = {
                    'id': row[0],
                    'nombre_campo': row[1],
                    'texto': row[2]
                }
                data[row[1]] = data_info
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'message': 'Error al obtener la información', 'error': e}, status=500)

@csrf_protect
def insertarRendimientoSemestrePrevio(request):
    if request.method == 'POST':
        try:
            anio = request.POST.get('anio')
            semestre = request.POST.get('semestre')
            rendimiento = request.POST.get('rendimiento')
            fecha_inicial = request.POST.get('fecha_inicial')
            fecha_fin = request.POST.get('fecha_fin')
            activo = request.POST.get('activo')
            
            user_id = 1 # TODO cambiar
            
            result = None
            with connection.cursor() as cursor:
                query = """
                    select id, usuario 
                    from tbr_usuarios 
                    where id = %s
                """
                cursor.execute(query,(user_id,))
                result = cursor.fetchone()
            if result is None:
                return JsonResponse({'message': 'Usuario no encontrado'}, status=500)
            
            usuario = result[1]
            data = {}
            with connection.cursor() as cursor:
                query = """
                    select id, nombre_campo, texto from tbr_texto_modulos
                    where nombre_campo = 'descripcion_ausencia_control_inasistencia_controles'
                """
                cursor.execute(query)
                for row in cursor.fetchall():

                    data_info = {
                        'id': row[0],
                        'nombre_campo': row[1],
                        'texto': row[2]
                    }
                    data[row[1]] = data_info
            
            des_x = data['descripcion_ausencia_control_inasistencia_controles']['texto']
            data_insert =(anio,semestre,rendimiento,des_x,fecha_inicial,fecha_fin,activo,usuario,)
            
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO [tbr_data_criterios]
                    (
                        [id], -- Aquí está el campo [id]
                        [año],
                        [semestre],
                        [x],
                        [des_x],
                        [fecha_ini],
                        [fecha_fin],
                        [activo],
                        [fecha_ult],
                        [usuario_ult]
                    )
                    VALUES
                    (
                        7, -- id
                        %s, -- año
                        %s, -- semestre
                        %s, -- x
                        %s, -- des_x
                        %s, -- fecha_ini
                        %s, -- fecha_fin
                        %s, -- activo
                        GETDATE(), -- fecha_ult
                        %s -- usuario_ult
                    )
                """
                cursor.execute(query,data_insert)
            connection.commit()
            return JsonResponse({'message': 'Registros guardados exitosamente'})
        except Exception as e:
            return JsonResponse({'message': 'Error al guardar la información', 'error': e}, status=500)
    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)
