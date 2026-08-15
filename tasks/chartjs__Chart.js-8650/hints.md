
I fixed this by adding `padding` value to the `right` hand side of the chart. I played around with the exact number and 4 looked about right for my chart. But I’d imagine the right number will depend on the size of your `pointRadius` and other variables you have. This is what it looks like for me with the changes.

```
options: {
        layout: {
            padding: {
                left: 0,
                right: 4,
                top: 0,
                bottom: 0
            }
        }
    }
```

Also posted the answer here: 

https://stackoverflow.com/questions/57240818/chart-js-the-rightmost-data-point-cut-off-for-line-chart
Still in v3 https://codepen.io/etimberg/pen/vYKxEPB