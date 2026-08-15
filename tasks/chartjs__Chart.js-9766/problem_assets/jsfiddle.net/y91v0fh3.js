var options = {
    responsive: true,
    scales: {
        yAxes: [{
        		// stacked: true,
        }]
    }
};

var data = {
        labels: ["A", "B", "C"],
        datasets: [{
            label: '# of Votes',
            data: [1000, 1059, 1050]
        },{
            label: '# of Votes',
            data: [1045, 1065, 1052]
        }]
    }

var ctx = document.getElementById("myChart");

var chartInstance = new Chart(ctx, {
    type: 'line',
    data: data,
    options:options
});
