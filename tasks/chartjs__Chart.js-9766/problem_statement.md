Stacked line charts dont take stack into account when calculating min y axis tick 
### Expected vs Current Behavior
When using stacked lines, the graphs always begin at zero despite setting beginAtZero to be false manually. See https://jsfiddle.net/y91v0fh3/ for an example of expected behavior when not stacked, and uncomment the stacked options to see erroneous behavior. I am unable to set the scales min value as many other posts suggest due to the data I will be working with having a large range of possible values.

### Environment
Chart.js version: v3.5.1
Browser name and version: Chrome
