var ctx = document.getElementById("myChart");


const options = {
  layout: { autoPadding: false },
  hover: { intersect: false },
  // borderWidth: 100,
  backdropPadding: 0,
  padding: 0,
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      caretPadding: 10,
      caretPosition: 'right',
      caretX: 0,
      caretY: 0,
      intersect: false,
      mode: 'index',
      // xAlign: 'right',
      yAlign: 'center',
      position: 'average',
      // callbacks: {
      //   //This removes the tooltip title
      //   // title: function () {},
      //   label: ({ raw }) => {
      //     return raw
      //   },
      // },
      //this removes legend color
      displayColors: false,
      padding: 3,
      pointHitRadius: 5,
      pointRadius: 1,
      caretSize: 10,
      backgroundColor: 'rgba(255,255,255,.9)',
      // borderColor: `red`,
      borderWidth: 1,
      bodyFont: {
        family: 'Inter',
        size: 12,
      },
      bodyColor: '#303030',
      titleFont: {
        family: 'Inter',
      },
      titleColor: 'rgba(0,0,0,0.6)',
    },
  },
  scales: {
    y: {
      ticks: {
        display: false,
      },
      grid: {
        drawBorder: false,
        borderWidth: 0,
        drawTicks: false,
        color: 'transparent',
        width: 0,
        backdropPadding: 0,
      },
      drawBorder: false,
      drawTicks: false,
    },
    x: {
      ticks: {
        display: false,
      },
      grid: {
        drawBorder: false,
        borderWidth: 0,
        drawTicks: false,
        display: false,
      },
    },
  },
  responsive: true,
  maintainAspectRatio: false,
}

const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July']

const data = {
  labels,
  datasets: [
    {
      label: 'Dataset 1',
      data: [0, 0, 3, 4, 5, 6, 0],
      backgroundColor: '#464eff',
      minBarLength: 50,
      borderRadius: 100,
      borderSkipped: false,
    },
    {
      label: 'Dataset 2',
      data: [0, 4, 2, 1, 4, 0, 7],
      backgroundColor: '#c7c8e9',
      minBarLength: 50,
      borderRadius: 100,
      borderSkipped: false,
    },
  ],
}


var myChart = new Chart(ctx, {
    type: 'bar',
    data,
    options,
});