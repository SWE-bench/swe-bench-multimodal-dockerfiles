var ctx = document.getElementById("myChart");
var dataEl = [];
for (var i = 0; i<15552; i++) {
	dataEl.push({x: i, y: i});
}


var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Test',
            data: dataEl
        }]
    },
    options: {
    parsing: false,
      // Data are already ordered
      normalized: true,
      animation: false,
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        y: {
          title: {
            display: true,
            text: 'y'
          },
          type: 'linear',
          ticks: {
            minRotation: 50,
            maxRotation: 50
          }
        },
        x: {
          title: {
            display: true,
            text: 'x'
          },
          type: 'linear',
          min: 0,
          max: 15552,
          ticks: {
            minRotation: 50,
            maxRotation: 50
          }
        }
      },
      plugins: {
        decimation: {
          enabled: true,
          algorithm: 'lttb'
        }
      }
    }
});