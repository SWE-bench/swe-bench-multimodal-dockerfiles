@benfrain there is a `mirror` option on the vertical axes that might solve this for you

```javascript
axisOptions = {
  ticks: {
    mirror: true
  }
}
```
@etimberg I have this config currently for the yAxis ([as discussed the xAxis mirror doesn't work yet](https://github.com/chartjs/Chart.js/issues/4488), ) which lets the yAxis ticks sit inside, is that what you meant?

```javascript
{
    yAxisID: "y-axis-0",
    ticks: {
        beginAtZero: false,
        mirror: true,
    },
    gridLines: {
        display: true,
        drawTicks: false,
    },
},
{
    position: "right",
    id: "y-axis-1",
    ticks: {
        beginAtZero: false,
        mirror: true,
    },
    gridLines: {
        display: false,
        drawTicks: false,
    },
},
```
That places the Y axis ticks inside nicely but padding appears either side of the canvas currently due to the X axis ticks rendering to the side of the main graph bounds.


That is what I meant. I see you've already tried that. One generic solution to this is to allow different tick alignments. As you noticed, the tick is center aligned to the value. We could add something that allows different alignments: `'left'|'center'|'right'|'auto'` and 'auto' would put left for the first tick, center for the middle ticks and right for the last tick. I think I tried implementing this about a year ago and ran into issues. I can't recall what they exactly were.
@etimberg that sounds ideal! Would certainly fix my problem :)
Is this still being worked on? Would love to see this feature.
**+1** This would add a huge UX factor, especially in state of the art chart designs.
+1 any news on that?
+1
Any updates? I've tried to remove the first and last trick because those are causing the padding:
```
'afterTickToLabelConversion' => function (settings) {
    settings.ticks[0] = null;
    settings.ticks[settings.ticks.length - 1] = null;
}
```

But it's not working :( Maybe we can setup a Bountysource to get this implemented? Related: https://github.com/chartjs/Chart.js/issues/4997 with a nasty fix, but it's working...
+1 Any updates?
Hello everyone!! Today I have been crazy about this issue, and I think I found a solution!:

```
xAxes: [{ticks: {
            padding: -25,
            z: 1,
        }}]
```

I hope it helps!
