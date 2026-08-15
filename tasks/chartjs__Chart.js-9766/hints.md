As stated in the issue template, chartjs versions lower as V3 are not supported anymore which means V2 is not supported.

In V3 this seems to be fixed after checking this sample and setting the min data to 50: https://www.chartjs.org/docs/master/samples/area/line-stacked.html
@LeeLenaleee, now that you mention it, I am having the same issue with v3.5. Is there a way to do this without setting the min? Unfortunately, I don't have that luxury in my actual use case. 

I have updated my original question with these details. 
I did not set a min on the scale itself, I used the stacked line example of chart.js and only generated data points with a minimum value of 50 and could not reproduce it, so if you have this issue can you provide a working example of the issue?
Glad to hear this is fixed in v3. Thanks for your help. 

I ended up solving my issue in v2.9 by using the options.scales.yAxes[0].afterDataLimits callback to reset the min on the axis manually by finding the min of the line at the bottom of my stack.
Hi @LeeLenaleee ,

I was finally able to reproduce the issue I am having using the link to the documentation that you provided. If you paste the following code into the setup tab to replace all that is there, you should see the y axis starts at zero despite no point being shown below 11. The key to reproducing was having the line with lower values (all 1's here) stacked on top of another line (all 10+ here). Seems that when calculating where to start the y axis, it finds the lowest value on the line not taking into account that those lowest points are stacked on top of points much further from 0. Ideally id want the yaxis to start somewhere closer to 10 than 0.

const DATA_COUNT = 7;
const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};

const labels = Utils.months({count: 7});
const data = {
  labels: labels,
  datasets: [
    {
      label: 'My Second dataset',
      data: [10,10,10,10,10,10,11],
      borderColor: Utils.CHART_COLORS.blue,
      backgroundColor: Utils.CHART_COLORS.blue,
      fill: true
    },
    {
      label: 'My First dataset',
      data: [1,1,1,1,1,1,1],
      borderColor: Utils.CHART_COLORS.red,
      backgroundColor: Utils.CHART_COLORS.red,
      fill: true
    }
  ]
};

I would expect it to find the minimum value of the lowest line in the stack when calculating the min y tick.

Curious to hear your thoughts on this. Thanks!