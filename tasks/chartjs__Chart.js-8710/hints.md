How is the page updating the charts? Something is altering the chart while its still updating. Maybe destroying it?
@kurkle 

> How is the page updating the charts? Something is altering the chart while its still updating. Maybe destroying it?

```
                      if (this.chart) {
                            // be shure that no chart exits before create..
                            this.chart.destroy()
                            this.chart = null
                        }
                        this.ChartControl.defaults.locale = "de-DE"
                        // this.ChartControl.defaults.locale = "de_DE" --> ERROR
                        this.chart = new window.Chart3(this.ctx, graphOptions)
                        this.graphDataSets = this.graphData.data.datasets

                        if (this.chart) {
                            this.chart_ready = true
                        }
```
Numberformat for series is working, only the ticks numbers has no locale based format.

![Bildschirmfoto 2021-03-24 um 07 56 34](https://user-images.githubusercontent.com/30198737/112268038-a52ab080-8c76-11eb-94ad-4cf92fd916b3.png)


`Render Graph Error on  line :  RangeError: Incorrect locale information provided`
I am shure that the locale was set, because if the locale is wrong --> Error  ???
Ok, what happens when `this.graphDatasets` is set? And what is `this.chart_ready` used for?
@kurkle 
> Ok, what happens when `this.graphDatasets` is set? And what is `this.chart_ready` used for?

I use `this.graphDatasets` and  `this.chart_ready` internal to check :
```
if (
   this.graphDataSets &&
   this.graphDataSets.length &&
   JSON.stringify(this.graphDataSets) === JSON.stringify(this.graphData.data.datasets)
) {
   // same data as before, skip redraw...
   return
}

```
Ok, and is anything done to the chart in the redraw?
@kurkle 
> Ok, and is anything done to the chart in the redraw?

Negativ, i do not use  `chart.update(....)`  and nothing with `redraw`

Last question, does removing the layout padding get rid of the error?
We really need a test case, its waste of time trying to debug this by asking questions.
@kurkle 
> Last question, does removing the layout padding get rid of the error?

Yes, No error when setting layout padding.

@kurkle 
It is difficult to create a test case, because in the simple case the error does not occur. 

I suspect it is a timing problem, if the chart is being resized while rendering,
 it could be the cause.
I'd suspect the problem is not in Chart.js, but its impossible to tell for sure without test case.
@kurkle 
I will try to find a testcase...
But **Pre-release v3.0.0-rc.1** is working w/o any errors...
Just making sure, beta.14 works correctly? (I saw beta.12 mentioned and there are just too many commits to start looking form there)
Circling back to the actual error message, can you debug the `options` passed to `formatNumber`? 

Escpecially the `minimumFractionDigits` and `maximumFractionDigits`?
@kurkle 
Searched for a long time, but you were right - it was due to the home assistant framework. 

This always renders the element twice, because the constructor is always called several times and this very quickly one after the other. The first time the HTML element is not yet visible and therefore the size cannot be calculated. This then leads to the error.
```
update(chart, width, height, minPadding) {
    if (!chart) {
      return;
    }
	.....
```
I now check beforehand whether the size is known and only then the rendering process of Chart.js is called.

```
if(this.card.getClientRects().length==0) return
this.chart = new window.Chart3(this.ctx, graphOptions)
...
```

Sorry - and thanks for your help and time 👍 

@zibous thanks for debugging! I found the root cause of the locale issue, so I'll have a PR up shortly to fix it.