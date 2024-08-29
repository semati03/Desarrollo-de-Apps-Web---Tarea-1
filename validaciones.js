function validarFormulario() {
    // Validación del nombre
    let nombreDonante = document.getElementById("nombreDonante").value;
    if (nombreDonante.length < 3 || nombreDonante.length > 80) {
        alert("El nombre debe tener entre 3 y 80 caracteres.");
        return false;
    }

    // Validación del email
    let emailDonante = document.getElementById("emailDonante").value;
    let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailDonante)) {
        alert("El email no es válido.");
        return false;
    }

    // Validación del número de celular
    let numeroCelular = document.getElementById("numeroCelular").value;
    if (numeroCelular.length != 9) {
        alert("El número de teléfono debe tener 9 dígitos.");
        return false;
    }

    // Validación del nombre del dispositivo
    let nombreDispositivo = document.getElementById("nombreDispositivo").value;
    if (nombreDispositivo.length < 3) {
        alert("El nombre del dispositivo debe tener más de 3 caracteres.");
        return false;
    }

    // Validación de que años de uso sea un número entero
    let anosUso = document.getElementById("anosUso").value;
    anosUso = parseInt(anosUso);
    if (!Number.isInteger(anosUso)) {
        alert("El campo 'Años de uso' debe ser un número entero.");
        return false;
    }

    // Validación de que años de uso esté entre 1 y 99
    if (anosUso < 1 || anosUso > 99) {
        alert("El campo 'Años de uso' debe estar entre 1 y 99.");
        return false;
    }

    // Validación de que haya entre 1 y 3 archivos
    let archivos = document.getElementById("fotos").files;
    if (archivos.length < 1 || archivos.length > 3) {
        alert("Debe subir entre 1 y 3 fotos del producto.");
        return false;
    }

    // Mostrar mensaje de confirmación
    document.getElementById("formDonacion").style.display = "none";
    document.getElementById("confirmationMessage").style.display = "block";
    return false; // Prevenir el envío del formulario hasta la confirmación
}

function confirmar() {
    document.getElementById("confirmationMessage").style.display = "none";
    document.getElementById("thankYouMessage").style.display = "block";
    // Simula el envío del formulario, aquí podrías enviar los datos con fetch o similar
}

function volver() {
    document.getElementById("formDonacion").style.display = "block";
    document.getElementById("confirmationMessage").style.display = "none";
}

function agregarOtroDispositivo() {
    // Implementa aquí la lógica para agregar más dispositivos
}


