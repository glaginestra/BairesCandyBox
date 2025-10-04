// Inicialización de Swiper
const swiper = new Swiper(".mySwiper", {
loop: true, // carrusel infinito
autoplay: {
    delay: 3000, // tiempo entre slides
    disableOnInteraction: false,
},
pagination: {
    el: ".swiper-pagination",
    clickable: true,
},
navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
},
});