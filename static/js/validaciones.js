// Si se presiona el boton de tipo submit, se llama a validarFormulario
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('formDonacion').addEventListener('submit', validarFormulario);
});

// Función para validar el formulario
function validarFormulario(event) {

    let nombreDonante = document.getElementById('nombreDonante').value; //
    let emailDonante = document.getElementById('emailDonante').value; //
    let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; //
    let numeroCelular = document.getElementById('numeroCelular').value; //
    let region = document.getElementById('r').value; //
    let comuna = document.getElementById('c').value; //
    let nombreDispositivo = document.getElementById("nombreDispositivo").value; //
    let tipoDispositivo = document.getElementById("tipo").value; //
    let anosUso = document.getElementById("anosUso").value; //
    let estadoDispositivo = document.getElementById("estado").value; //
    let archivos = document.getElementById("fotos").files; //

    // Verificar que no haya ningun campo obligatorio vacio
    if (nombreDonante === '' || emailDonante === '' || numeroCelular === '' || region === '' || comuna === '' ||
        anosUso === ''|| nombreDispositivo === '' || tipoDispositivo === "" || estadoDispositivo === '') {
        msjError('Debes llenar todos los campos obligatorios.');
        return false;
    }

    // Validacion del nombre
    if (nombreDonante.length < 3 || nombreDonante.length > 80) {
        msjError('El nombre debe tener entre 3 y 80 caracteres.');
        return false;
    }

    // Validacion del email
    if (!emailRegex.test(emailDonante)) {
        //alert("El email no es válido.");
        msjError('El email no es válido.');
        return false;
    }

    // Validación del número de celular
    if (Number.isInteger(numeroCelular)) {
        msjError('El número de teléfono debe tener 9 digitos y ser un entero.');
        return false;
    }

    // Validación del nombre del dispositivo
    if (nombreDispositivo.length < 3) {
        msjError('El nombre del dispositivo debe tener más de 3 caracteres.');
        return false;
    }

    if (archivos.length < 1 || archivos.length > 3) {
        msjError('Debe subir entre 1 y 3 archivos .');
    }

    msjConfirmacion();
    return false;
}

// Si falla alguna validacion, se ejecuta esta función
function msjError(mensaje) {
    let alertDiv = document.getElementById('alert');
    let alertMessage = document.getElementById('alertMessage');

    alertMessage.textContent = mensaje;
    alertDiv.style.display = 'block';

    setTimeout(function () {
        alertDiv.style.display = 'none';
    }, 2000);
}

// Si todas las validaciones pasan, se ejecuta esta función
function msjConfirmacion() {
    let confirmationMessage = document.getElementById('confirmationMessage');
    confirmationMessage.style.display = 'block';
}

// Funcion en la que se oculta el msj de confirmacion y se muestra el msj de agradecimiento
function confirmar() {
    document.getElementById("confirmationMessage").style.display = "none";
    document.getElementById("thankYouMessage").style.display = "block";
}

// Funcion que oculta el msj de confirmacion
function volver() {
    let confirmationMessage = document.getElementById('confirmationMessage');
    confirmationMessage.style.display = 'none';
}

let dispositivoCount = 0;
function agregarOtroDispositivo() {
    dispositivoCount++; // Incrementa el contador para cada dispositivo agregado
    $("<section/>").insertBefore("[name='otroDisp']")
        .append(`
            <fieldset>
                <legend>Información del Dispositivo</legend>
                <label for="nombreDispositivo${dispositivoCount}">Nombre del dispositivo:</label>
                <input type="text" id="nombreDispositivo${dispositivoCount}" size="80" name="nombreDisp${dispositivoCount}">
                <br>
                <label for="descripcion${dispositivoCount}">Descripción:</label>
                <textarea id="descripcion${dispositivoCount}" rows="4" cols="50" placeholder="Agregar descripción..." name="descripcionDisp${dispositivoCount}"></textarea>
                <br>
                <label for="tipo${dispositivoCount}">Tipo:</label>
                <select id="tipo${dispositivoCount}" name="tipoDisp${dispositivoCount}">
                    <option value="">Seleccione un tipo</option>
                    <option value="pantalla">Pantalla</option>
                    <option value="notebook">Notebook</option>
                    <option value="tablet">Tablet</option>
                    <option value="celular">Celular</option>
                    <option value="consola">Consola</option>
                    <option value="mouse">Mouse</option>
                    <option value="teclado">Teclado</option>
                    <option value="impresora">Impresora</option>
                    <option value="parlante">Parlante</option>
                    <option value="audífonos">Audífonos</option>
                    <option value="otro">Otro</option>
                </select>
                <br>
                <label for="anosUso${dispositivoCount}">Años de uso:</label>
                <input type="number" id="anosUso${dispositivoCount}" min="1" max="99" name="anosDisp${dispositivoCount}">
                <br>
                <label for="estado${dispositivoCount}">Estado de funcionamiento:</label>
                <select id="estado${dispositivoCount}" name="estadoDisp${dispositivoCount}">
                    <option value="">Seleccione el estado</option>
                    <option value="funciona perfecto">Funciona perfecto</option>
                    <option value="funciona a medias">Funciona a medias</option>
                    <option value="no funciona">No funciona</option>
                </select>
                <br>
                <label for="fotos${dispositivoCount}">Fotos del producto:</label>
                <input type="file" id="fotos${dispositivoCount}" accept="image/*" name="fotosDisp${dispositivoCount}" multiple>
                <button type="button" onclick="eliminar(this)">Eliminar</button>
            </fieldset>
        `)
        .find("button")
        .attr("onclick", "eliminar(this)")
        .text("Eliminar");
}

function eliminar() { // todo: implementar la eliminacion de un dispositivo
    $(obj).closest("section").remove();
}

document.getElementById('region').addEventListener('change', function() {
    const selectedRegionId = this.value;

    // Obtener todas las opciones de comuna
    const comunas = document.querySelectorAll('#comuna option');

    if (selectedRegionId === "") {
        comunas.forEach(comuna => {
            comuna.style.display = 'none';
        })
    } else {
        comunas.forEach(comuna => {
            if (comuna.getAttribute('data-region') === selectedRegionId) {
                comuna.style.display = 'block'; // Mostrar la comuna
            } else {
                comuna.style.display = 'none'; // Ocultar la comuna
            }
        });
    }

    document.getElementById('comuna').value = '';
});
