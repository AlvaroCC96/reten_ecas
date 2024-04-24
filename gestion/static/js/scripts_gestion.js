// Define la función editarCita fuera del ámbito de $(document).ready()
const editarCita = (event) => {
  id = event.event.id;
  fetch('../obtenerDatosEditarCita/' + id)  
  .then(response => {
    if (!response.ok) {
        throw new Error('Error al obtener los datos');
    }
    return response.json();
  })
  .then(data => {
    const datos = data.datos;
    $('#editarCita #motivo').empty();
    $('#editarCita #nombre_alumno').val(datos.nombre);
    $('#editarCita #rut').val(datos.rut);
    $('#editarCita #rut').val(datos.rut);
    let select = $('#editarCita #motivo');
    let emptyOption = $('<option></option>').attr('value', '').text("Seleccione una opción");
    select.append(emptyOption);
    datos.motivos.forEach(motivo => {
        let option = $('<option></option>').attr('value', motivo[0]).text(motivo[1]);
        if (datos.id_motivo === motivo[0]) {
          option.attr('selected',true)
        }
        select.append(option);
    });
    let fecha = new Date(datos.fecha_consulta);
    let horaInicioParts = datos.hora_inicio.split(':');
    let horaInicio = new Date();
    horaInicio.setHours(parseInt(horaInicioParts[0]));
    horaInicio.setMinutes(parseInt(horaInicioParts[1]));
    horaInicio.setSeconds(parseInt(horaInicioParts[2]));

    let horaFinParts = datos.hora_termino.split(':');
    let horaFin = new Date();
    horaFin.setHours(parseInt(horaFinParts[0]));
    horaFin.setMinutes(parseInt(horaFinParts[1]));
    horaFin.setSeconds(parseInt(horaFinParts[2]));
    let hora_inicio_formated = ("0" + horaInicio.getHours()).slice(-2) + ":" + ("0" + horaInicio.getMinutes()).slice(-2) + ":" + ("0" + horaInicio.getSeconds()).slice(-2);
    let hora_fin_formated = ("0" + horaFin.getHours()).slice(-2) + ":" + ("0" + horaFin.getMinutes()).slice(-2) + ":" + ("0" + horaFin.getSeconds()).slice(-2);
    let fecha_formated = fecha.toISOString().split('T')[0];
  
    $('#editarCita #fecha_consulta').val(fecha_formated);
    $('#editarCita #hora_inicio_consulta').val(hora_inicio_formated);
    $('#editarCita #hora_termino_consulta').val(hora_fin_formated);
    $('#editarCita #texto_comentario').val(datos.comentario);
    $('#editarCita #id_cita').val(id);

    $('#editarCita #guardarCita').attr('hidden',false);
    $('#editarCita #eliminarCita').attr('hidden',false);
    $('#editarCita #terminarCita').attr('hidden',false);
    if (datos.estado_id == 2) {
      $('#editarCita #guardarCita').attr('hidden',true);
      $('#editarCita #terminarCita').attr('hidden',true);
      $('#editarCita #eliminarCita').attr('hidden',true);
      $('#editarCita #texto_comentario').attr('disabled',true);
      select.attr('disabled',true);
    } else {
      $('#editarCita #texto_comentario').attr('disabled',false);
      select.attr('disabled',false);
    }

  })
  .catch(error => console.error('Error al obtener datos del servidor:', error));
  $('#editarCita').modal('show');
};

const crearCita = (info, calendar) => {
  $('#crearCitaForm textarea').val('');
  $('#crearCitaForm select').val('');
  $('#crearCita #motivo').empty();

  let id_alumno = 1; // TODO:
  fetch('../obtenerDatosNuevaCita/' + id_alumno)  
  .then(response => {
    if (!response.ok) {
        throw new Error('Error al obtener los datos');
    }
    return response.json();
  })
  .then(data => {
    const datos = data.datos;
    $('#crearCita #nombre_alumno').val(datos.nombre);
    $('#crearCita #rut').val(datos.rut);
    let select = $('#crearCita #motivo');
    let emptyOption = $('<option></option>').attr('value', '').text("Seleccione una opción");
    select.append(emptyOption);
    datos.motivos.forEach(motivo => {
        let option = $('<option></option>').attr('value', motivo[0]).text(motivo[1]);
        select.append(option);
    });
  })
  .catch(error => console.error('Error al obtener datos del servidor:', error));

  let fecha = new Date(info.start);
  let fecha_fin = new Date(info.end)
  let fecha_formated = fecha.toISOString().split('T')[0];
  let hora_inicio_formated = ("0" + fecha.getHours()).slice(-2) + ":" + ("0" + fecha.getMinutes()).slice(-2) + ":" + ("0" + fecha.getSeconds()).slice(-2);
  let hora_fin_formated = ("0" + fecha_fin.getHours()).slice(-2) + ":" + ("0" + fecha_fin.getMinutes()).slice(-2) + ":" + ("0" + fecha_fin.getSeconds()).slice(-2);
  
  $('#crearCita #fecha_consulta').val(fecha_formated);
  $('#crearCita #hora_inicio_consulta').val(hora_inicio_formated);
  $('#crearCita #hora_termino_consulta').val(hora_fin_formated);
  $('#crearCita #id_alumno').val(id_alumno);
  $('#crearCita').modal('show');
}

