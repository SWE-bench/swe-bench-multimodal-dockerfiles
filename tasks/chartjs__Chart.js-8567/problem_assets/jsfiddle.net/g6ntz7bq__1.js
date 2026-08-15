var toCurrency=(label, currency) => label;

var data = {
  datasets: [
        {
          label: "Dataset 1",
          data: [52088152, 88035769, 12109270],
          backgroundColor: "#0D3359",
        },
        {
          label: "Dataset 2",
          data: [89273999, 83055712, 16456745],
          backgroundColor: "#103E6C",
        },
        {
          label: "Dataset 3",
          data: [44523423, undefined, 76453453],
          backgroundColor: "#13497F",
        },
      ],
      labels: ["2019", "2018", "2017"],
};

var options = {
  maintainAspectRatio: false,
  legend: {
        position: "bottom",
      },
  scales: {
    yAxes: [{
      ticks: {
         callback: label => {
           //Formats the label using numbro in real code
            return toCurrency(label);
          },
      }
    }]
  }
};

Chart.Bar('chart', {
  options: options,
  data: data
});
