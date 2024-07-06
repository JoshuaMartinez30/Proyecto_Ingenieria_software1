const toggleSidebar = () => document.body.classList.toggle("open");

// .............................
let currentSlide = 0;
const slides = document.querySelectorAll('.carousel-images img');
const totalSlides = slides.length;

const showSlide = (index) => {
    slides.forEach((slide, i) => {
        slide.style.display = (i === index) ? 'block' : 'none';
    });
};

const nextSlide = () => {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
};

// ......................
showSlide(currentSlide);

// tiempo de cmbio
setInterval(nextSlide, 3000);
