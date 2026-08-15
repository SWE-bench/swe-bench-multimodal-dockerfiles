Legend label click (& other events) use wrong label with multi-line, gets worse the more labels there are
### Expected behavior

Clicking anywhere in a multi-line label performs the click action (or hover event) on that legend item, not the one above it.

### Current behavior

If legend is positioned `right` and labels are multi-line (2 lines for me), then clicking a legend label (for default behavior of hiding/showing), will perform that on the label above the one you click. This gets worse (more off) the more labels you have (like 5+). For example, clicking the 4th label performs the action on the 3rd.

![LegenLabelClick-Hover](https://user-images.githubusercontent.com/12361341/236559775-b3c7823e-816b-43cd-b6eb-c44d0ca8dc7b.gif)


### Reproducible sample

https://www.chartjs.org/docs/latest/samples/legend/events.html

### Optional extra steps/info to reproduce

I don't use Codepen, but on this samples page:
https://www.chartjs.org/docs/latest/samples/legend/events.html

If you position legend to the right, and use the following for labels, you can easily see it.
```
labels: [['Red Test','Test line 2'], ['Blue test','Test line 2'], ['Yellow test','Test line 2'], ['Green test','Test line 2'], ['Purple test','Test line 2'], ['Orange test','Test line 2']],
```

### Possible solution

_No response_

### Context

_No response_

### chart.js version

v4.3.0

### Browser name and version

Firefox Windows 102.10, and Edge Windows

### Link to your project

_No response_
