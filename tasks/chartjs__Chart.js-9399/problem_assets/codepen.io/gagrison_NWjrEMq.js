var config = {
  type: 'bar',
  options: {
    categoryPercentage: 1,
    barPercentage: 1,
    backgroundColor: '#2E5C76',
    scales: {
      x: {
        grid: { display: false },
      },
    },
    plugins: {
      legend: { display: false },
    },
  },
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [{
      data: [9, 25, 13, 17, 12, 21, 20, 19, 6, 12, 14, 20],
    }],
  }
};

new Chart('chart', config);