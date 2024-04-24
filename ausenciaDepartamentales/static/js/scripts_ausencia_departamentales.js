
$(document).ready( function () {
    
    $('#asignaturas').DataTable({
        "bLengthChange" : false,
        "language": {
            "sEmptyTable": "No hay datos disponibles en la tabla",
            "sInfo": "Mostrando _START_ a _END_ de _TOTAL_ entradas",
            "sInfoEmpty": "Mostrando 0 a 0 de 0 entradas",
            "sInfoFiltered": "(filtrado de un total de _MAX_ entradas)",
            "sInfoPostFix": "",
            "sInfoThousands": ",",
            "sLengthMenu": "Mostrar _MENU_ entradas",
            "sLoadingRecords": "Cargando...",
            "sProcessing": "Procesando...",
            "sSearch": "Buscar:",
            "sZeroRecords": "No se encontraron coincidencias",
            "oPaginate": {
                "sFirst": "Primero",
                "sLast": "Último",
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
            },
            "oAria": {
                "sSortAscending": ": activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": activar para ordenar la columna de manera descendente"
            },

            "oPaginate": {
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
            },
        },
    });

    $('#ausencias').DataTable({
        "bLengthChange" : false,
        "language": {
            "sEmptyTable": "No hay datos disponibles en la tabla",
            "sInfo": "Mostrando _START_ a _END_ de _TOTAL_ entradas",
            "sInfoEmpty": "Mostrando 0 a 0 de 0 entradas",
            "sInfoFiltered": "(filtrado de un total de _MAX_ entradas)",
            "sInfoPostFix": "",
            "sInfoThousands": ",",
            "sLengthMenu": "Mostrar _MENU_ entradas",
            "sLoadingRecords": "Cargando...",
            "sProcessing": "Procesando...",
            "sSearch": "Buscar:",
            "sZeroRecords": "No se encontraron coincidencias",
            "oPaginate": {
                "sFirst": "Primero",
                "sLast": "Último",
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
            },
            "oAria": {
                "sSortAscending": ": activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": activar para ordenar la columna de manera descendente"
            },

            "oPaginate": {
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
            },
        },
        "ajax": {
            "url": "listadoAusencias/",
            "dataSrc": "data",
            "type": "POST",
            "beforeSend": function(xhr){
                let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
                // Agrega el token CSRF a los datos de la solicitud
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }
        },
        "columns": [
            { "data": "fecha" },
            { "data": "nombre" },
            { "data": "cod_asig" },
            { "data": "departamental" }
            // Agrega más columnas según la estructura de tus datos
        ]
    });


    $('#form_ausencia').submit(function(event) {
        event.preventDefault();

        var checkboxesMarcados = [];
        $('#asignaturas').DataTable().rows().every(function() {
            var checkbox = $(this.node()).find('td:first-child input[type="checkbox"]');
            if (checkbox.prop('checked')) {
                checkboxesMarcados.push(checkbox.val());
            }
        });
        
        fecha = $("#fecha").val();
        id_alumno = $("#id_alumno").val();
        departamental = $("#departamental").val();
        

        console.log(fecha +" "+ id_alumno+" "+departamental);
        if (fecha== "" || id_alumno == "" || departamental == "") {
            Swal.fire({
                title: '',
                text: '¡Debe seleccionar todos los campos!',
                icon: 'error',
                confirmButtonText: 'Aceptar'
            });
            return;
        }

        if (checkboxesMarcados.length == 0) {
            Swal.fire({
                title: '',
                text: '¡Debe seleccionar al menos una asignatura!',
                icon: 'error',
                confirmButtonText: 'Aceptar'
            });
            return;
        }
        
        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        let form = new FormData();
        form.append('csrfmiddlewaretoken', csrfToken); // Agrega el token CSRF al FormData

        // Agrega los demás datos del formulario al FormData
        form.append('fecha', fecha);
        form.append('id_alumno', id_alumno);
        form.append('departamental', departamental);
        form.append('codigos', checkboxesMarcados);

        $.ajax({
            url: '/postAusencia/',
            method: 'POST',
            data: form,
            processData: false,
            contentType: false, 
            success: function(response) {
                Swal.fire({
                    title: '',
                    text: response.message,
                    icon: 'success',
                    timer: 2000
                })
                $('#ausencias').DataTable().ajax.reload();
            },
            error: function(xhr, status, error) {
                response = JSON.parse(xhr.responseText)
                Swal.fire({
                    title: '',
                    text: response.message,
                    icon: 'error',
                    confirmButtonText: 'Aceptar'
                });
            }
        });
    });
    
    $("#id_alumno").selectize({
        highlight: false,
    });

});