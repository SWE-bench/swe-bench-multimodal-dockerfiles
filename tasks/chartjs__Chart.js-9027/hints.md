Options passed to `new Chart()`

ref to canvas:
```
<canvas height="0" width="0" style="display: block; box-sizing: border-box; height: 0px; width: 0px;"></canvas>
```

opts:
```
{"type":"bar","data":{"datasets":[{"data":[29.05,4,15.69,11.69,2.84,4,0,3.84,4],"backgroundColor":["#597fdd","#51a8e7","#56c9ab","#6fd872","#a4d53f","#e6c72f","#f29a2c","#f0583b","#dc2054","#e0379d","#dd48e1","#aa4ee0","#8260ed"],"hoverBackgroundColor":["#597fdd","#51a8e7","#56c9ab","#6fd872","#a4d53f","#e6c72f","#f29a2c","#f0583b","#dc2054","#e0379d","#dd48e1","#aa4ee0","#8260ed"],"label":"Costs"}],"labels":[0,1,2,3,4,5,6,7,"7+"]},"options":{"responsive":true,"maintainAspectRatio":true,"aspectRatio":2,"plugins":{"labels":false,"legend":{"display":false},"tooltip":{"enabled":true}},"elements":{"line":{"borderColor":"rgba(0,0,0,0)","borderWidth":1}},"layout":{"padding":{"top":30,"bottom":1,"right":1,"left":1}},"devicePixelRatio":2,"animation":{"duration":0}},"plugins":[{"id":"labels"},{"id":"centerText"}]}
```
Also, FWIW, this error is non-fatal and causes a lot of noise in logs. The chart will update and render correctly as soon as the element has proper dimensions.
Actually, on further thought. I believe this may actually result in a memory leak, since the `new Chart()` constructor never returns, but the Canvas element is attached to the chart configuration.
Additionally, this bug seems to occur when `padding` exceeds the available chart height (0). Removing the padding configuration seems to prevent the error from occurring.