document.addEventListener("DOMContentLoaded", function () {
  // === Parse weekly data ===
  const raw = document.getElementById("weekly-data");
  if (!raw) return;

  const data = JSON.parse(raw.textContent);
  const summary = data.summary || {};
  const goal = data.goal || 300;
  const start = new Date(data.start_date);

  // === Shared date/weekday labels for donut & line charts ===
  const labels = Array.from({ length: 7 }, (_, i) => {
    const d = new Date(start);
    d.setDate(start.getDate() + i);
    return {
      dateStr: d.toISOString().split("T")[0],
      weekday: d.toLocaleDateString(undefined, { weekday: 'short' })
    };
  });

  // === Donut Charts (per day) ===
  labels.forEach(({ dateStr }) => {
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
          ctx.fillStyle = '#1f2937';
          ctx.fillText(text, textX, textY);
          ctx.save();
        }
      }]
    });
  });

  // === Line Chart: Weekly Progress ===
  const lineCtx = document.getElementById("weeklyLineChart")?.getContext("2d");
  if (lineCtx) {
    const lineLabels = labels.map(l => l.weekday);
    const lineData = labels.map(l => summary[l.dateStr] || 0);

    new Chart(lineCtx, {
      type: "line",
      data: {
        labels: lineLabels,
        datasets: [{
          label: "Calories Burned",
          data: lineData,
          fill: false,
          borderColor: "rgba(255,99,132,1)",
          backgroundColor: "rgba(255,99,132,0.3)",
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            title: { display: true, text: "Calories" }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  // === Bar Chart: Activity Summary ===
  const rawActivity = document.getElementById("activity-data");
  if (rawActivity) {
    const activityData = JSON.parse(rawActivity.textContent || "[]");

    const activityTotals = {};
    const calorieTotals = {};

    activityData.forEach(a => {
      const [h, m, s] = a.activity_length.split(':').map(Number);
      const totalMinutes = h * 60 + m + s / 60;
      activityTotals[a.activity_type] = (activityTotals[a.activity_type] || 0) + totalMinutes;
      calorieTotals[a.activity_type] = (calorieTotals[a.activity_type] || 0) + a.calories_burned;
    });

    const ctxBar = document.getElementById('activityBarChart')?.getContext('2d');
    if (ctxBar) {
      new Chart(ctxBar, {
        type: 'bar',
        data: {
          labels: Object.keys(activityTotals),
          datasets: [
            {
              label: 'Minutes',
              data: Object.values(activityTotals),
              backgroundColor: 'rgba(0, 123, 255, 0.85)'
            },
            {
              label: 'Calories Burned',
              data: Object.values(calorieTotals),
              backgroundColor: 'rgba(255, 0, 0, 0.85)'
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            y: { beginAtZero: true },
            x: { stacked: false }
          }
        }
      });
    }
  }
});
