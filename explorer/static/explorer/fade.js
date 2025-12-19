// Descriptions animation
window.onload = () => {
    setTimeout(() => {
        document.getElementById("conjecture").classList.add("show");
    }, 500);

    setTimeout(() => {
        document.getElementById("rules").classList.add("show");
    }, 1500);
};

let numbers = []
let currentIndex = 0;
let startTime, timerInterval;