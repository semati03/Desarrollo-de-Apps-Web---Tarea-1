function validarComentario() {
    // Validación del nombre
    let nombreComentario = document.getElementById('nombreComentario');
    if (nombreComentario.length < 3 && nombreComentario.length > 80) {
        alert("El nombre debe tener entre 3 y 80 caracteres.");
        return false;
    }

}
