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

const registerForm = document.getElementById('register-form');
const errorNombre = document.getElementById('error-nombre');
const errorEmail = document.getElementById('error-email');
const errorPassword = document.getElementById('error-password');
const errorConfirmPassword = document.getElementById('error-confirm-password');
const modal = document.querySelector('.modal');
const closeModal = document.querySelector('.modal .close');


registerForm.addEventListener('submit', function(event) {
    let valido = true;

    const nombre = document.getElementById('nombre-registro').value;
    const email = document.getElementById('email-registro').value;
    const password = document.getElementById('password-registro').value;
    const confirmPassword = document.getElementById('confirm-password-registro').value;

    errorNombre.textContent = '*';
    errorEmail.textContent = '*';
    errorPassword.textContent = '*';
    errorConfirmPassword.textContent = '*';

    if (!nombre) {
        valido = false;
        errorNombre.style.color = 'red';
        errorNombre.textContent = '* Ingresa tu nombre.';
    } else {
        errorNombre.textContent = ''; 
    }

    if (!email || !email.includes('@')) {
        valido = false;
        errorEmail.style.color = 'red';
        errorEmail.textContent = '* Ingresa un email válido.';
    } else {
        errorEmail.textContent = ''; 
    }


    if (!password) {
        valido = false;
        errorPassword.style.color = 'red';
        errorPassword.textContent = '* Ingresa una contraseña.';
    } else if (password && password.length < 8) {
        valido = false;
        errorPassword.style.color = 'red';
        errorPassword.textContent = '* La contraseña debe tener al menos 8 caracteres.';   
    } else {
        errorPassword.textContent = '';
    }


    if (password !== confirmPassword) {
        valido = false;
        errorConfirmPassword.style.color = 'red';
        errorConfirmPassword.textContent = '* Las contraseñas no coinciden.';
    } else {
        errorConfirmPassword.textContent = ''; 
    }

    // ReCaptcha validacion
    const captcha = grecaptcha.getResponse();
    const errorRecaptcha = document.getElementById('error-recaptcha');

    if (!captcha) {
        valido = false;
        errorRecaptcha.style.color = 'red';
        errorRecaptcha.textContent = 'Por favor, completa el reCAPTCHA.';
    } else {
        errorRecaptcha.textContent = '';
    }

    if (nombre && email && password && confirmPassword && password === confirmPassword && captcha) {
        errorNombre.textContent = '';
        errorEmail.textContent = '';
        errorPassword.textContent = '';
        errorConfirmPassword.textContent = '';
        errorRecaptcha.textContent = '';
    }

    if (!valido) {
        event.preventDefault();
    } else {
        modal.style.display = 'block';
    }
});


closeModal.addEventListener('click', function() {
    modal.style.display = 'none';
});