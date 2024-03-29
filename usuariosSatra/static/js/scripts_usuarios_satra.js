
$(document).ready( function () {

    let tabla_usuarios_satra = $('#tabla_usuarios_satra').DataTable({
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
            "url": "listadoUsuariosSatra/",
            "dataSrc": "data",
            "type": "POST",
            "beforeSend": function(xhr){
                let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
                // Agrega el token CSRF a los datos de la solicitud
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }
        },
        "columns": [
            { "data": "id" },
            { "data": "usuario" },
            { "data": "persona" },
            { "data": "cargo" },
            { "data": null, "defaultContent": "<button class='btn btn-info' id='verDetalleUsuario'>Detalle Usuario</button>" }
            // Agregar columna accion ???
        ]
    });

    $('#tabla_usuarios_satra tbody').on('click', '#verDetalleUsuario', function() {
        console.log("hola")
        let data = tabla_usuarios_satra.row($(this).parents('tr')).data();
        let id = data.id; // Obtener el ID del usuario
        $('#editarUsuario').modal('show'); // Corregir aquí
    });

    $('#activar_edicion').click(function() {
        // Si hay algún campo deshabilitado, activar todos los campos
        if ($('#editarUsuario form #cargo:disabled').length > 0 || $('#editarUsuario form select:disabled').length > 0) {
            $('#editarUsuario #cargo, #editarUsuario #activo, #editarUsuario #fecha_ini, #editarUsuario #fecha_fin, #editarUsuario form select').prop('disabled', false);
            $('#actualizarUsuario').prop('disabled', false);
        } else {
            // Si todos los campos están activos, desactivarlos todos
            $('#editarUsuario #cargo, #editarUsuario #activo, #editarUsuario #fecha_ini, #editarUsuario #fecha_fin, #editarUsuario form select').prop('disabled', true);
            $('#actualizarUsuario').prop('disabled', true);
        }
    });
    
    $('#editarUsuario').on('hidden.bs.modal', function() {
        $('#editarUsuario form input, #editarUsuario form select').prop('disabled', true);
        $('#actualizarUsuario').prop('disabled', true);
    });
    

    // $('#form_ausencia').submit(function(event) {
    //     event.preventDefault();

    //     var checkboxesMarcados = [];
    //     $('#asignaturas').DataTable().rows().every(function() {
    //         var checkbox = $(this.node()).find('td:first-child input[type="checkbox"]');
    //         if (checkbox.prop('checked')) {
    //             checkboxesMarcados.push(checkbox.val());
    //         }
    //     });
        
    //     fecha = $("#fecha").val();
    //     id_alumno = $("#id_alumno").val();
    //     departamental = $("#departamental").val();
        

    //     console.log(fecha +" "+ id_alumno+" "+departamental);
    //     if (fecha== "" || id_alumno == "" || departamental == "") {
    //         Swal.fire({
    //             title: '',
    //             text: '¡Debe seleccionar todos los campos!',
    //             icon: 'error',
    //             confirmButtonText: 'Aceptar'
    //         });
    //         return;
    //     }

    //     if (checkboxesMarcados.length == 0) {
    //         Swal.fire({
    //             title: '',
    //             text: '¡Debe seleccionar al menos una asignatura!',
    //             icon: 'error',
    //             confirmButtonText: 'Aceptar'
    //         });
    //         return;
    //     }
        
    //     let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    //     let form = new FormData();
    //     form.append('csrfmiddlewaretoken', csrfToken); // Agrega el token CSRF al FormData

    //     // Agrega los demás datos del formulario al FormData
    //     form.append('fecha', fecha);
    //     form.append('id_alumno', id_alumno);
    //     form.append('departamental', departamental);
    //     form.append('codigos', checkboxesMarcados);

    //     $.ajax({
    //         url: '/postAusencia/',
    //         method: 'POST',
    //         data: form,
    //         processData: false,
    //         contentType: false, 
    //         success: function(response) {
    //             Swal.fire({
    //                 title: '',
    //                 text: response.message,
    //                 icon: 'success',
    //                 timer: 2000
    //             })
    //             $('#ausencias').DataTable().ajax.reload();
    //         },
    //         error: function(xhr, status, error) {
    //             response = JSON.parse(xhr.responseText)
    //             Swal.fire({
    //                 title: '',
    //                 text: response.message,
    //                 icon: 'error',
    //                 confirmButtonText: 'Aceptar'
    //             });
    //         }
    //     });
    // });
    
    // $("#id_alumno").selectize({
    //     highlight: false,
    // });

});