document.addEventListener('DOMContentLoaded', function () {
    const regionSelect = document.getElementById('region');
    const comunaSelect = document.getElementById('comuna');

    const comunas = {
        'arica-parinacota': [
            { value: 'arica', text: 'Arica' },
            { value: 'camarones', text: 'Camarones' },
            { value: 'general-laguna', text: 'General Lagos' },
            { value: 'putre', text: 'Putre' }
        ],
        'tarapaca': [
            { value: 'alto-hospicio', text: 'Alto Hospicio' },
            { value: 'camiña', text: 'Camiña' },
            { value: 'huara', text: 'Huara' },
            { value: 'colchane', text: 'Colchane' },
            { value: 'iquique', text: 'Iquique' },
            { value: 'pica', text: 'Pica' },
            { value: 'pozo-almonte', text: 'Pozo Almonte' }
        ],
        'antofagasta': [
            { value: 'antofagasta', text: 'Antofagasta' },
            { value: 'mejillones', text: 'Mejillones' },
            { value: 'sierra-gorda', text: 'Sierra Gorda' },
            { value: 'taltal', text: 'Taltal' },
            { value: 'calama', text: 'Calama' },
            { value: 'san-pedro-de-atacama', text: 'San Pedro de Atacama' }
        ],
        'atacama': [
            { value: 'alto-del-carmen', text: 'Alto del Carmen' },
            { value: 'caldera', text: 'Caldera' },
            { value: 'chañaral', text: 'Chañaral' },
            { value: 'copiapó', text: 'Copiapó' },
            { value: 'diego-de-almagro', text: 'Diego de almagro' },
            { value: 'freirina', text: 'Freirina' }
        ],

        'coquimbo': [
            { value: 'andacollo', text: 'Andacollo' },
            { value: 'canela', text: 'Canela' },
            { value: 'combarbalá', text: 'Combarbala' },
            { value: 'coquimbo', text: 'Coquimbo' },
            { value: 'illapel', text: 'Illapel' },
            { value: 'la-serena', text: 'La serena' }
        ],

        'valparaiso': [
            { value: 'algarrobo', text: 'Algarrobo' },
            { value: 'cabildo', text: 'Cabildo' },
            { value: 'calle-larga', text: 'Calle Larga' },
            { value: 'cartagena', text: 'Cartagena' },
            { value: 'casablanca', text: 'Casablanca' },
            { value: 'catemu', text: 'Catemu' }
        ],

        'metropolitana': [
            { value: 'santiago', text: 'Santiago' },
            { value: 'la-florida', text: 'La Florida' },
            { value: 'las-condes', text: 'Las Condes' },
            { value: 'maipú', text: 'Maipú' },
            { value: 'providencia', text: 'Providencia' }
        ],

        'ohiggins': [
            { value: 'chépica', text: 'Chépica' },
            { value: 'chimbarongo', text: 'Chimbarongo' },
            { value: 'coinco', text: 'Coinco' },
            { value: 'doñihue', text: 'Doñihue' },
            { value: 'coltauco', text: 'Coltauco' }
        ],

        'maule': [
            { value: 'cauquenes', text: 'Cauquenes' },
            { value: 'chanco', text: 'Chanco' },
            { value: 'colbún', text: 'Colbún' },
            { value: 'constitución', text: 'Constitución' },
            { value: 'curepto', text: 'Curepto' }
        ],

        'ñuble': [
            { value: 'bulnes', text: 'Bulnes' },
            { value: 'chillán', text: 'Chillán' },
            { value: 'chillan-viejo', text: 'Chillán Viejo' },
            { value: 'cobquecura', text: 'Cobquecura' },
            { value: 'coelemu', text: 'Coelemu' }
        ],

        'biobio': [
            { value: 'alto-biobío', text: 'Alto Biobío' },
            { value: 'antuco', text: 'Antuco' },
            { value: 'arauco', text: 'Arauco' },
            { value: 'cabrero', text: 'Cabrero' },
            { value: 'cañete', text: 'Cañete' }
        ],

        'araucania': [
            { value: 'angol', text: 'Angol' },
            { value: 'carahue', text: 'Carahue' },
            { value: 'cholchol', text: 'Cholchol' },
            { value: 'cullipulli', text: 'Cullipulli' },
            { value: 'cunco', text: 'Cunco' }
        ],

        'los-rios': [
            { value: 'corral', text: 'Corral' },
            { value: 'futrono', text: 'Futrono' },
            { value: 'lago-ranco', text: 'Lago Ranco' },
            { value: 'lanco', text: 'Lanco' },
            { value: 'la-unión', text: 'La Unión' }
        ],

        'los-lagos': [
            { value: 'ancud', text: 'Ancud' },
            { value: 'calbuco', text: 'Calbuco' },
            { value: 'castro', text: 'Castro' },
            { value: 'chaitén', text: 'Chaiten' },
            { value: 'osorno', text: 'Osorno' }
        ],

        'aysén': [
            { value: 'aysén', text: 'Aysén' },
            { value: 'chile-chico', text: 'Chile Chico' },
            { value: 'cisnes', text: 'Cisnes' },
            { value: 'cochrane', text: 'Cochrane' },
            { value: 'coyhaique', text: 'Coyhaique' },
        ],

        'magallanes': [
            { value: 'antártica', text: 'Antártica' },
            { value: 'cabo-de-hornos', text: 'Cabo de Hornos' },
            { value: 'laguna-blanca', text: 'Laguna Blanca' },
            { value: 'natales', text: 'Natales' },
            { value: 'porvenir', text: 'Porvenir' },
        ]
    };

    function updateComunass() {
        const selectedRegion = regionSelect.value;
        const comunasForRegion = comunas[selectedRegion] || [];
        
        // Limpiar las opciones actuales de la comuna
        comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
        
        // Agregar las nuevas opciones de comuna
        comunasForRegion.forEach(comuna => {
            const option = document.createElement('option');
            option.value = comuna.value;
            option.textContent = comuna.text;
            comunaSelect.appendChild(option);
        });
    }

    regionSelect.addEventListener('change', updateComunass);
});
