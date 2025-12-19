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

// Collatz visualization.
// This script created the visualization of the collatz conjeture game using mountain and spiral charts (mountain looks better for low steps and spiral looks better for high steps).
// Equivalent to pythons if __name__ == "__main__" fix the issue where this script has to wait for the html to load.
window.addEventListener("DOMContentLoaded", () => {
  const dataScript = document.getElementById("collatz-data");
  if (!dataScript) return;

  const sequence = JSON.parse(dataScript.textContent);

  // Draw visualizations
  drawMountainChart(sequence);
  drawSpiralChart(sequence);
  
  // Find the tabs in the HTML
  document.querySelectorAll('button[data-bs-toggle="tab"]').forEach(tab => {
    tab.addEventListener('shown.bs.tab', () => {
        const target = tab.getAttribute('data-bs-target');
        // Mountain tab redraw
        if (target === '#mountain') drawMountainChart(sequence);
        // Spiral tab redraw
        if (target === '#spiral') drawSpiralChart(sequence);
    });
  });
});

// MountainChart
function drawMountainChart(sequence){
    const canvas = document.getElementById('mountainChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const padding = 40;

    ctx.clearRect(0, 0, width, height);

    const maxVal = Math.max(...sequence);
    const xStep = (width - 2 * padding) / (sequence.length - 1);
    const yScale = (height - 2 * padding) / maxVal;

    // Gradient
    const gradient = ctx.createLinearGradient(0, padding, 0, height - padding);
    gradient.addColorStop(0, 'rgba(13, 110, 253, 0.8)');
    gradient.addColorStop(1, 'rgba(13, 110, 253, 0.1)');

    // Area Drawing
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.moveTo(padding, height - padding);
    
    sequence.forEach((val, i) => {
        const x = padding + i * xStep;
        const y = height - padding - val * yScale;
        ctx.lineTo(x, y);
    });
    
    ctx.lineTo(width - padding, height - padding);
    ctx.closePath();
    ctx.fill();

    ctx.strokeStyle = '#0d6efd';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    sequence.forEach((val, i) => {
        const x = padding + i * xStep;
        const y = height - padding - val * yScale;
        
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    
    ctx.stroke();

    // Text stuff
    ctx.font = '10px sans-serif';
    ctx.textAlign = 'center';

    const labelInterval = Math.max(1, Math.floor(sequence.length / 15));
    const maxIndex = sequence.indexOf(maxVal);

    sequence.forEach((val,i) => {
        const shouldLabel = i === 0 || i === sequence.length - 1 || i === maxIndex || i % labelInterval === 0;
        
        if(shouldLabel) {
            const x = padding + i * xStep;
            const y = height - padding - val * yScale;

            // Background
            ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
            const text = val.toLocaleString();
            const metrics = ctx.measureText(text);
            ctx.fillRect(x - metrics.width/2 - 3, y - 18, metrics.width + 6, 16);

            // Text
            ctx.fillStyle = '#333';
            ctx.fillText(text, x, y - 8);

            // Dots
            ctx.fillStyle = '#0d6efd';
            ctx.beginPath();
            ctx.arc(x, y, 3, 0, 2 * Math.PI);
            ctx.fill();
        }
    });
}

// SpiralChart
function drawSpiralChart(sequence){
    const canvas = document.getElementById('spiralChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    ctx.clearRect(0, 0, width, height);
    
    const centerX = width / 2;
    const centerY = height / 2;
    const maxRadius = Math.min(width, height) / 2 - 40;
    
    const angleStep = (2 * Math.PI) / 50;
    let angle = 0;
    let radius = 10;
    const radiusStep = maxRadius / sequence.length;
    
    const maxVal = Math.max(...sequence);
    
    ctx.lineWidth = 2;
    ctx.beginPath(); 

    sequence.forEach((val, i) => {
        const hue = (val / maxVal) * 240;
        ctx.strokeStyle = `hsl(${240 - hue}, 70%, 50%)`;
        
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;
        
        if (i === 0) {
        ctx.moveTo(x, y);
        } else {
        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y);
        }
        
        // Node drwing
        ctx.fillStyle = ctx.strokeStyle;
        ctx.beginPath();
        ctx.arc(x, y, Math.log(val + 1) / 2, 0, 2 * Math.PI);
        ctx.fill();
        
        angle += angleStep + (val % 2 === 0 ? 0.1 : -0.1);
        radius += radiusStep;
    });

    ctx.stroke();

    // Add labels for key points
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'center';
  
    angle = 0;
    radius = 10;
    const labelInterval = Math.max(1, Math.floor(sequence.length / 12));
    const maxIndex = sequence.indexOf(maxVal);
  
    sequence.forEach((val, i) => {
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;

        const shouldLabel = i === 0 || i === sequence.length - 1 || i === maxIndex || i % labelInterval === 0;

        if(shouldLabel) {
            const text = val.toLocaleString();
            const metrics = ctx.measureText(text);
            ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
            const offsetX = Math.cos(angle) * 20;
            const offsetY = Math.sin(angle) * 20;
            ctx.fillRect(x + offsetX - metrics.width/2 - 3, y + offsetY - 10, metrics.width + 6, 14);
            
            ctx.fillStyle = '#333';
            ctx.fillText(text, x + offsetX, y + offsetY);
        }

        angle += angleStep + (val % 2 === 0 ? 0.1: -0.1);
        radius += radiusStep;
    });

    // Draw center point
    ctx.fillStyle = '#dc3545';
    ctx.beginPath();
    ctx.arc(centerX, centerY, 5, 0, 2 * Math.PI);
    ctx.fill();
}

// Start game logic
document.addEventListener("DOMContentLoaded", () => {
  const startBtn = document.getElementById("startBtn");
  const gameArea = document.getElementById("gameArea");

  if (startBtn && gameArea) {
    startBtn.addEventListener("click", () => {
      gameArea.classList.remove("d-none"); // show game area
      startBtn.classList.add("d-none");    // hide start button
    });
  }
});

