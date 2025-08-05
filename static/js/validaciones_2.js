function validarComentario(event) {

    event.preventDefault();

    let nombreComentario = document.getElementById('nombreComentario').value;
    let textoComentario = document.getElementById('textoComentario').value;

    if (nombreComentario === '' || textoComentario === '') {
        msjError("Debes llenar el nombre y el comentario.")
        return false;
    }

    if (nombreComentario.length < 3 || nombreComentario.length > 80) {
        msjError("El nombre debe tener entre 3 y 80 caracteres.");
        return false;
    }

    if (textoComentario.length < 5) {
        msjError("El comentario debe tener más de 5 caracteres");
        return false;
    }
    confirmacion();
    return true;
}

// Función para mostrar un mensaje de error
function msjError(mensaje) {
    let alertDiv = document.getElementById('alert2');
    let alertMessage = document.getElementById('alertMessage2');

    alertMessage.textContent = mensaje;
    alertDiv.style.display = 'block';

    setTimeout(function () {
        alertDiv.style.display = 'none';
    }, 3000);
}

function confirmacion() {
    document.getElementById("msg").style.display = "block";
}


document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('formComentario').addEventListener('submit', validarComentario);
});

