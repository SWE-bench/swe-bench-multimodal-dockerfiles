var jsonfile = {
  "jsonarray": 
[
 {
   "ID": 12,
   "STATION": "Maida Vale",
   "Median": "695000",
   "# of results": 22,
   "ZONE": 2
 },
 {
   "ID": 13,
   "STATION": "Warwick Avenue",
   "Median": "710000",
   "# of results": 33,
   "ZONE": 2
 },
 {
   "ID": 14,
   "STATION": "Paddington",
   "Median": "720000",
   "# of results": 52,
   "ZONE": 1
 },
 {
   "ID": 15,
   "STATION": "Edgware Road",
   "Median": "775000",
   "# of results": 45,
   "ZONE": 1
 },
 {
   "ID": 16,
   "STATION": "Marylebone",
   "Median": "667500",
   "# of results": 38,
   "ZONE": 1
 },
 {
   "ID": 17,
   "STATION": "Baker Street",
   "Median": "995000",
   "# of results": 18,
   "ZONE": 1
 },
 {
   "ID": 18,
   "STATION": "Regent’s Park",
   "Median": " 1375000",
   "# of results": 12,
   "ZONE": 1
 },
 {
   "ID": 19,
   "STATION": "Oxford Circus",
   "Median": "802500",
   "# of results": 18,
   "ZONE": 1
 },
 {
   "ID": 20,
   "STATION": "Piccadilly Circus",
   "Median": " 1225000",
   "# of results": 23,
   "ZONE": 1
 },
 {
   "ID": 21,
   "STATION": "Charing Cross",
   "Median": " 1160000",
   "# of results": 24,
   "ZONE": 1
 }
]
};

var labels = jsonfile.jsonarray.map(function(e) {
   return e.STATION;
});
var data = jsonfile.jsonarray.map(function(e) {
   return e.Median;
});;
var sampleSize = jsonfile.jsonarray.map(function(e) {
   return e.nResults;
});;

var ctx = document.getElementById("myChart").getContext('2d');
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: labels,
    datasets: [
      { 
        data: data,
        label: 'Median price',
        borderColor: "#996633",
        pointRadius: 5, 
        pointHoverRadius: 6,
        pointBorderWidth: 2,
        pointBorderColor: "white",
        pointBackgroundColor: "black",
        fill: false
      }
    ]
  }, 
  options: {
      legend: {
        display: false,
      },
      tooltips: {
        displayColors: false,
        callbacks: {
            label: function (tooltipItem, data) {
              var tooltipValue = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
              return "£" + parseInt(tooltipValue).toLocaleString();
          }
      }
      },    
        scales: {
          yAxes: [{ 
                gridLines: {
                  color: "white",
                  lineWidth: 2
                },
                ticks: {
                  beginAtZero: true,
              min: 0,
              stepSize: 500000,
              callback: function(value, index, values) {
              return "£" + value.toLocaleString();
            },
          },
          scaleLabel: {
              display: true,
              labelString: "Median house price"
        }
              }],
            xAxes: [{
              display: false, 
                ticks: {
                    display: false 
                }
            }]
        }
    },
});


Chart.plugins.register({
  beforeDraw: function(chartInstance, easing) {
    var ctx = chartInstance.chart.ctx;
    ctx.fillStyle = '#F8F8F8'; 
    var chartArea = chartInstance.chartArea;
    ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);
  }
});