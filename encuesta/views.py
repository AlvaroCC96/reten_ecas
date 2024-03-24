from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db import connection
from django.views.decorators.csrf import csrf_protect
import json
import traceback



def homeEncuestas(request):
    return render(request, 'encuesta.html')

def entrevista(request):
    
    query = """
        SELECT
        P.id AS pregunta_id,
        P.categoria AS pregunta,
        '[' + ISNULL(STUFF((SELECT ', "' + R.respuesta + '"'
                            FROM tbr_respuestas_encuestas R
                            WHERE R.id_categoria = P.id
                            FOR XML PATH('')), 1, 2, ''), '') + ']' AS respuestas,
        '[' + ISNULL(STUFF((SELECT ', ' + CONVERT(VARCHAR, R.id)
                            FROM tbr_respuestas_encuestas R
                            WHERE R.id_categoria = P.id
                            FOR XML PATH('')), 1, 2, ''), '') + ']' AS id_respuestas,
        P.saltable as saltable
        FROM
    tbr_categorias_encuestas P
    """
    resultados = None
    with connection.cursor() as cursor:
        cursor.execute(query)
        resultados = cursor.fetchall()
        
    data_cuestionario = []
    if resultados is not None:
        for resultado in resultados:
            data_pregunta = {}
            data_respuestas = []
            pregunta_id = resultado[0]
            pregunta = resultado[1]
            respuestas = json.loads(resultado[2])
            respuestas_id = json.loads(resultado[3])
            pregunta_saltable = resultado[4]
            for x in range (len(respuestas)):
                opcion = {
                    'respuesta_id': respuestas_id[x],
                    'respuesta': respuestas[x]
                }
                data_respuestas.append(opcion)
            
            data_pregunta = {
                'pregunta_id':pregunta_id,
                'pregunta':pregunta,
                'saltable':pregunta_saltable,
                'respuestas':data_respuestas
            }
            data_cuestionario.append(data_pregunta)
        
    query = """
        SELECT 
            id, 
            rut, 
            ISNULL(nombres + ' ', '') + ISNULL(apellido_m + ' ', '') + ISNULL(apellido_p, '') AS nombre_completo 
        FROM 
            tb_alumnos
    """
    alumnos = None
    with connection.cursor() as cursor:
        cursor.execute(query)
        alumnos = cursor.fetchall()
    
    data_render = {
        'alumnos' : alumnos,
        'cuestionario' : data_cuestionario
    }
    return render(request, 'entrevista.html', data_render)

