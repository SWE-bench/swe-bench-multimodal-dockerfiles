Thicker border in 3.5.0+


## Expected Behavior

Same as version 3.4.1.

## Current Behavior

Since version 3.5.0 the border thickness has increased for the chart (but not legend).

## Possible Solution

Decreasing the "borderWidth", but that also affects the border used in the legend which I don't want to change.

## Steps to Reproduce

You can check this behaviour in the documentation (compare latest version vs 3.4.1.):
https://www.chartjs.org/docs/latest/samples/bar/border-radius.html (thicker border)
vs 
https://www.chartjs.org/docs/3.4.1/samples/bar/border-radius.html (OK border)

https://www.chartjs.org/docs/latest/samples/bar/horizontal.html (thicker border)
vs
https://www.chartjs.org/docs/3.4.1/samples/bar/horizontal.html (OK border)

Might have to resize your screen for a better comparison (in the latest version the chart is much larger in the documentation).

## Context

Since version 3.5.0 (also in 3.5.1) the border thickness has changed. It's more bolder now.

I always used "borderWidth: 2" which was perfect for my case, but now it's too thick. When I use "borderWidth: 1" it's thinner than before and also the legend border changes (which I don't want).
