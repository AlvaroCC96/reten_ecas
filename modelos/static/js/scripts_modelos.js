$(document).ready( function () {

    // Inicio Mantenedor Toma de Ramos
    $('#agregarRegistroModal').on('shown.bs.modal', function () {
        fetch('/obtenerDatosTomaRamos/')  
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener los datos');
            }
            return response.json();
        }).then(data => {
            let descripcion_dias_alarma_toma_ramos = data.descripcion_dias_alarma_toma_ramos;
            let descripcion_dias_previos_toma_ramos  = data.descripcion_dias_previos_toma_ramos;
            $('#agregarRegistroModal #descripcion_a').text(descripcion_dias_previos_toma_ramos.texto);
            $('#agregarRegistroModal #descripcion_b').text(descripcion_dias_alarma_toma_ramos.texto);
        }).catch(e=>{
            console.log(error);
        });
    });

    $('#agregarRegistroTomaRamosForm').submit(function(e){
        e.preventDefault();
        let formData = new FormData(this);
        Swal.fire({
            title: 'Confirmación',
            text: '¿Estás seguro de realizar esta acción?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
              $.ajax({
                url: '/insertarTomaRamos/',
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                  Swal.fire({
                    title: 'Éxito',
                    text: 'La acción se realizó correctamente, se recargará la página',
                    icon: 'success',
                    confirmButtonText: 'Aceptar'
                  }).then((result)=> {
                    if(result.isConfirmed){
                        $('#agregarRegistroModal').modal('hide');
                        location.reload();
                    }
                  });
                },
                error: function(xhr, status, error) {
                  let errorMessage = "Hubo un error al realizar la acción";
                  if (xhr.responseText) {
                      try {
                          const response = JSON.parse(xhr.responseText);
                          if (response.message) {
                              errorMessage = response.message;
                          }
                      } catch (e) {
                          console.error("Error al analizar la respuesta del servidor:", e);
                      }
                  }
                  Swal.fire({
                      title: 'Error',
                      text: errorMessage,
                      icon: 'error',
                      confirmButtonText: 'Aceptar',
                  })
                }
              });
            }
        })
    });

    $('#mantenedor_toma_ramos_table').DataTable({
        "bLengthChange" : false,
        "pageLength": 5, 
        "searching": false, 
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
    // Fin Mantenedor Toma de Ramos

    // Inicio Mantenedor Asistencia a clases
    $('#modalAsistenciaClases').on('shown.bs.modal', function () {
        fetch('/obtenerDatosAsistencia/')  
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener los datos');
            }
            return response.json();
        }).then(data => {
            let descripcion_dias_alarma_toma_ramos = data.descripcion_dias_alarma_asistencia_clases;
            let descripcion_dias_previos_toma_ramos  = data.descripcion_dias_previos_asistencia_clases;
            $('#modalAsistenciaClases #descripcion_a').text(descripcion_dias_previos_toma_ramos.texto);
            $('#modalAsistenciaClases #descripcion_b').text(descripcion_dias_alarma_toma_ramos.texto);
        }).catch(e=>{
            console.log(error);
        });
    });

    $('#modalAsistenciaClasesForm').submit(function(e){
        e.preventDefault();
        let formData = new FormData(this);
        Swal.fire({
            title: 'Confirmación',
            text: '¿Estás seguro de realizar esta acción?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
              $.ajax({
                url: '/insertarAsistenciaModelo/',
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                  Swal.fire({
                    title: 'Éxito',
                    text: 'La acción se realizó correctamente, se recargará la página',
                    icon: 'success',
                    confirmButtonText: 'Aceptar'
                  }).then((result)=> {
                    if(result.isConfirmed){
                        $('#modalAsistenciaClases').modal('hide');
                        location.reload();
                    }
                  });
                },
                error: function(xhr, status, error) {
                  let errorMessage = "Hubo un error al realizar la acción";
                  if (xhr.responseText) {
                      try {
                          const response = JSON.parse(xhr.responseText);
                          if (response.message) {
                              errorMessage = response.message;
                          }
                      } catch (e) {
                          console.error("Error al analizar la respuesta del servidor:", e);
                      }
                  }
                  Swal.fire({
                      title: 'Error',
                      text: errorMessage,
                      icon: 'error',
                      confirmButtonText: 'Aceptar',
                  })
                }
              });
            }
        })
    });

    $('#mantenedor_asistencia_table').DataTable({
        "bLengthChange" : false,
        "pageLength": 5, 
        "searching": false, 
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
    // Fin Mantenedor Asistencia a clases

    // Inicio Mantenedor Notas Parciales 
    $('#agregarRegistroModalNotasParciales').on('shown.bs.modal', function () {
        fetch('/obtenerDatosNotasParciales/')  
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener los datos');
            }
            return response.json();
        }).then(data => {
            let descripcion_promedio_notas_parciales = data.descripcion_promedio_notas_parciales;
            let descripcion_cantidad_controles_notas_parciales  = data.descripcion_cantidad_controles_notas_parciales;
            $('#agregarRegistroModalNotasParciales #descripcion_a').text(descripcion_cantidad_controles_notas_parciales.texto);
            $('#agregarRegistroModalNotasParciales #descripcion_b').text(descripcion_promedio_notas_parciales.texto);
        }).catch(e=>{
            console.log(e);
        });
    });

    $('#agregarRegistroFormNotasParciales').submit(function(e){
        e.preventDefault();
        let formData = new FormData(this);
        Swal.fire({
            title: 'Confirmación',
            text: '¿Estás seguro de realizar esta acción?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
              $.ajax({
                url: '/insertarNotasParciales/',
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                  Swal.fire({
                    title: 'Éxito',
                    text: 'La acción se realizó correctamente, se recargará la página',
                    icon: 'success',
                    confirmButtonText: 'Aceptar'
                  }).then((result)=> {
                    if(result.isConfirmed){
                        $('#agregarRegistroModalNotasParciales').modal('hide');
                        location.reload();
                    }
                  });
                },
                error: function(xhr, status, error) {
                  let errorMessage = "Hubo un error al realizar la acción";
                  if (xhr.responseText) {
                      try {
                          const response = JSON.parse(xhr.responseText);
                          if (response.message) {
                              errorMessage = response.message;
                          }
                      } catch (e) {
                          console.error("Error al analizar la respuesta del servidor:", e);
                      }
                  }
                  Swal.fire({
                      title: 'Error',
                      text: errorMessage,
                      icon: 'error',
                      confirmButtonText: 'Aceptar',
                  })
                }
              });
            }
        })
    });

    $('#mantenedor_notas_parciales_table').DataTable({
        "bLengthChange" : false,
        "pageLength": 5, 
        "searching": false, 
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
    // Fin Mantenedor Notas Parciales

    // Inicio Mantenedor Inasistencias Departamentales
    $('#agregarRegistroModalInasistenciaDepartamentales').on('shown.bs.modal', function () {
        fetch('/obtenerDatosInasistenciaDepartamentales/')  
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener los datos');
            }
            return response.json();
        }).then(data => {
            let descripcion_ausencia_departamental_1 = data.descripcion_ausencia_departamental_1;
            let descripcion_ausencia_departamental_2  = data.descripcion_ausencia_departamental_2;
            $('#agregarRegistroModalInasistenciaDepartamentales #descripcion_a').text(descripcion_ausencia_departamental_1.texto);
            $('#agregarRegistroModalInasistenciaDepartamentales #descripcion_b').text(descripcion_ausencia_departamental_2.texto);
        }).catch(e=>{
            console.log(e);
        });
    });

    $('#agregarRegistroFormInasistenciaDepartamentales').submit(function(e){
        e.preventDefault();
        let formData = new FormData(this);
        Swal.fire({
            title: 'Confirmación',
            text: '¿Estás seguro de realizar esta acción?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
              $.ajax({
                url: '/insertarInasistenciaDepartamentales/',
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                  Swal.fire({
                    title: 'Éxito',
                    text: 'La acción se realizó correctamente, se recargará la página',
                    icon: 'success',
                    confirmButtonText: 'Aceptar'
                  }).then((result)=> {
                    if(result.isConfirmed){
                        $('#agregarRegistroModalInasistenciaDepartamentales').modal('hide');
                        location.reload();
                    }
                  });
                },
                error: function(xhr, status, error) {
                  let errorMessage = "Hubo un error al realizar la acción";
                  if (xhr.responseText) {
                      try {
                          const response = JSON.parse(xhr.responseText);
                          if (response.message) {
                              errorMessage = response.message;
                          }
                      } catch (e) {
                          console.error("Error al analizar la respuesta del servidor:", e);
                      }
                  }
                  Swal.fire({
                      title: 'Error',
                      text: errorMessage,
                      icon: 'error',
                      confirmButtonText: 'Aceptar',
                  })
                }
              });
            }
        })
    });

    $('#mantenedor_inasistencia_departamentales_table').DataTable({
        "bLengthChange" : false,
        "pageLength": 5, 
        "searching": false, 
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
    // Fin Mantenedor Inasistencias Departamentales

    // Inicio Mantenedor Notas Departamentales
    $('#agregarRegistroModalNotasDepartamentales').on('shown.bs.modal', function () {
        fetch('/obtenerDatosNotasDepartamentales/')  
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener los datos');
            }
            return response.json();
        }).then(data => {
            let descripcion_promedio_notas_departamentales = data.descripcion_promedio_notas_departamentales;
            $('#agregarRegistroModalNotasDepartamentales #descripcion_a').text(descripcion_promedio_notas_departamentales.texto);
            
        }).catch(e=>{
            console.log(e);
        });
    });

    $('#agregarRegistroFormNotasDepartamentales').submit(function(e){
        e.preventDefault();
        let formData = new FormData(this);
        Swal.fire({
            title: 'Confirmación',
            text: '¿Estás seguro de realizar esta acción?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
              $.ajax({
                url: '/insertarNotasDepartamentales/',
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                  Swal.fire({
                    title: 'Éxito',
                    text: 'La acción se realizó correctamente, se recargará la página',
                    icon: 'success',
                    confirmButtonText: 'Aceptar'
                  }).then((result)=> {
                    if(result.isConfirmed){
                        $('#agregarRegistroModalNotasDepartamentales').modal('hide');
                        location.reload();
                    }
                  });
                },
                error: function(xhr, status, error) {
                  let errorMessage = "Hubo un error al realizar la acción";
                  if (xhr.responseText) {
                      try {
                          const response = JSON.parse(xhr.responseText);
                          if (response.message) {
                              errorMessage = response.message;
                          }
                      } catch (e) {
                          console.error("Error al analizar la respuesta del servidor:", e);
                      }
                  }
                  Swal.fire({
                      title: 'Error',
                      text: errorMessage,
                      icon: 'error',
                      confirmButtonText: 'Aceptar',
                  })
                }
              });
            }
        })
    });

    $('#mantenedor_notas_departamentales_table').DataTable({
        "bLengthChange" : false,
        "pageLength": 5, 
        "searching": false, 
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
    // Fin Mantenedor Notas Departamentales

    // Inicio Mantenedor Rendimiento Semestre Previo
    $('#agregarRegistroModalRendimientoSemestrePrevio').on('shown.bs.modal', function () {
        fetch('/obtenerDatosRendimientoSemestrePrevio/')  
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener los datos');
            }
            return response.json();
        }).then(data => {
            let descripcion_rendimiento_semestre_previo = data.descripcion_rendimiento_semestre_previo;
            $('#agregarRegistroModalRendimientoSemestrePrevio #descripcion_a').text(descripcion_rendimiento_semestre_previo.texto);
            
        }).catch(e=>{
            console.log(e);
        });
    });

    $('#agregarRegistroFormRendimientoSemestrePrevio').submit(function(e){
        e.preventDefault();
        let formData = new FormData(this);
        Swal.fire({
            title: 'Confirmación',
            text: '¿Estás seguro de realizar esta acción?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
              $.ajax({
                url: '/insertarRendimientoSemestrePrevio/',
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                  Swal.fire({
                    title: 'Éxito',
                    text: 'La acción se realizó correctamente, se recargará la página',
                    icon: 'success',
                    confirmButtonText: 'Aceptar'
                  }).then((result)=> {
                    if(result.isConfirmed){
                        $('#agregarRegistroModalRendimientoSemestrePrevio').modal('hide');
                        location.reload();
                    }
                  });
                },
                error: function(xhr, status, error) {
                  let errorMessage = "Hubo un error al realizar la acción";
                  if (xhr.responseText) {
                      try {
                          const response = JSON.parse(xhr.responseText);
                          if (response.message) {
                              errorMessage = response.message;
                          }
                      } catch (e) {
                          console.error("Error al analizar la respuesta del servidor:", e);
                      }
                  }
                  Swal.fire({
                      title: 'Error',
                      text: errorMessage,
                      icon: 'error',
                      confirmButtonText: 'Aceptar',
                  })
                }
              });
            }
        })
    });

    $('#mantenedor_rendimiento_semestre_previo_table').DataTable({
        "bLengthChange" : false,
        "pageLength": 5, 
        "searching": false, 
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
    // Fin Mantenedor Rendimiento Semestre Previo

    // Inicio Mantenedor Rendimiento Inasistencia Controles
    $('#agregarRegistroModalInasistenciaControles').on('shown.bs.modal', function () {
        fetch('/obtenerDatosInasistenciaControles/')  
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener los datos');
            }
            return response.json();
        }).then(data => {
            let descripcion_ausencia_control_inasistencia_controles = data.descripcion_ausencia_control_inasistencia_controles;
            $('#agregarRegistroModalInasistenciaControles #descripcion_a').text(descripcion_ausencia_control_inasistencia_controles.texto);
            
        }).catch(e=>{
            console.log(e);
        });
    });

    $('#agregarRegistroFormInasistenciaControles').submit(function(e){
        e.preventDefault();
        let formData = new FormData(this);
        Swal.fire({
            title: 'Confirmación',
            text: '¿Estás seguro de realizar esta acción?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
              $.ajax({
                url: '/insertarRendimientoSemestrePrevio/',
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                  Swal.fire({
                    title: 'Éxito',
                    text: 'La acción se realizó correctamente, se recargará la página',
                    icon: 'success',
                    confirmButtonText: 'Aceptar'
                  }).then((result)=> {
                    if(result.isConfirmed){
                        $('#agregarRegistroModalInasistenciaControles').modal('hide');
                        location.reload();
                    }
                  });
                },
                error: function(xhr, status, error) {
                  let errorMessage = "Hubo un error al realizar la acción";
                  if (xhr.responseText) {
                      try {
                          const response = JSON.parse(xhr.responseText);
                          if (response.message) {
                              errorMessage = response.message;
                          }
                      } catch (e) {
                          console.error("Error al analizar la respuesta del servidor:", e);
                      }
                  }
                  Swal.fire({
                      title: 'Error',
                      text: errorMessage,
                      icon: 'error',
                      confirmButtonText: 'Aceptar',
                  })
                }
              });
            }
        })
    });

    $('#mantenedor_inasistencia_controles_table').DataTable({
        "bLengthChange" : false,
        "pageLength": 5, 
        "searching": false, 
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

    // Fin Mantenedor Rendimiento Inasistencia Controles
});