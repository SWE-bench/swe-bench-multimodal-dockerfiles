Pie Chart hoverOffset bugs on a specific value
### Expected behavior

When hovering, while using hoverOffset,  any border of the initial circle should not appear in any case.

### Current behavior

If you provide the pie chart an array containing a value "385" while the rest of the values in the array are 0, it messes up when you hover. This only happens when using the hoverOffset option.

### Reproducible sample

https://jsfiddle.net/5rnyo4qc/12/

### Optional extra steps/info to reproduce

Just pass an array with a 385 value at any index while the rest of the values are 0 like [0,0,385,0] and use hoverOffset and you'll see the bug when you hover.

### Possible solution

_No response_

### Context

_No response_

### chart.js version

v3.9.1

### Browser name and version

Chrome v106.0.5249.119

### Link to your project

_No response_