$(document).ready(function(){

    $('#crearCitaForm').submit(function(event) {
      event.preventDefault();
      let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
      let form = new FormData();
      form.append('csrfmiddlewaretoken', csrfToken)

      let fecha_consulta = $('#crearCita #fecha_consulta').val();
      let hora_consulta_ini = $('#crearCita #hora_inicio_consulta').val();
      let hora_consulta_fin = $('#crearCita #hora_termino_consulta').val();
      let id_alumno = $('#crearCita #id_alumno').val();
      let textarea_crear = $('#crearCita #texto_comentario').val();
      let motivo = $('#crearCita #motivo').val();
      let alumno = $('#crearCita #nombre_alumno').val();


      $('#crearCita #motivo').prop('disabled', true);
      $('#crearCita #texto_comentario').prop('disabled', true);

      form.append('fecha_consulta', fecha_consulta);
      form.append('hora_consulta_ini', hora_consulta_ini);
      form.append('hora_consulta_fin', hora_consulta_fin);
      form.append('id_alumno', id_alumno);
      form.append('comentario', textarea_crear);
      form.append('motivo', motivo);

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
            url: '/postCita/',
            method: 'POST',
            data: form,
            processData: false,
            contentType: false,
            success: function(response) {
              let idEvento = response.id;
              Swal.fire({
                title: 'Éxito',
                text: 'La acción se realizó correctamente.',
                icon: 'success',
                confirmButtonText: 'Aceptar'
              }).then(function(){
                let nuevoEvento = {
                  id: idEvento,
                  title: alumno, 
                  start: fecha_consulta + 'T' + hora_consulta_ini,
                  end: fecha_consulta + 'T' + hora_consulta_fin
                };
                calendar.addEvent(nuevoEvento);
                $('#crearCita').modal('hide');
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
                  confirmButtonText: 'Aceptar'
              });
            }
          });
        }
        $('#crearCita #motivo').prop('disabled', false);
        $('#crearCita #texto_comentario').prop('disabled', false);
      });
    });

  $('#guardarCita').on('click', function(){
    let csrfToken = $('#editarCita input[name="csrfmiddlewaretoken"]').val();
    let form = new FormData();
    let texto_comentario = $('#editarCita #texto_comentario').val();
    let motivo = $('#editarCita #motivo').val();
    let id_cita = $('#editarCita #id_cita').val();

    form.append('csrfmiddlewaretoken', csrfToken)
    form.append('texto_comentario',texto_comentario);
    form.append('motivo', motivo);
    form.append('id_cita',id_cita)

    $('#editarCita #motivo').prop('disabled', true);
    $('#editarCita #texto_comentario').prop('disabled', true);
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
          url: '../postEditarCita/',
          method: 'POST',
          data: form,
          processData: false,
          contentType: false,
          success: function(response) {
            Swal.fire({
              title: 'Éxito',
              text: 'La acción se realizó correctamente.',
              icon: 'success',
              confirmButtonText: 'Aceptar'
            }).then(function(){

              $('#editarCita').modal('hide');
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
                confirmButtonText: 'Aceptar'
            });
          }
        });
      }
      $('#editarCita #motivo').prop('disabled', false);
      $('#editarCita #texto_comentario').prop('disabled', false);
    });
  });

  $('#eliminarCita').on('click', function(){
    let csrfToken = $('#editarCita input[name="csrfmiddlewaretoken"]').val();
    let form = new FormData();
    let id_cita = $('#editarCita #id_cita').val();

    form.append('csrfmiddlewaretoken', csrfToken)
    form.append('id_cita',id_cita)

    $('#editarCita #motivo').prop('disabled', true);
    $('#editarCita #texto_comentario').prop('disabled', true);
    $('#editarCita #guardarCita').prop('disabled', true);
    $('#editarCita #terminarCita').prop('disabled', true);
    Swal.fire({
      title: 'Confirmación',
      text: '¿Estás seguro de cancelar esta cita?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Confirmar acción',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          url: '../postEliminarCita/',
          method: 'POST',
          data: form,
          processData: false,
          contentType: false,
          success: function(response) {
            Swal.fire({
              title: 'Éxito',
              text: 'La cita se ha eliminado correctamente',
              icon: 'success',
              confirmButtonText: 'Aceptar'
            }).then(function(){
              $('#editarCita').modal('hide');
              let event = calendar.getEventById(id_cita);
              if(event){
                event.remove();
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
                confirmButtonText: 'Aceptar'
            });
          }
        });
      }
      $('#editarCita #motivo').prop('disabled', false);
      $('#editarCita #texto_comentario').prop('disabled', false);
      $('#editarCita #guardarCita').prop('disabled', false);
      $('#editarCita #terminarCita').prop('disabled', false);
    });
  });


  $('#terminarCita').on('click', function(){
    let csrfToken = $('#editarCita input[name="csrfmiddlewaretoken"]').val();
    let form = new FormData();
    let id_cita = $('#editarCita #id_cita').val();

    form.append('csrfmiddlewaretoken', csrfToken)
    form.append('id_cita',id_cita)

    $('#editarCita #motivo').prop('disabled', true);
    $('#editarCita #texto_comentario').prop('disabled', true);
    $('#editarCita #guardarCita').prop('disabled', true);
    $('#editarCita #terminarCita').prop('disabled', true);
    Swal.fire({
      title: 'Confirmación',
      text: '¿Estás seguro que desea terminar esta cita? , una vez terminada solo quedará el registro en el calendario',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Confirmar acción',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          url: '../postTerminarCita/',
          method: 'POST',
          data: form,
          processData: false,
          contentType: false,
          success: function(response) {
            Swal.fire({
              title: 'Éxito',
              text: 'La cita se ha finalizado correctamente',
              icon: 'success',
              confirmButtonText: 'Aceptar'
            }).then(function(){
              $('#editarCita').modal('hide');
              calendar.render();
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
                confirmButtonText: 'Aceptar'
            });
          }
        });
      }
      $('#editarCita #motivo').prop('disabled', false);
      $('#editarCita #texto_comentario').prop('disabled', false);
      $('#editarCita #guardarCita').prop('disabled', false);
      $('#editarCita #terminarCita').prop('disabled', false);
    });
  });

});

