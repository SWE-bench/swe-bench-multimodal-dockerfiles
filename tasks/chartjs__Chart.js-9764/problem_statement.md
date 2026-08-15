hover radius not working correctly
## Expected Behavior

As described [here](https://www.chartjs.org/docs/latest/charts/bubble.html#interactions), hover radius is defined as *additional* radius when hovered. Setting hover radius to 0 should result in the same size for hover / not hover.

## Current Behavior
When the hover radius is set to 0, the bubble disappears on hover. When the hover radius is set to the same as the radius, the bubble gets bigger.

## Steps to Reproduce
https://codepen.io/elitastic/pen/jOLPZvP

## Environment

* Chart.js version: 3.5.1
* Browser name and version: Chrome 94

