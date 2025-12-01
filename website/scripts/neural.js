const canvas = document.getElementById('neuralCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

class Neuron {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.connections = [];
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
        ctx.fillStyle = '#00d4ff';
        ctx.fill();
    }
}

const neurons = [];
for (let i = 0; i < 100; i++) {
    neurons.push(new Neuron());
}

function drawConnections() {
    for (let i = 0; i < neurons.length; i++) {
        for (let j = i + 1; j < neurons.length; j++) {
            const dx = neurons[i].x - neurons[j].x;
            const dy = neurons[i].y - neurons[j].y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 150) {
                ctx.beginPath();
                ctx.moveTo(neurons[i].x, neurons[i].y);
                ctx.lineTo(neurons[j].x, neurons[j].y);
                ctx.strokeStyle = `rgba(0, 212, 255, ${1 - distance / 150})`;
                ctx.lineWidth = 0.5;
                ctx.stroke();
            }
        }
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    neurons.forEach(neuron => {
        neuron.update();
        neuron.draw();
    });
    
    drawConnections();
    requestAnimationFrame(animate);
}

animate();

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        
        document.querySelectorAll('.nav-link').forEach(navLink => {
            navLink.classList.remove('active');
        });
        
        link.classList.add('active');
        document.getElementById(targetId).classList.add('active');
    });
});

function toggleEmergencyMode() {
    const statusEl = document.getElementById('emergencyStatus');
    const isActive = statusEl.textContent === 'ON';
    
    fetch('/api/emergency-mode', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({enabled: !isActive})
    }).then(() => {
        statusEl.textContent = isActive ? 'OFF' : 'ON';
        statusEl.style.color = isActive ? '#666' : '#00ff88';
    });
}

function showDopamineSchedule() {
    showModal('Dopamine Schedule', `
        <h3>Configure Allowed Hours</h3>
        <p>Set the hours when you can use certain apps:</p>
        <div class="time-picker">
            <input type="time" id="modalStart" class="time-input glass">
            <span>to</span>
            <input type="time" id="modalEnd" class="time-input glass">
        </div>
        <button class="action-btn" onclick="saveDopamineSchedule()">Save Schedule</button>
    `);
}

function generateReport() {
    fetch('/api/reports/monthly', {method: 'POST'})
        .then(res => res.json())
        .then(data => {
            showModal('Report Generated', `
                <h3>Monthly Report Created</h3>
                <p>Your detailed report has been generated and sent to your parent's email.</p>
                <p><strong>Threats Blocked:</strong> ${data.threats}</p>
                <p><strong>Time Saved:</strong> ${data.timeSaved} minutes</p>
            `);
        });
}

function showParentLink() {
    fetch('/api/parent/status')
        .then(res => res.json())
        .then(data => {
            if (data.linked) {
                showModal('Parent Account', `
                    <h3>Linked to Parent</h3>
                    <p><strong>Parent Email:</strong> ${data.parentEmail}</p>
                    <button class="action-btn" onclick="unlinkParent()">Unlink</button>
                `);
            } else {
                showModal('Link Parent Account', `
                    <h3>Enter Pairing Code</h3>
                    <input type="text" id="pairingInput" class="input-field glass" maxlength="6">
                    <button class="action-btn" onclick="linkParent()">Link</button>
                `);
            }
        });
}

function saveSettings() {
    const start = document.getElementById('allowedStart').value;
    const end = document.getElementById('allowedEnd').value;
    const level = document.getElementById('protectionLevel').value;
    
    fetch('/api/settings', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({allowedStart: start, allowedEnd: end, protectionLevel: level})
    }).then(() => {
        showModal('Settings Saved', '<h3>Your settings have been updated successfully!</h3>');
    });
}

function pairAccount() {
    const code = document.getElementById('pairingCode').value;
    
    fetch('/api/parent/pair', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({code})
    }).then(res => res.json())
      .then(data => {
          showModal('Pairing Result', data.success ? '<h3>Account Linked Successfully!</h3>' : '<h3>Invalid Code</h3>');
      });
}

function generatePairingCode() {
    fetch('/api/parent/generate-code', {method: 'POST'})
        .then(res => res.json())
        .then(data => {
            document.getElementById('generatedCode').textContent = data.code;
        });
}

function showModal(title, content) {
    document.getElementById('modalBody').innerHTML = `<h2>${title}</h2>${content}`;
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

window.onclick = (e) => {
    if (e.target === document.getElementById('modal')) {
        closeModal();
    }
};

function loadDashboardData() {
    fetch('/api/stats/today')
        .then(res => res.json())
        .then(data => {
            document.getElementById('threatsBlocked').textContent = data.threatsBlocked;
            document.getElementById('timeSaved').textContent = data.timeSaved;
            document.getElementById('currentStreak').textContent = data.currentStreak;
        });
}

setInterval(loadDashboardData, 5000);
loadDashboardData();
