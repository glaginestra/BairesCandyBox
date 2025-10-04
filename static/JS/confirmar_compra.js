document.addEventListener("DOMContentLoaded", function () {
    // Espera a que cargue TODO (imágenes, CSS, etc.)

    window.addEventListener("load", function () {
        document.getElementById("loader").style.display = "none";
    });

    const otraPersonaCheckbox = document.getElementById('otra-persona');
    const inputsRetira = document.getElementById('container-retira');
    const nombreRetiraInput = document.getElementById("nombre-compra-retira");
    const apellidoRetiraInput = document.getElementById("apellido-compra-retira");

    otraPersonaCheckbox.addEventListener("change", function() {
        if (otraPersonaCheckbox.checked) {
            inputsRetira.style.display = 'flex';
            nombreRetiraInput.style.border = '0.125em solid #ccc';
            apellidoRetiraInput.style.border = '0.125em solid #ccc';
        } else {
            inputsRetira.style.display = 'none';
        }
    });

    const sinNumeroCheckbox = document.getElementById('sin-nro');
    const inputNumeroCalle = document.getElementById('numero-calle-compra');

    sinNumeroCheckbox.addEventListener('change', function () {
        if (sinNumeroCheckbox.checked) {
            inputNumeroCalle.value = 'Sin número';
            inputNumeroCalle.disabled=true;
        } else{
            inputNumeroCalle.value = '';
        }
    });

    const formularioComprar = document.getElementById("formulario-comprar");

    formularioComprar.addEventListener('submit', function(event){
        let valido = true
        const emailCompraInput = document.getElementById("email-compra");
        const emailCompra = emailCompraInput.value;
        const nombreCompraInput = document.getElementById("nombre-compra");
        const nombreCompra = nombreCompraInput.value; 
        const apellidoCompraInput = document.getElementById("apellido-compra");
        const apellidoCompra = apellidoCompraInput.value;
        const telefonoCompraInput = document.getElementById("telefono-compra");
        const telefonoCompra = telefonoCompraInput.value;
        const regexTelefono = /^\+?\d{7,15}$/;
        const postalCompraInput = document.getElementById("postal-compra");
        const postalCompra = postalCompraInput.value;
        const checkboxCompra = document.getElementById("otra-persona").checked;
        const nombreRetiroCompraInput = document.getElementById("nombre-compra-retira");
        const nombreRetiroCompra = nombreRetiroCompraInput.value;
        const apellidoRetiroCompraInput = document.getElementById("apellido-compra-retira");
        const apellidoRetiroCompra = apellidoRetiroCompraInput.value;
        const ciudadCompraInput = document.getElementById("ciudad-compra");
        const ciudadCompra = ciudadCompraInput.value;
        const barrioCompraInput = document.getElementById("barrio-compra");
        const barrioCompra = barrioCompraInput.value;
        const calleCompraInput = document.getElementById("calle-compra");
        const calleCompra = calleCompraInput.value;
        const numeroCalleCompraInput = document.getElementById("numero-calle-compra");
        const numeroCalleCompra = numeroCalleCompraInput.value;

        if (!emailCompra || !emailCompra.includes('@')) {
            valido=false
            emailCompraInput.style.border = '0.125em solid red';
        } else {
            emailCompraInput.style.border = '0.125em solid #ccc';
        }

        if (!nombreCompra) {
            valido=false
            nombreCompraInput.style.border = '0.125em solid red';
        } else {
            nombreCompraInput.style.border = '0.125em solid #ccc';
        }

        if (!apellidoCompra) {
            valido=false
            apellidoCompraInput.style.border = '0.125em solid red';
        } else {
            apellidoCompraInput.style.border = '0.125em solid #ccc';
        }

        if (!regexTelefono.test(telefonoCompra)) {
            valido=false
            telefonoCompraInput.style.border = '0.125em solid red';
        } else {
            telefonoCompraInput.style.border = '0.125em solid #ccc';
        }

        if (!postalCompra || postalCompra.length > 4) {
            valido=false
            postalCompraInput.style.border = '0.125em solid red';
        } else {
            postalCompraInput.style.border = '0.125em solid #ccc';
        }

        if (checkboxCompra) {
            if (!nombreRetiroCompra) {
                valido=false
                nombreRetiroCompraInput.style.border = '0.125em solid red';
            } else {
                nombreRetiroCompraInput.style.border = '0.125em solid #ccc';
            }
            if (!apellidoRetiroCompra) {
                valido=false
                apellidoRetiroCompraInput.style.border = '0.125em solid red';
            } else {
                apellidoRetiroCompraInput.style.border = '0.125em solid #ccc';
            }
        } else{
            nombreRetiroCompraInput.style.border = '0.125em solid #ccc';
            apellidoRetiroCompraInput.style.border = '0.125em solid #ccc';

        }
        
        if (!ciudadCompra) {
            valido=false
            ciudadCompraInput.style.border = '0.125em solid red';
        } else {
            ciudadCompraInput.style.border = '0.125em solid #ccc';
        }

        if (!barrioCompra) {
            valido=false
            barrioCompraInput.style.border = '0.125em solid red';
        } else {
            barrioCompraInput.style.border = '0.125em solid #ccc';
        }

        if (!calleCompra) {
            valido=false
            calleCompraInput.style.border = '0.125em solid red';
        } else {
            calleCompraInput.style.border = '0.125em solid #ccc';
        }

        if (!numeroCalleCompra) {
            valido=false
            numeroCalleCompraInput.style.border = '0.125em solid red';
        } else {
            numeroCalleCompraInput.style.border = '0.125em solid #ccc';
        }


        if (!valido) {
            event.preventDefault();
        }
    });

});