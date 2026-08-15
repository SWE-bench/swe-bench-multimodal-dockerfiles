Shifting items of array option for dataset breaks the chart
## Expected Behavior

I created a line chart, and a dataset has a backgroundColor array. When the first items of the data and backgroundColor arrays are removed using `shift()`, it should be correctly reflected in the chart.

## Current Behavior

When the first items of the data and backgroundColor arrays are removed, elements in the chart have wrong colors.

<img width="491" alt="Screen Shot 2021-05-15 at 12 22 33 AM" src="https://user-images.githubusercontent.com/723188/118299781-c2ac2600-b513-11eb-9267-6701697702d1.png">

## Possible Solution

Not sure, but I suspect that the caching when resolving the options might cause the problem.

## Steps to Reproduce

Press 'Push Data' button, then press 'Shift Data' button.

https://jsfiddle.net/nagix/6n34bsym/

## Environment

* Chart.js version: 3.2.1
