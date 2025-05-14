document.addEventListener("DOMContentLoaded", function () {
  const raw = document.getElementById("weekly-data");
  if (!raw) return;

  const data = JSON.parse(raw.textContent);
  const summary = data.summary || {};   // e.g. { "2024-05-13": 280, "2024-05-14": 320 }
  const goal = data.goal || 300;
  const start = new Date(data.start_date);
  const labels = [];

  for (let i = 0; i < 7; i++) {
    const d = new Date(start);
    d.setDate(d.getDate() + i);
    const dateStr = d.toISOString().split("T")[0]; // YYYY-MM-DD
    const weekday = d.toLocaleDateString(undefined, { weekday: 'short' }); // e.g. Mon
    labels.push({ dateStr, weekday });
  }

  labels.forEach(({ dateStr, weekday }) => {
    const value = summary[dateStr] || 0;
    const reached = Math.min(value, goal);
    const remaining = Math.max(goal - value, 0);
    const ctx = document.getElementById(`donut-${dateStr}`);
    if (!ctx) return;

    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Reached', 'Remaining'],
        datasets: [{
          data: [reached, remaining],
          backgroundColor: [
            value >= goal ? 'rgba(34,197,94,0.8)' : 'rgba(255,165,0,0.8)',
            'rgba(229,231,235,0.6)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        cutout: '70%',
        plugins: {
          tooltip: { enabled: false },
          legend: { display: false },
          title: { display: false }
        }
      },
      plugins: [{
        id: 'centerText',
        beforeDraw(chart) {
          const { width, height } = chart;
          const ctx = chart.ctx;
          ctx.restore();
          ctx.font = '14px sans-serif';
          ctx.textBaseline = 'middle';
          const text = `${Math.round(value)} kcal`;
          const textX = Math.round((width - ctx.measureText(text).width) / 2);
          const textY = height / 2;
          ctx.fillStyle = '#1f2937'; // gray-800
          ctx.fillText(text, textX, textY);
          ctx.save();
        }
      }]
    });
  });
});

