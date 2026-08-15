var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
    type: 'bubble',
    data: {
        datasets: [{
            label: '# of Votes',
            data: [
              [12, 2],
              [19, 3],
              [1, 7],
              [15, 10],
              [13, 5],
              [22, 6]
            ],
            radius: 5,
            hoverRadius: 0, /* bubble disappears */
            //hoverRadius: 5 /* bubble gets bigger */
        }]
    }
});