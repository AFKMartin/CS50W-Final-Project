document.addEventListener("DOMContentLoaded", () => {

    // Description animations
    const conjectureEl = document.getElementById("conjecture");
    const rulesEl = document.getElementById("rules");
    const primeDescEl = document.getElementById("prime-desc");
    
    if (conjectureEl) conjectureEl.classList.add("show");
    if (rulesEl) rulesEl.classList.add("show");
    if (primeDescEl) primeDescEl.classList.add("show");

    // Zeta Function (real axis)
    const ctx = document.getElementById("zetaChart");
    const sMaxInput = document.getElementById("s-max");
    const updateBtn = document.getElementById("update-zeta");
    
    // Computes the Riemann zeta function ζ(s) for real s > 1
    function zetaReal(s, terms = 10000) {
        let sum = 0;
        for (let n = 1; n <= terms; n++) {
            sum += 1 / Math.pow(n, s);
        }
        return sum;
    }
    // Visualization on how ζ(s) behaves as s increases.
    function generateData(sMin = 1.1, sMax = 6, step = 0.1) {
        const labels = [];
        const values = [];
        for (let s = sMin; s <= sMax + 1e-9; s += step) {
            const rounded = parseFloat(s.toFixed(2));
            labels.push(rounded);
            values.push(zetaReal(rounded));
        }
        return { labels, values };
    }

    const initialMax = parseFloat(sMaxInput.value) || 6.0;
    const initialData = generateData(1.1, initialMax);

    const zetaChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: initialData.labels,
            datasets: [{
                label: "ζ(s) for real s > 1",
                data: initialData.values,
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                fill: true,
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true },
                tooltip: { mode: "index", intersect: false }
            },
            scales: {
                x: { title: { display: true, text: "s (real)" } },
                y: { title: { display: true, text: "ζ(s)" }, beginAtZero: false }
            }
        }
    });

    updateBtn.addEventListener("click", () => {
        let sMax = parseFloat(sMaxInput.value);
        if (isNaN(sMax) || sMax < 2 || sMax > 10) {
            sMax = 6.0;
            sMaxInput.value = sMax;
        }
        const newData = generateData(1.1, sMax);
        zetaChart.data.labels = newData.labels;
        zetaChart.data.datasets[0].data = newData.values;
        zetaChart.update();
    });

    // Prime counting vs Riemann
    // First 200 non-trivial zeros of ζ(s) - imaginary parts
    const zetaZeros = [
        14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588,
        37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478,
        52.970321478, 56.446247697, 59.347044003, 60.831778525, 65.112544048,
        67.079810529, 69.546401711, 72.067157674, 75.704690699, 77.144840069,
        79.337375020, 82.910380854, 84.735492981, 87.425274613, 88.809111208,
        92.491899271, 94.651344041, 95.870634228, 98.831194218, 101.317851006,
        103.725538040, 105.446623052, 107.168611184, 111.029535543, 111.874659177,
        114.320220915, 116.226680321, 118.790782866, 121.370125002, 122.946829294,
        124.256818554, 127.516683880, 129.578704200, 131.087688531, 133.497737203,
        134.756509753, 138.116042055, 139.736208952, 141.123707404, 143.111845808,
        146.000982487, 147.422765343, 150.053520421, 150.925257612, 153.024693811,
        156.112909294, 157.597591818, 158.849988171, 161.188964138, 163.030709687,
        165.537069188, 167.184439978, 169.094515416, 169.911976479, 173.411536520,
        174.754191523, 176.441434298, 178.377407776, 179.916484020, 182.207078484,
        184.874467848, 185.598783678, 187.228922584, 189.416158656, 192.026656361,
        193.079726604, 195.265396680, 196.876481841, 198.015309676, 201.264751944,
        202.493594514, 204.189671803, 205.394697202, 207.906258888, 209.576509717,
        211.690862595, 213.347919360, 214.547044783, 216.169538508, 219.067596349,
        220.714918839, 221.430705555, 224.007000985, 224.983324670, 227.421444280,
        229.337413306, 231.250188700, 231.987235253, 233.693404179, 236.524229666,
        237.769868387, 239.555200202, 241.049298105, 242.893744672, 244.070897484,
        247.056667036, 248.074229672, 249.827525076, 251.014403687, 254.017670388,
        254.639877232, 256.446108785, 257.773315929, 260.044741428, 261.256175637,
        262.886890319, 265.575468538, 266.533427684, 267.883167199, 269.379666161,
        271.072293494, 273.046547926, 274.387748381, 275.571592752, 277.375766589,
        279.229875980, 280.799640181, 282.455267563, 283.313147889, 285.781207808,
        286.690302903, 289.034844804, 290.146213281, 290.912132825, 292.963492422,
        294.670654126, 295.489293976, 297.559654998, 298.996772235, 300.181911153,
        302.064462890, 303.734921050, 304.719867155, 306.247326432, 307.268268075,
        309.716985959, 311.231476695, 312.656169892, 313.467421034, 315.968549777,
        317.126060485, 318.992952453, 319.948190137, 321.954515878, 322.857547955,
        324.681993127, 326.023418481, 327.586265673, 328.846301928, 330.291161689,
        332.055458730, 333.139764398, 334.893289508, 336.378817594, 337.329482632,
        339.223497155, 340.695544037, 341.875943752, 343.248881834, 344.185962111,
        346.397262806, 347.361978569, 349.076215563, 350.045605497, 351.988120502,
        353.052943579, 354.536710624, 355.835563867, 357.008154903, 358.485337756,
        360.045396106, 361.123188555, 362.588423060, 363.512343555, 365.283951269,
        366.346207422, 367.857936702, 368.701699183, 370.627621890, 371.649691179,
        372.859031217, 374.171056028, 375.433234292, 376.577598816, 377.884705916,
        379.024311454, 380.507909375
    ];

    // Prime checker helper
    function isPrime(n) {
        if (n < 2) return false;
        for (let i = 2; i * i <= n; i++) {
            if (n % i === 0) return false;
        }
        return true;
    }
    // PI(x)
    function primeCount(x) {
        let count = 0;
        for (let i = 2; i <= x; i++) {
            if (isPrime(i)) count++;
        }
        return count;
    }
    // Li(x)
    function li(x) {
        if (x < 2) return 0;
        const steps = 8000;
        const dx = (x - 2) / steps;
        let sum = 0;
        for (let i = 0; i < steps; i++) {
            const t = 2 + i * dx;
            sum += dx / Math.log(t);
        }
        return sum;
    }

    // Mobius function
    function mobius(n) {
        if (n === 1) return 1;
        let factors = 0;
        let temp = n;
        
        for (let i = 2; i * i <= temp; i++) {
            if (temp % i === 0) {
                factors++;
                temp /= i;
                if (temp % i === 0) return 0; // squared factor
            }
        }
        if (temp > 1) factors++;
        
        return factors % 2 === 0 ? 1 : -1;
    }

    // Riemann R function
    function riemannR(x, numTerms = 20) {
        let sum = 0;
        for (let n = 1; n <= numTerms; n++) {
            const mu = mobius(n);
            const term = li(Math.pow(x, 1/n));
            sum += (mu / n) * term;
        }
        return sum;
    }

    // Riemann explicit formula approximation (simplified oscillatory)
    function riemannApprox(x, k) {
        if (x < 2) return 0;
        
        // Start with Riemann R function (includes prime powers with Mobius weighting)
        let result = riemannR(x);
        
        if (k === 0) return result;
        
        // Using a damped oscillation formula
        const logX = Math.log(x);
        
        for (let n = 0; n < k && n < zetaZeros.length; n++) {
            const gamma = zetaZeros[n];
            
            // Oscillatory correction term each pair of conjugate zeros contributes an oscillation
            const amplitude = Math.sqrt(x) / (gamma * logX);
            const phase = gamma * logX;
            const correction = amplitude * Math.sin(phase);
            
            result -= 2 * correction;
        }
        
        return result;
    }

    const primeBtn = document.getElementById("update-primes");
    const primeXInput = document.getElementById("prime-x");
    const zeroCountInput = document.getElementById("zero-count");

    if (!primeBtn) {
        console.error("Button 'update-primes' not found!");
        return;
    }

    primeBtn.addEventListener("click", () => {
        const x = parseInt(primeXInput.value);
        let k = parseInt(zeroCountInput.value);
        
        // Validate and limit k to availablezeros
        if (k > zetaZeros.length) {
            k = zetaZeros.length;
            zeroCountInput.value = k;
        }

        const labels = [];
        const realPrimes = [];
        const liValues = [];
        const rhValues = [];

        for (let n = 2; n <= x; n++) {
            labels.push(n);
            realPrimes.push(primeCount(n));
            liValues.push(li(n));
            rhValues.push(riemannApprox(n, k));
        }

        if (window.primeChart && typeof window.primeChart.destroy === "function") {
            window.primeChart.destroy();
        }

        const ctx2 = document.getElementById("primeChart");
        window.primeChart = new Chart(ctx2, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "π(x) — Actual primes",
                        data: realPrimes,
                        borderColor: "rgba(255, 99, 132, 1)",
                        tension: 0.1,
                        pointRadius: 0
                    },
                    {
                        label: "Li(x) — Classical approximation",
                        data: liValues,
                        borderColor: "rgba(54, 162, 235, 1)",
                        borderDash: [5, 5],
                        tension: 0.1,
                        pointRadius: 0
                    },
                    {
                        label: `R(x) — Using ${k} zeros`,
                        data: rhValues,
                        borderColor: "rgba(75, 192, 75, 1)",
                        tension: 0.1,
                        pointRadius: 0
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: true } },
                scales: { y: { beginAtZero: false } }
            }
        });

        // Summary 
        const actualPrimes = realPrimes[realPrimes.length - 1];
        const liApprox = liValues[liValues.length - 1];
        const rhApprox = rhValues[rhValues.length - 1];

        document.getElementById("summary-x").textContent = x;
        document.getElementById("summary-actual").textContent = actualPrimes;
        document.getElementById("summary-li").textContent = liApprox.toFixed(2);
        document.getElementById("summary-zeros").textContent = k;
        document.getElementById("summary-rh").textContent = rhApprox.toFixed(2);
        document.getElementById("prime-summary").style.display = "block";
        document.getElementById("error-li").textContent = (liApprox - actualPrimes).toFixed(2);
        document.getElementById("error-rh").textContent = (rhApprox - actualPrimes).toFixed(2);
    });

});