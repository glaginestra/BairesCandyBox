const menuProductos = document.getElementById('menu-productos');
const productosLink = document.getElementById('productos');

productosLink.addEventListener('click', function() {
    if (menuProductos.style.display === 'flex') {
        menuProductos.style.display = 'none';
    } else {
        menuProductos.style.display = 'flex';
    }
});

window.addEventListener('click', function(event) {
    if (!productosLink.contains(event.target) && !menuProductos.contains(event.target)) {
        menuProductos.style.display = 'none';
    }
});

// Additional code for login.js

const loginForm = document.getElementById('login-form');

loginForm.addEventListener('submit', function(event) {
    let valido = true;

    const email = document.getElementById('email-login').value;
    const password = document.getElementById('password-login').value;
    const errorMensaje = document.getElementById('error-alert');

    errorMensaje.textContent = ''; 


    if (!email && !password) {
        valido = false;
        errorMensaje.style.color = 'red';
        errorMensaje.textContent = 'Por favor, completa todos los campos.';
    } else if (!email.includes('@')) {
        valido = false;
        errorMensaje.style.color = 'red';
        errorMensaje.textContent = 'Por favor, ingresa un email válido.';
    } else if (!password) {
        valido = false;
        errorMensaje.style.color = 'red';
        errorMensaje.textContent = 'Por favor, ingresa tu contraseña.';
    }




    if(!valido){
        event.preventDefault();
    }
    
});