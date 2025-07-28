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