var calendar;
document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var externalEventsEl = document.getElementById('external-events');
  new FullCalendar.Draggable(externalEventsEl, {
    itemSelector: '.fc-event',
    eventData: function(eventEl) {
      return {
        title: eventEl.innerText.trim()
      };
    }
  });

  calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'timeGridWeek',
    locale: 'es',
    editable: true, 
    droppable: true,
    weekends: false, 
    firstDay: 1, 
    allDaySlot: false,
    slotMinTime: '08:00:00', 
    slotMaxTime: '21:00:00', 
    buttonText: {
      today: 'Hoy'
    },
    events: function(fetchInfo, successCallback, failureCallback) {
      $.ajax({
          url: '/getListadoCitas/', 
          method: 'GET',
          dataType: 'json',
          success: function(response) {
              var eventos = response.citas.map(function(cita) {
                  return {
                      id: cita.id,
                      title: cita.nombre,
                      start: cita.fecha_consulta + 'T' + cita.hora_inicio,
                      end: cita.fecha_consulta + 'T' + cita.hora_termino
                  };
              });
              successCallback(eventos);
          },
          error: function(xhr, status, error) {
              console.error('Error al obtener las citas:', error);
              failureCallback(error);
          }
      });
  },
    eventClick: function(info) {
      editarCita(info);
    },
    eventDrop: function(info) {

    },
    selectable: true, 
    select: function(arg) { 
      let events = calendar.getEvents();
      let canSelect = true;
      events.forEach(function(event) {
          if (arg.start >= event.start && arg.end < event.end) {
              canSelect = false;
              return;
          }
      });
      if (canSelect) {
          crearCita(arg, calendar);
      } 

      calendar.unselect(); // Desmarca la selección después de añadir el evento
      },
  });
  calendar.render();
});