@csrf_protect
def postEntrevista(request):
    if request.method == 'POST':
        preguntasRequest = request.POST.get('preguntas')
        id_alumno = request.POST.get('id_alumno')
        if id_alumno == '' or preguntasRequest is None or preguntasRequest == '':
            return JsonResponse({'message': 'Complete todos los campos de la encuesta y seleccione al/la alumno/a'}, status=500)
        preguntas = json.loads(preguntasRequest)
        lista_preguntas = []
        json_puntajes = {}
        respuesta_pregunta_34 = None
        for pregunta, respuesta in preguntas.items():
            if pregunta == 'pregunta34':
                respuesta_pregunta_34 = respuesta
            else:
                lista_preguntas.append(int(respuesta))
                numero_pregunta = int(pregunta.lstrip('pregunta'))
                json_puntajes[numero_pregunta] = int(respuesta) if respuesta.isdigit() else respuesta
        
        try:
            puntaje = obtenerPuntaje(lista_preguntas=lista_preguntas)
            id_encuesta = insertar_encuesta(id_alumno=id_alumno,puntaje=puntaje)
            if id_encuesta is None:
                return JsonResponse({'message': 'Error al registrar la encuesta, contacte al administrador  '}, status=500)

            id_detalle = insertar_detalle_encuesta(preguntas=json_puntajes,id_encuesta=id_encuesta)
            if id_detalle is None:
                return JsonResponse({'message': 'Error al registrar el detalle de la encuesta, contacte al administrador  '}, status=500)
            
            if respuesta_pregunta_34 is not None or respuesta_pregunta_34 != '':
                id_pregunta34 = insertar_detalle_pregunta34(id_encuesta=id_encuesta,respuesta =respuesta_pregunta_34)
                if id_pregunta34 is None:
                    return JsonResponse({'message': 'Error al registrar el detalle de la encuesta, contacte al administrador  '}, status=500)
            return JsonResponse({'message': 'Encuesta guardada correctamente'}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Error al registrar la encuesta, contacte al administrador  '}, status=500)
            
    else:
        return JsonResponse({'message': 'Error al realizar esta acción'}, status=405)

def obtenerPuntaje (lista_preguntas):
    lista_str = ', '.join(str(id_pregunta) for id_pregunta in lista_preguntas)
    query = """
        SELECT SUM(puntaje) AS puntaje_total FROM tbr_respuestas_encuestas
        WHERE id IN ({})
    """.format(lista_str)
    
    puntaje = None
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            puntaje = row[0]
    return puntaje

def insertar_encuesta(id_alumno, puntaje):
    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO [tbr_encuesta_alumno] ([id_alumno], [puntaje_total], [created_at], [updated_at]) VALUES (%s, %s, GETDATE(), GETDATE())
            """
            cursor.execute(query, (id_alumno, puntaje))
            connection.commit()  # Confirmar los cambios en la base de datos
            
            query = "SELECT MAX(id) FROM tbr_encuesta_alumno WHERE id_alumno = %s"
            cursor.execute(query,(id_alumno))
            inserted_id = cursor.fetchone()[0]
            return inserted_id
            
    except Exception as e:
        traceback.print_exc()
        print("Error al insertar encuesta: ", e)

def insertar_detalle_encuesta(preguntas, id_encuesta):
    query = """
        INSERT INTO [tbr_detalle_respuestas_alumno] ([id_encuesta], [id_pregunta], [id_detalle_respuesta] , [created_at], [updated_at]) VALUES (%s, %s, %s, GETDATE(), GETDATE())
    """ 
    with connection.cursor() as cursor:
        for pregunta, respuesta in preguntas.items():
            cursor.execute(query, (id_encuesta, int(pregunta), int(respuesta)))
            connection.commit()  # Confirmar los cambios en la base de datos
        query = "SELECT MAX(id) FROM tbr_detalle_respuestas_alumno WHERE id_encuesta = %s"
        cursor.execute(query,(id_encuesta,))
        inserted_id = cursor.fetchone()[0]
        return inserted_id

def insertar_detalle_pregunta34(id_encuesta,respuesta):
    query = """
        INSERT INTO [tbr_detalle_respuestas_alumno_texto] ([id_encuesta], [id_pregunta], [texto] , [created_at], [updated_at]) VALUES (%s, 34, %s, GETDATE(), GETDATE())
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (id_encuesta, respuesta))
        connection.commit()  # Confirmar los cambios en la base de datos
        query = "SELECT id FROM tbr_detalle_respuestas_alumno_texto WHERE id_encuesta = %s"
        cursor.execute(query,(id_encuesta,))
        inserted_id = cursor.fetchone()[0]
        return inserted_id
    
def analisis_entrevista(request):
    query = """
        SELECT 
            id, 
            categoria
        FROM 
            tbr_categorias_encuestas
        WHERE deleted_at is null and id <> 34
    """
    categorias = None
    with connection.cursor() as cursor:
        cursor.execute(query)
        categorias = cursor.fetchall()
    
    data_render = {
        'categorias' : categorias,
    }
    return render(request, 'analisis.html',data_render)

def obtenerDatosGrafico(request,id_categoria):
    query = """
        SELECT
            tre.respuesta,
            COUNT(*) AS total
        FROM
            tbr_detalle_respuestas_alumno tdra
        LEFT JOIN
            tbr_respuestas_encuestas tre ON
                tdra.id_detalle_respuesta = tre.id
        WHERE
            id_pregunta = %s and 
            id_encuesta IN (SELECT max(id) AS id
                FROM tbr_encuesta_alumno
                GROUP BY id_alumno)
        GROUP BY
        tre.respuesta
        ORDER BY
        total DESC;
    """
    resultado = None
    with connection.cursor() as cursor:
        cursor.execute(query,(id_categoria,))
        resultado = cursor.fetchall()
    
    labels = []
    datos = []
    for elemento in resultado:
        labels.append(elemento[0])
        datos.append(elemento[1])
    return JsonResponse({'labels': labels, 'datos': datos})
    
