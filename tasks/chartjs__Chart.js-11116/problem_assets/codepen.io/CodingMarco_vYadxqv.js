var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
  type: "line",
  data: {
    datasets: [
      {
        label: "Dataset",
        // Datapoints are exactly at the x- and y-axis min and max values
        data: [
          { x: 2.404e-8, y: 2.404e-8 },
          { x: 2.4143e-8, y: 2.4143e-8 }
        ],
        yAxisID: "y"
      }
    ]
  },
  options: {
    scales: {
      x: {
        type: "linear",
        min: 2.404e-8,
        max: 2.4143e-8,
        ticks: {
          includeBounds: false,
          callback: (value, index, ticks) => value.toExponential()
        }
      },
      y: {
        type: "linear",
        min: 2.404e-8,
        max: 2.4143e-8,
        ticks: {
          includeBounds: false,
          callback: (value, index, ticks) => value.toExponential()
        }
      }
    }
  }
});