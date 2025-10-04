document.addEventListener("DOMContentLoaded", function () {
    // Espera a que cargue TODO (imágenes, CSS, etc.)
    window.addEventListener("load", function () {
        document.getElementById("loader").style.display = "none";
    });

});


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

const menuPerfil = document.getElementById('menu-perfil');
const perfilLink = document.getElementById('perfil');

perfilLink.addEventListener('click', function() {
    if (menuPerfil.style.display === 'flex') {
        menuPerfil.style.display = 'none';
    } else {
        menuPerfil.style.display = 'flex';
    }
});

const botonMenuOculto = document.getElementById('boton-menu-oculto');
const menuOculto = document.getElementById('container-menu-oculto');
const cerrarMenuOculto = document.getElementById('cerrar-menu-oculto');
const iconoMenuOculto = document.getElementById('icono-menu-oculto');

botonMenuOculto.addEventListener('click', function(){
    const menuDisplay = window.getComputedStyle(menuOculto).display;
    if (menuDisplay === 'none') {
        menuOculto.style.display = 'block';
        cerrarMenuOculto.style.display = 'block';
        iconoMenuOculto.style.display = 'none';
    } else {
        menuOculto.style.display = 'none';
        cerrarMenuOculto.style.display = 'none';
        iconoMenuOculto.style.display = 'block';
    }
});



window.addEventListener('click', function(event) {
    if (!perfilLink.contains(event.target) && !menuPerfil.contains(event.target)) {
        menuPerfil.style.display = 'none';
    }
});

window.addEventListener('click', function(event) {
    if (!botonMenuOculto.contains(event.target) && !menuOculto.contains(event.target)) {
        menuOculto.style.display = 'none';
        cerrarMenuOculto.style.display = 'none';
        iconoMenuOculto.style.display = 'block';
    }
});
