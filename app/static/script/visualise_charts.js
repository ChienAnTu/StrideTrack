document.addEventListener("DOMContentLoaded", function () {
  const rawDataScript = document.getElementById('activity-data');
  const rawData = rawDataScript ? JSON.parse(rawDataScript.textContent) : [];

  const activityTotals = {};
  const calorieTotals = {};

  rawData.forEach(a => {
    const [h, m, s] = a.activity_length.split(':').map(Number);
    const totalMinutes = h * 60 + m + s / 60;

    activityTotals[a.activity_type] = (activityTotals[a.activity_type] || 0) + totalMinutes;
    calorieTotals[a.activity_type] = (calorieTotals[a.activity_type] || 0) + a.calories_burned;
  });

  const ctxBar = document.getElementById('activityTimeChart')?.getContext('2d');
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

  const ctxPie = document.getElementById('activityPieChart')?.getContext('2d');
  if (ctxPie) {
    new Chart(ctxPie, {
      type: 'doughnut',
      data: {
        labels: Object.keys(activityTotals),
        datasets: [{
          data: Object.values(activityTotals),
          backgroundColor: [
          'rgba(255, 99, 132, 0.85)',   // Red-Pink
          'rgba(0, 123, 255, 0.85)',    // Bright Blue
          'rgba(255, 193, 7, 0.85)',    // Yellow
          'rgba(40, 167, 69, 0.85)',    // Green
          'rgba(255, 87, 34, 0.85)',    // Deep Orange
          'rgba(102, 16, 242, 0.85)'    // Purple
        ]

        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom' }
        }
      }
    });
  }
});
