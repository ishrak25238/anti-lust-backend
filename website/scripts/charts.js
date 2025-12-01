function initCharts() {
    const patternCanvas = document.getElementById('patternChart');
    const timelineCanvas = document.getElementById('timelineChart');
    const categoryCanvas = document.getElementById('categoryChart');

    if (patternCanvas) {
        const patternCtx = patternCanvas.getContext('2d');
        drawPatternChart(patternCtx, patternCanvas.width, patternCanvas.height);
    }

    if (timelineCanvas) {
        const timelineCtx = timelineCanvas.getContext('2d');
        drawTimelineChart(timelineCtx, timelineCanvas.width, timelineCanvas.height);
    }

    if (categoryCanvas) {
        const categoryCtx = categoryCanvas.getContext('2d');
        drawCategoryChart(categoryCtx, categoryCanvas.width, categoryCanvas.height);
    }
}

function drawPatternChart(ctx, width, height) {
    const hours = Array.from({ length: 24 }, (_, i) => i);
    const data = [2, 1, 0, 0, 0, 1, 2, 3, 4, 5, 3, 2, 2, 1, 2, 3, 4, 6, 8, 12, 15, 18, 12, 6];

    const padding = 40;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;
    const maxValue = Math.max(...data);
    const pointSpacing = chartWidth / (data.length - 1);

    ctx.clearRect(0, 0, width, height);

    ctx.strokeStyle = 'rgba(0, 212, 255, 0.2)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
        const y = padding + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
    }

    ctx.beginPath();
    ctx.strokeStyle = '#00d4ff';
    ctx.lineWidth = 2;

    data.forEach((value, index) => {
        const x = padding + index * pointSpacing;
        const y = height - padding - (value / maxValue) * chartHeight;

        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });

    ctx.stroke();

    ctx.fillStyle = 'rgba(0, 212, 255, 0.2)';
    ctx.lineTo(width - padding, height - padding);
    ctx.lineTo(padding, height - padding);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = '#fff';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    [0, 6, 12, 18, 23].forEach(hour => {
        const x = padding + (hour / 23) * chartWidth;
        ctx.fillText(`${hour}:00`, x, height - 10);
    });
}

function drawTimelineChart(ctx, width, height) {
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const data = [45, 38, 52, 41, 36, 55, 48];

    const padding = 40;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;
    const barWidth = chartWidth / days.length - 20;
    const maxValue = Math.max(...data);

    ctx.clearRect(0, 0, width, height);

    data.forEach((value, index) => {
        const x = padding + (chartWidth / days.length) * index + 10;
        const barHeight = (value / maxValue) * chartHeight;
        const y = height - padding - barHeight;

        const gradient = ctx.createLinearGradient(x, y, x, height - padding);
        gradient.addColorStop(0, '#00d4ff');
        gradient.addColorStop(1, '#00ff88');

        ctx.fillStyle = gradient;
        ctx.fillRect(x, y, barWidth, barHeight);

        ctx.fillStyle = '#fff';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(days[index], x + barWidth / 2, height - 20);
        ctx.fillText(value, x + barWidth / 2, y - 10);
    });
}

function drawCategoryChart(ctx, width, height) {
    const categories = [
        { name: 'NSFW Images', value: 45, color: '#ff0055' },
        { name: 'Adult Sites', value: 30, color: '#ff6b00' },
        { name: 'Keywords', value: 15, color: '#ffd000' },
        { name: 'Dark Web', value: 8, color: '#00d4ff' },
        { name: 'Other', value: 2, color: '#00ff88' }
    ];

    const total = categories.reduce((sum, cat) => sum + cat.value, 0);
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) / 2 - 40;

    let currentAngle = -Math.PI / 2;

    categories.forEach(category => {
        const sliceAngle = (category.value / total) * Math.PI * 2;

        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
        ctx.closePath();

        ctx.fillStyle = category.color;
        ctx.fill();

        ctx.strokeStyle = '#0a0e27';
        ctx.lineWidth = 2;
        ctx.stroke();

        const labelAngle = currentAngle + sliceAngle / 2;
        const labelX = centerX + Math.cos(labelAngle) * (radius - 40);
        const labelY = centerY + Math.sin(labelAngle) * (radius - 40);

        ctx.fillStyle = '#fff';
        ctx.font = 'bold 12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`${Math.round((category.value / total) * 100)}%`, labelX, labelY);

        currentAngle += sliceAngle;
    });

    let legendY = 20;
    categories.forEach(category => {
        ctx.fillStyle = category.color;
        ctx.fillRect(width - 120, legendY, 15, 15);

        ctx.fillStyle = '#fff';
        ctx.font = '11px Arial';
        ctx.textAlign = 'left';
        ctx.fillText(category.name, width - 100, legendY + 12);

        legendY += 25;
    });
}

window.addEventListener('load', initCharts);
