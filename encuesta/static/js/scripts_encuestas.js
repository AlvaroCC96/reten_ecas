$(document).ready(function() {
    // Ocultar pregunta Trabaja
    let radiosPregunta6 = $('input[type="radio"][name="pregunta6"]');
    let formGroupPregunta7 = $('div.form-group[data-numero-pregunta="7"]');
    radiosPregunta6.on('change', function() {
        // Verificar si el radio "No" está seleccionado
        if (radiosPregunta6.filter(':checked').val() === "18") {
            formGroupPregunta7.hide(); // Ocultar form-group de la pregunta 7
            formGroupPregunta7.find('input, select, textarea').removeAttr('required');
        } else {
            formGroupPregunta7.show(); // Mostrar form-group de la pregunta 7
            formGroupPregunta7.find('input, select, textarea').attr('required', true);
        }
    });

    //Ocultar pregunta tiene hijos
    let radiosPregunta12 = $('input[type="radio"][name="pregunta12"]');
    let formGroupPregunta13 = $('div.form-group[data-numero-pregunta="13"]');
    let formGroupPregunta14 = $('div.form-group[data-numero-pregunta="14"]');
    radiosPregunta12.on('change', function() {
        // Verificar si el radio "No" está seleccionado
        if (radiosPregunta12.filter(':checked').val() === "47") {
            formGroupPregunta13.hide(); // Ocultar form-group de la pregunta 13
            formGroupPregunta14.hide(); // Ocultar form-group de la pregunta 14

            formGroupPregunta13.find('input, select, textarea').removeAttr('required');
            formGroupPregunta14.find('input, select, textarea').removeAttr('required');
        } else {
            formGroupPregunta13.show(); // Mostrar form-group de la pregunta 13
            formGroupPregunta14.show(); // Mostrar form-group de la pregunta 14

            formGroupPregunta13.find('input, select, textarea').attr('required', true);
            formGroupPregunta14.find('input, select, textarea').attr('required', true);
        }
    });

    //Ocultar pregunta Hay personas que dependan de usted o estén a su cuidado
    let radiosPregunta15 = $('input[type="radio"][name="pregunta15"]');
    let formGroupPregunta16 = $('div.form-group[data-numero-pregunta="16"]');
    radiosPregunta15.on('change', function() {
        // Verificar si el radio "No" está seleccionado
        if (radiosPregunta15.filter(':checked').val() === "59") {
            formGroupPregunta16.hide(); // Ocultar form-group de la pregunta 16
            formGroupPregunta16.find('input, select, textarea').removeAttr('required');
        } else {
            formGroupPregunta16.show(); // Mostrar form-group de la pregunta 16
            formGroupPregunta16.find('input, select, textarea').attr('required', true);
        }
    });

    //Ocultar pregunta Cuenta con conexión a internet en su hogar 
    let radiosPregunta20 = $('input[type="radio"][name="pregunta20"]');
    let formGroupPregunta21 = $('div.form-group[data-numero-pregunta="21"]');
    radiosPregunta20.on('change', function() {
        // Verificar si el radio "No" está seleccionado
        if (radiosPregunta20.filter(':checked').val() === "89") {
            formGroupPregunta21.hide(); // Ocultar form-group de la pregunta 21
            formGroupPregunta21.find('input, select, textarea').removeAttr('required');
        } else {
            formGroupPregunta21.show(); // Mostrar form-group de la pregunta 21
            formGroupPregunta21.find('input, select, textarea').attr('required', true);
        }
    });

    //Ocultar pregunta Cuenta con computador
    let radiosPregunta22 = $('input[type="radio"][name="pregunta22"]');
    let formGroupPregunta23 = $('div.form-group[data-numero-pregunta="23"]');
    radiosPregunta22.on('change', function() {
        // Verificar si el radio "No" está seleccionado
        if (radiosPregunta22.filter(':checked').val() === "94") {
            formGroupPregunta23.hide(); // Ocultar form-group de la pregunta 23
            formGroupPregunta23.find('input, select, textarea').removeAttr('required');
        } else {
            formGroupPregunta23.show(); // Mostrar form-group de la pregunta 23
            formGroupPregunta23.find('input, select, textarea').attr('required', true);
        }
    });

    //Ocultar pregunta  otras opciones de carrera
    let radiosPregunta33 = $('input[type="radio"][name="pregunta33"]');
    let formGroupPregunta34 = $('div.form-group[data-numero-pregunta="34"]');
    radiosPregunta33.on('change', function() {
        // Verificar si el radio "No" está seleccionado
        if (radiosPregunta33.filter(':checked').val() === "143") {
            formGroupPregunta34.hide(); // Ocultar form-group de la pregunta 34
            formGroupPregunta34.find('input, select, textarea').removeAttr('required');
        } else {
            formGroupPregunta34.show(); // Mostrar form-group de la pregunta 34
            formGroupPregunta34.find('input, select, textarea').attr('required', true);
        }
    });

    $('#form_entrevista').submit(function(event) {
        event.preventDefault();

        const formGroups = $(this).find('.form-group');
        const preguntas = {};
        formGroups.each(function() {

            const valorRespuesta = $(this).find('input[type="radio"]:checked, select, input[type="text"]').val();
            const numeroRespuesta= $(this).find('input[type="radio"]:checked, select, input[type="text"]').attr('name');

            const esRequerido = $(this).find('input[required], select[required], textarea[required]').length > 0;

            if (esRequerido) {
                preguntas[numeroRespuesta] = valorRespuesta;
            }
        });

        const preguntasJson = JSON.stringify(preguntas);
        const formData = new FormData();      
        formData.append('preguntas', preguntasJson);

        // Obtener el valor seleccionado del select
        const id_alumno = $('#id_alumno').val();
        formData.append('id_alumno', id_alumno);
        
        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        formData.append('csrfmiddlewaretoken', csrfToken);

        $.ajax({
            url: '/postEntrevista/',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false, 
            success: function(response) {
                Swal.fire({
                    title: '',
                    text: response.message,
                    icon: 'success',
                    timer: 3000,
                    allowOutsideClick: false,
                    showConfirmButton: false
                }).then(()=>{
                    document.getElementById('form_entrevista').reset();
                })
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

});