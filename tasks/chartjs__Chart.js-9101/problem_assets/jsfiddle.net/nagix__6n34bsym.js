var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    datasets: [{
      data: [
      	{x: 1, y: 2},
        {x: 2, y: 1},
        {x: 3, y: 3}
      ],
      borderColor: 'black',
      backgroundColor: ['pink', 'lightblue', 'lightgreen'],
      pointRadius: 20,
      pointHoverRadius: 25
    }]
  },
  options: {
    scales: {
      x: {
        type: 'linear',
			},
      y: {
        type: 'linear',
        min: 0,
        max: 4
      }
    },
    plugins: {
      legend: false
    }
  }
});

function showData() {
  const {data, backgroundColor} = myChart.data.datasets[0];
  document.getElementById('data').textContent = data.map(p => `{x: ${p.x}, y: ${p.y}}`).join(', ');
  document.getElementById('background-color').textContent = backgroundColor.join(', ');
}

function randomColor() {
  return ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'grey'][Math.floor(Math.random() * 7)];
}

showData();

document.getElementById('push').addEventListener('click', () => {
  const {data, backgroundColor} = myChart.data.datasets[0];
  data.push({
    x: data[data.length - 1].x + 1,
    y: Math.floor(Math.random() * 3) + 1
  });
  backgroundColor.push(randomColor());
  showData();
  myChart.update();
});

document.getElementById('shift').addEventListener('click', () => {
  const {data, backgroundColor} = myChart.data.datasets[0];
  data.shift();
  backgroundColor.shift();
  showData();
  myChart.update();
});