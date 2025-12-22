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

// Generate even numbers between 10 and 300
function generateEvenNumbers() {
    numbers = [];
    while(numbers.length < 10){
        let n = Math.floor(Math.random() * (300-10+1)) + 10;
        if (n % 2 === 0 && n > 2) numbers.push(n);
    }
}

// Start the game
function startGame() {
    generateEvenNumbers();
    currentIndex = 0;
    document.getElementById("gameArea").classList.remove("d-none");
    document.getElementById("startBtn").classList.add("d-none");
    startTime = Date.now();
    timerInterval = setInterval(updateTimer, 1000);
    showNumber();
}

function showNumber() {
    document.getElementById("currentNumber").innerText = "Find two primes that sum to: " + numbers[currentIndex];
    document.getElementById("feedback").innerText = "";
    document.getElementById("prime1").value = "";
    document.getElementById("prime2").value = "";
    document.getElementById("progress").innerText = (currentIndex + 1) + " / " + numbers.length;
}

function updateTimer() {
    let elapsed = Math.floor((Date.now() - startTime) / 1000);
    document.getElementById("timer").innerText = "Time: " + elapsed + "s";
}

// Prime checker
function isPrime(num) {
    if (num < 2) return false;
    for (let i = 2; i <= Math.sqrt(num); i++) {
        if (num % i === 0) return false;
    }
    return true;
}

document.getElementById("startBtn").addEventListener("click", startGame);

document.getElementById("primeForm").addEventListener("submit", function(e){
    e.preventDefault();
    let p1 = parseInt(document.getElementById("prime1").value);
    let p2 = parseInt(document.getElementById("prime2").value);
    let target = numbers[currentIndex];

    if (isPrime(p1) && isPrime(p2) && p1 + p2 === target) {
      document.getElementById("feedback").innerText = "Correct!";
      currentIndex++;
      if (currentIndex < numbers.length) {
        setTimeout(showNumber, 1000);
      } else {
        clearInterval(timerInterval);
        let finalTime = Math.floor((Date.now() - startTime) / 1000);
        document.getElementById("gameArea").classList.add("d-none");
        document.getElementById("resultArea").classList.remove("d-none");
        document.getElementById("finalScore").innerText = finalTime;
        saveGoldbachTime(finalTime); // Save the value
      }
    } else {
      document.getElementById("feedback").innerText = "Try again!";
    }
});

// Best time Django sender
function saveGoldbachTime(time) {
    fetch("/goldbach/save-time/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
        },
        body: "time=" + time
    });
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
