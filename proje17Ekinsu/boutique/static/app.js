window.sr = ScrollReveal();

sr.reveal('.anime-left', {
    origin: 'left',
    duration: 1000,
    distance: '25rem',
    delay: 300
});
sr.reveal('.anime-right', {
    origin: 'right',
    duration: 1000,
    distance: '25rem',
    delay: 600
});
sr.reveal('.anime-top', {
    origin: 'top',
    duration: 1000,
    distance: '25rem',
    delay: 600
});
sr.reveal('.anime-bottom', {
    origin: 'bottom',
    duration: 1000,
    distance: '25rem',
    delay: 600
});


ScrollReveal().reveal('.ani1', { delay: 250 });
ScrollReveal().reveal('.ani2', { delay: 500 });
ScrollReveal().reveal('.ani3', { delay: 750 });

var menuItems = document.getElementById('menuItems');
menuItems.style.maxHeight = "0px";

function menuToggle() {
    if (menuItems.style.maxHeight == "0px") {
        menuItems.style.maxHeight = "200px";
    } else {
        menuItems.style.maxHeight = "0px";
    }
}