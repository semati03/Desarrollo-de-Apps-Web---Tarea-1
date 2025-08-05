function validarComentario() {

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


document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('formComentario').addEventListener('submit', validarComentario);
});

