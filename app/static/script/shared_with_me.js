document.addEventListener("DOMContentLoaded", () => {
  const raw = document.getElementById("shared-data");
  if (!raw) return;
  const data = JSON.parse(raw.textContent);

  const labels = Object.keys(data);
  const values = Object.values(data);

  const ctx = document.getElementById("sharedPieChart").getContext("2d");

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: [
          '#60A5FA', '#34D399', '#FBBF24', '#F87171', '#A78BFA', '#F472B6'
        ]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });
});
