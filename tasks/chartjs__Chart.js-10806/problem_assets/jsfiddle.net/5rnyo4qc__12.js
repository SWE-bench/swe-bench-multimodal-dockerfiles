var options = {
  type: 'pie',
  data: {
    labels: ['a', 'b', 'c', 'd', '1', '2', '3'],
    datasets: [
      {
        data: [0, 0, 0, 385, 0, 0, 0],
        backgroundColor: [
          '#FE433C',
          '#3C50B1',
          '#0095EF',
          '#A224AD',
          '#F31D64'
        ],
        hoverOffset: 20
      }
    ]
  },
  options: {
    plugins: {
      legend: {
        position: 'bottom',
        labels: { usePointStyle: true, pointStyle: 'circle' }
      }
    },
    radius: '90%'
  }
};

var ctx = document.getElementById('chartJSContainer').getContext('2d');
new Chart(ctx, options);