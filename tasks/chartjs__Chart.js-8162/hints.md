Can you please provide a working sample since the config you are using is giving a correct chart: https://jsfiddle.net/Leelenaleee/yftv0nLb/3/
@LeeLenaleee 
> Can you please provide a working sample since the config you are using is giving a correct chart:

Negativ, when i try this with a simple sample (as you do), it works.

It doesn't always happen, depending on the load on the rendering process. Could have something to do with the animation, but even if I turn it off, it happens occasionally.

see: http://www.ipscon.com/transfer/testcase.mp4

Sorry


It looks like it's a timing problem because when I try to debug the title and legend are rendered multiple times.

![Bildschirmfoto 2020-12-09 um 20 03 50](https://user-images.githubusercontent.com/30198737/101675422-0fb63880-3a5a-11eb-8ba5-811aece23ca0.png)

Woah! This is interesting. I think it is caused by this code. I believe @kurkle removed `chart.legend` and so it is always added again.

https://github.com/chartjs/Chart.js/blob/649f8153281bf5dfa17a02d8d7923b3e699177a0/src/plugins/plugin.legend.js#L677-L679
@etimberg, @kurkle 
Thanks, do I have to wait for the next beta version or can I fix it in another way?
Does this change affect the title and legend?

@etimberg I'm not sure if that is correct:

https://github.com/chartjs/Chart.js/blob/649f8153281bf5dfa17a02d8d7923b3e699177a0/src/plugins/plugin.legend.js#L641

@zibous are you calling `update` from a timer? 
> @zibous are you calling `update` from a timer?

Negativ. Only `chart = new Chart(ctx, graphOptions);`
But only occurs when the browser is under load and the rendering process takes longer. It works in a simple application.
ok, can you try with `responsive: false` if that hides the issue (just to narrow things down)?
@kurkle 
Yes this is working (title and legend) no only once. But the chart is not scaled on the card.

![Bildschirmfoto 2020-12-10 um 09 58 16](https://user-images.githubusercontent.com/30198737/101749781-6c533b00-3ace-11eb-97b3-f8ee0556d517.png)

It looks like that `responsive: true` has problems.

```
Chart.defaults.responsive = true;
Chart.defaults.maintainAspectRatio = false;
Chart.defaults.animation = 0;
Chart.defaults.locale = this.chart_locale;
```

Also Error on "arc" when  `Chart.defaults.responsive = true`, not when `Chart.defaults.responsive = false`

```

ctx.beginPath();
	if (circular) {
		ctx.arc(scale.xCenter, scale.yCenter, radius, 0, TAU);  <--- ERROR radius = -39
	} else {
		pointPosition = scale.getPointPosition(0, radius);
		ctx.moveTo(pointPosition.x, pointPosition.y);
		for (let i = 1; i < valueCount; i++) {
			pointPosition = scale.getPointPosition(i, radius);
			ctx.lineTo(pointPosition.x, pointPosition.y);
		}
	}

Uncaught DOMException: Failed to execute 'arc' on 'CanvasRenderingContext2D': The radius provided (-39) is negative.
    at drawRadiusLine (http://testserver.home:8123/hacsfiles/chart-card/chart.js?module:11228:7)
    at http://testserver.home:8123/hacsfiles/chart-card/chart.js?module:11371:6
    at Array.forEach (<anonymous>)
    at RadialLinearScale.drawGrid (http://testserver.home:8123/hacsfiles/chart-card/chart.js?module:11368:13)
    at RadialLinearScale.draw (http://testserver.home:8123/hacsfiles/chart-card/chart.js?module:4882:6)
    at Object.draw (http://testserver.home:8123/hacsfiles/chart-card/chart.js?module:4895:9)
    at Chart.draw (http://testserver.home:8123/hacsfiles/chart-card/chart.js?module:5750:14)
    at Chart.render (http://testserver.home:8123/hacsfiles/chart-card/chart.js?module:5729:7)
    at Chart.update (http://testserver.home:8123/hacsfiles/chart-card/chart.js?module:5677:6)
    at Chart._resize (http://testserver.home:8123/hacsfiles/chart-card/chart.js?module:5489:7)
drawRadiusLine @ chart.js?module:11228
(anonymous) @ chart.js?module:11371
drawGrid @ chart.js?module:11368
draw @ chart.js?module:4882
draw @ chart.js?module:4895
draw @ chart.js?module:5750
render @ chart.js?module:5729
update @ chart.js?module:5677
_resize @ chart.js?module:5489
resize @ chart.js?module:5463
listener @ chart.js?module:5938
(anonymous) @ chart.js?module:1710
(anonymous) @ chart.js?module:34
(anonymous) @ chunk.af43f6ec356055cbfe65.js:1
requestAnimationFrame (async)
window.requestAnimationFrame @ chunk.af43f6ec356055cbfe65.js:1
(anonymous) @ chart.js?module:32
(anonymous) @ chart.js?module:1722
```
Do you get any errors when multiple legends are shown? That would explain it if there is an error before `chart.legend` is set, but the box got added already.

It could be the new `start` hook that gets called multiple times in some situation.


@kurkle 
> Do you get any errors when multiple legends are shown? That would explain it if there is an error before `chart.legend` is set, but the box got added already.

Negativ, no error.  It is based on `Chart.defaults.responsive = true`, inital all is ok, than comes resize and the title and legend are twice.

see: http://www.ipscon.com/transfer/testcase.mp4

The `Uncaught DOMException: Failed to execute 'arc' on 'CanvasRenderingContext2D':` happens only when
i resize the browser to a iPhoneX screen.



Would it be easy to add a plugin in your config?
```js
{
  id: 'debug',
  start(chart) { console.log('start' + chart.id); },
  stop(chart) { console.log('stop' + chart.id); },
  beforeUpdate(chart) { console.log('beforeUpdate' + chart.id); }
}
```

I'm guessing `beforeUpdate` before `start` or multiple `start` calls (without `stop`).
@kurkle 

```
Chart.register({
    id: "debug",
    start(chart) {
        console.log("start",new Date().toISOString(),ct, 'id:',chart.id);
    },
    stop(chart) {
        console.log("stop",new Date().toISOString() ,ct, 'id:',chart.id);
    },
    beforeUpdate(chart) {
        console.log("beforeUpdate",new Date().toISOString() ,ct, 'id:',chart.id);
    }
});

```

Results: i have **14 charts** on the page

|id|event|date|timestamp | id |
|--|----|-----|-----|----|
|1|start| 2020-12-10T10:02:51.479Z| pie | 0|
|3|beforeUpdate| 2020-12-10T10:02:51.487Z| pie | 0|
|1|start| 2020-12-10T10:02:51.508Z| pie | 1
|3|beforeUpdate| 2020-12-10T10:02:51.514Z| pie | 1|
|1|start| 2020-12-10T10:02:51.532Z| pie | 2
|3|beforeUpdate| 2020-12-10T10:02:51.536Z| pie | 2|
|1|start| 2020-12-10T10:02:51.542Z| pie | 3
|3|beforeUpdate| 2020-12-10T10:02:51.548Z| pie | 3|
|1|start| 2020-12-10T10:02:51.558Z| pie | 4
|3|beforeUpdate| 2020-12-10T10:02:51.560Z| pie | 4|
|1|start| 2020-12-10T10:02:51.567Z| pie | 5
|3|beforeUpdate| 2020-12-10T10:02:51.570Z| pie | 5|
|1|start| 2020-12-10T10:02:51.597Z| pie | 6
|3|beforeUpdate| 2020-12-10T10:02:51.600Z| pie | 6|
|1|start| 2020-12-10T10:02:51.604Z| pie | 7
|3|beforeUpdate| 2020-12-10T10:02:51.607Z| pie | 7|
|1|start| 2020-12-10T10:02:51.613Z| pie | 8
|3|beforeUpdate| 2020-12-10T10:02:51.615Z| pie | 8|
|1|start| 2020-12-10T10:02:51.622Z| pie | 9
|3|beforeUpdate| 2020-12-10T10:02:51.624Z| pie | 9|
|1|start| 2020-12-10T10:02:51.632Z| pie | 10
|3|beforeUpdate| 2020-12-10T10:02:51.635Z| pie | 10|
|1|start| 2020-12-10T10:02:51.640Z| pie | 11
|3|beforeUpdate| 2020-12-10T10:02:51.642Z| pie | 11|
|1|start| 2020-12-10T10:02:51.817Z| pie | 12
|3|beforeUpdate| 2020-12-10T10:02:51.821Z| pie | 12|
|1|start| 2020-12-10T10:02:51.826Z| pie | 13
|3|beforeUpdate| 2020-12-10T10:02:51.828Z| pie | 13|
|1|start| 2020-12-10T10:02:51.833Z| pie | 14
|3|beforeUpdate| 2020-12-10T10:02:51.834Z| pie | 14|
|1|start| 2020-12-10T10:02:51.839Z| pie | 15
|3|beforeUpdate| 2020-12-10T10:02:51.841Z| pie | 15|
|1|start| 2020-12-10T10:02:51.845Z| pie | 16
|3|beforeUpdate| 2020-12-10T10:02:51.847Z| pie | 16|
|1|start| 2020-12-10T10:02:51.851Z| pie | 17
|3|beforeUpdate| 2020-12-10T10:02:51.853Z| pie | 17|
|1|start| 2020-12-10T10:02:51.965Z| pie | 6
|3|beforeUpdate| 2020-12-10T10:02:51.966Z| pie | 6|
|1|start| 2020-12-10T10:02:51.973Z| pie | 7
|3|beforeUpdate| 2020-12-10T10:02:51.974Z| pie | 7|
|1|start| 2020-12-10T10:02:51.982Z| pie | 8
|3|beforeUpdate| 2020-12-10T10:02:51.983Z| pie | 8|
|1|start| 2020-12-10T10:02:51.986Z| pie | 9
|3|beforeUpdate| 2020-12-10T10:02:51.987Z| pie | 9|
|1|start| 2020-12-10T10:02:51.993Z| pie | 10
|3|beforeUpdate| 2020-12-10T10:02:51.994Z| pie | 10|
|1|start| 2020-12-10T10:02:51.999Z| pie | 11
|3|beforeUpdate| 2020-12-10T10:02:52.000Z| pie | 11|
|3|beforeUpdate| 2020-12-10T10:02:52.049Z| pie | 12|
|3|beforeUpdate| 2020-12-10T10:02:52.053Z| pie | 13|
|3|beforeUpdate| 2020-12-10T10:02:52.059Z| pie | 14|
|3|beforeUpdate| 2020-12-10T10:02:52.063Z| pie | 15|
|3|beforeUpdate| 2020-12-10T10:02:52.069Z| pie | 16|
|3|beforeUpdate| 2020-12-10T10:02:52.075Z| pie | 17|
|1|start| 2020-12-10T10:02:52.090Z| pie | 18
|3|beforeUpdate| 2020-12-10T10:02:52.093Z| pie | 18|
|1|start| 2020-12-10T10:02:52.101Z| pie | 19
|3|beforeUpdate| 2020-12-10T10:02:52.103Z| pie | 19|
|1|start| 2020-12-10T10:02:52.111Z| pie | 20
|3|beforeUpdate| 2020-12-10T10:02:52.113Z| pie | 20|
|1|start| 2020-12-10T10:02:52.121Z| pie | 21
|3|beforeUpdate| 2020-12-10T10:02:52.123Z| pie | 21|
|1|start| 2020-12-10T10:02:52.128Z| pie | 22
|3|beforeUpdate| 2020-12-10T10:02:52.130Z| pie | 22|
|1|start| 2020-12-10T10:02:52.195Z| pie | 23
|3|beforeUpdate| 2020-12-10T10:02:52.196Z| pie | 23|
|1|start| 2020-12-10T10:02:52.206Z| pie | 24
|3|beforeUpdate| 2020-12-10T10:02:52.208Z| pie | 24|
|1|start| 2020-12-10T10:02:52.212Z| pie | 25
|3|beforeUpdate| 2020-12-10T10:02:52.214Z| pie | 25|
|1|start| 2020-12-10T10:02:52.218Z| pie | 26
|3|beforeUpdate| 2020-12-10T10:02:52.220Z| pie | 26|
|1|start| 2020-12-10T10:02:52.291Z| pie | 27
|3|beforeUpdate| 2020-12-10T10:02:52.292Z| pie | 27|
|1|start| 2020-12-10T10:02:52.351Z| pie | 28
|3|beforeUpdate| 2020-12-10T10:02:52.353Z| pie | 28|
|1|start| 2020-12-10T10:02:52.454Z| pie | 29
|3|beforeUpdate| 2020-12-10T10:02:52.457Z| pie | 29|
|1|start| 2020-12-10T10:02:52.529Z| pie | 30
|3|beforeUpdate| 2020-12-10T10:02:52.532Z| pie | 30|
|1|start| 2020-12-10T10:02:52.544Z| pie | 31
|3|beforeUpdate| 2020-12-10T10:02:52.547Z| pie | 31|
|1|start| 2020-12-10T10:02:52.560Z| pie | 32
|3|beforeUpdate| 2020-12-10T10:02:52.563Z| pie | 32|
|1|start| 2020-12-10T10:02:52.572Z| pie | 13
|1|start| 2020-12-10T10:02:52.580Z| pie | 33
|3|beforeUpdate| 2020-12-10T10:02:52.584Z| pie | 33|
|1|start| 2020-12-10T10:02:52.690Z| pie | 34
|3|beforeUpdate| 2020-12-10T10:02:52.696Z| pie | 34|
|1|start| 2020-12-10T10:02:52.726Z| pie | 13
|1|start| 2020-12-10T10:02:52.827Z| pie | 35
|3|beforeUpdate| 2020-12-10T10:02:52.830Z| pie | 35|
|1|start| 2020-12-10T10:02:52.882Z| pie | 12
|3|beforeUpdate| 2020-12-10T10:02:52.884Z| pie | 12|
|3|beforeUpdate| 2020-12-10T10:02:52.888Z| pie | 13|
|1|start| 2020-12-10T10:02:52.894Z| pie | 14
|3|beforeUpdate| 2020-12-10T10:02:52.895Z| pie | 14|
|1|start| 2020-12-10T10:02:52.899Z| pie | 15
|3|beforeUpdate| 2020-12-10T10:02:52.900Z| pie | 15|
|1|start| 2020-12-10T10:02:52.905Z| pie | 16
|3|beforeUpdate| 2020-12-10T10:02:52.906Z| pie | 16|
|1|start| 2020-12-10T10:02:52.911Z| pie | 17
|3|beforeUpdate| 2020-12-10T10:02:52.912Z| pie | 17|
|1|start| 2020-12-10T10:02:52.916Z| pie | 30
|3|beforeUpdate| 2020-12-10T10:02:52.918Z| pie | 30|
|1|start| 2020-12-10T10:02:52.923Z| pie | 31
|3|beforeUpdate| 2020-12-10T10:02:52.924Z| pie | 31|
|1|start| 2020-12-10T10:02:52.930Z| pie | 32
|3|beforeUpdate| 2020-12-10T10:02:52.932Z| pie | 32|
|1|start| 2020-12-10T10:02:52.940Z| pie | 33
|3|beforeUpdate| 2020-12-10T10:02:52.943Z| pie | 33|
|3|beforeUpdate| 2020-12-10T10:02:52.952Z| pie | 34|
|3|beforeUpdate| 2020-12-10T10:02:52.963Z| pie | 35|
|3|beforeUpdate| 2020-12-10T10:02:52.998Z| pie | 12|
|3|beforeUpdate| 2020-12-10T10:02:53.002Z| pie | 13|
|3|beforeUpdate| 2020-12-10T10:02:53.009Z| pie | 14|
|3|beforeUpdate| 2020-12-10T10:02:53.016Z| pie | 15|
|3|beforeUpdate| 2020-12-10T10:02:53.022Z| pie | 16|
|3|beforeUpdate| 2020-12-10T10:02:53.027Z| pie | 17|
|3|beforeUpdate| 2020-12-10T10:02:53.034Z| pie | 30|
|3|beforeUpdate| 2020-12-10T10:02:53.040Z| pie | 31|
|3|beforeUpdate| 2020-12-10T10:02:53.048Z| pie | 32|
|3|beforeUpdate| 2020-12-10T10:02:53.054Z| pie | 33|
|3|beforeUpdate| 2020-12-10T10:02:53.065Z| pie | 34|
|3|beforeUpdate| 2020-12-10T10:02:53.075Z| pie | 35|
|3|beforeUpdate| 2020-12-10T10:02:53.108Z| pie | 12|
|3|beforeUpdate| 2020-12-10T10:02:53.113Z| pie | 13|
|3|beforeUpdate| 2020-12-10T10:02:53.119Z| pie | 14|
|3|beforeUpdate| 2020-12-10T10:02:53.123Z| pie | 15|
|3|beforeUpdate| 2020-12-10T10:02:53.129Z| pie | 16|
|3|beforeUpdate| 2020-12-10T10:02:53.134Z| pie | 17|
|3|beforeUpdate| 2020-12-10T10:02:53.138Z| pie | 30|
|3|beforeUpdate| 2020-12-10T10:02:53.142Z| pie | 31|
|3|beforeUpdate| 2020-12-10T10:02:53.149Z| pie | 32|
|3|beforeUpdate| 2020-12-10T10:02:53.153Z| pie | 33|
|3|beforeUpdate| 2020-12-10T10:02:53.160Z| pie | 34|
|3|beforeUpdate| 2020-12-10T10:02:53.168Z| pie | 35|
|3|beforeUpdate| 2020-12-10T10:02:53.197Z| pie | 12|
|3|beforeUpdate| 2020-12-10T10:02:53.201Z| pie | 13|
|3|beforeUpdate| 2020-12-10T10:02:53.206Z| pie | 14|
|3|beforeUpdate| 2020-12-10T10:02:53.209Z| pie | 15|
|3|beforeUpdate| 2020-12-10T10:02:53.213Z| pie | 16|
|3|beforeUpdate| 2020-12-10T10:02:53.219Z| pie | 17|
|3|beforeUpdate| 2020-12-10T10:02:53.224Z| pie | 30|
|3|beforeUpdate| 2020-12-10T10:02:53.229Z| pie | 31|
|3|beforeUpdate| 2020-12-10T10:02:53.236Z| pie | 32|
|3|beforeUpdate| 2020-12-10T10:02:53.242Z| pie | 33|
|3|beforeUpdate| 2020-12-10T10:02:53.249Z| pie | 34|
|3|beforeUpdate| 2020-12-10T10:02:53.258Z| pie | 35|
|3|beforeUpdate| 2020-12-10T10:02:53.283Z| pie | 12|
|3|beforeUpdate| 2020-12-10T10:02:53.287Z| pie | 13|
|3|beforeUpdate| 2020-12-10T10:02:53.297Z| pie | 14|
|3|beforeUpdate| 2020-12-10T10:02:53.300Z| pie | 15|
|3|beforeUpdate| 2020-12-10T10:02:53.304Z| pie | 16|
|3|beforeUpdate| 2020-12-10T10:02:53.309Z| pie | 17|
|3|beforeUpdate| 2020-12-10T10:02:53.315Z| pie | 30|
|3|beforeUpdate| 2020-12-10T10:02:53.320Z| pie | 31|
|3|beforeUpdate| 2020-12-10T10:02:53.327Z| pie | 32|
|3|beforeUpdate| 2020-12-10T10:02:53.332Z| pie | 33|
|3|beforeUpdate| 2020-12-10T10:02:53.341Z| pie | 34|
|3|beforeUpdate| 2020-12-10T10:02:53.350Z| pie | 35|
looks like there are 36 charts constructed? I'm not able to reproduce the issue.
How many of those charts produced the error when you logged the above?
> How many of those charts produced the error when you logged the above?

All except **LINE Chart**, where it does not occur

> looks like there are 36 charts constructed?

I don't understand why this is the case, because it would mean that if there are 12 chart's are generated 3 times each.

```
 if (chart) {
    // be shure that no chart exits before create..
    chart.destroy(); 
    chart = null;
 }
chart = new Chart(ctx, graphOptions);
```

If you remove the `chart.destroy()` line, you should get an error when a second chart is constructed for the same canvas element. Could help finding out why.

@kurkle 
> If you remove the `chart.destroy()` line, you should get an error when a second chart is constructed for the same canvas element. 

chart.destroy () is required:

`Canvas is already in use. Chart with ID '1' must be destroyed before the canvas can be reused.`
That is the error I was talking about. You should not be constructing the chart multiple times on same canvas. 
Thats something to do with the framework you are using for the elements / components.

Back to Chart.js:
No `stop` events on your log, even though you are calling `destroy`. <del>That is interesting.</del>

Already forgot the stop event only occurs when plugin is disabled at chart runtime, `destroy` is called when its destroyed.
> No `stop` events on your log, even though you are calling `destroy`. That is interesting.
But on a simple chart..


One last thing to try:

If using UMD build, add somewhere before any charts are constructed (run once):
```js
delete Chart.Title.start;
```
or ESM (not tested, but should work right after `import {..., Title} from 'chart.js'`): 
```js
delete Title.start;
```
> If using UMD build, add somewhere before any charts are constructed (run once):

?? UMD build

```
delete Chart.Title.start;
chart = new Chart(ctx, graphOptions);
```

Nothing happens, same as before.
Need a reproduce of this to be able to find the cause.
@kurkle 

Now i am shure, that only on call  `chart = new Chart(ctx, graphOptions);` w/o `chart.destroy(); `

```
2020-12-10T19:33:21.867Z HASS: Create chart pie339 pie
chart-card.js:103 2020-12-10T19:33:21.871Z Create new chart pie339 pie
```
Result:
- On Firefox all is working perfect.
- On Safari and Chrome the legend and title will be rendered multiple.
- `responsive: false` works for all browsers.
-  initial works for all browsers, but after responsive mode Safari and Chrome fails

 


> Need a reproduce of this to be able to find the cause.

@kurkle, @etimberg 

Here is the testcase:
http://www.ipscon.com/test/

Download:
http://www.ipscon.com/transfer/test.zip

Load the page `http://www.ipscon.com/test/` and resize the browser window. 
After resize, sometimes the legend and title are multiple.

Sorry, only a QAD way, but maybe it will help.


I can reproduce this locally. I see the title getting duplicated as well. What seems to happen is that on the call to `notifyPlugins` inside of the resize handler, there are no `descriptors`, so the cache needs to be built. As part of building this cache, we notify the plugins that they are starting. Sometimes when this occurs, there are no previous plugins stored (i.e. `_oldCache` is undefined), the `PluginService` class assumes that all the plugins are starting and notifies them. This creates a 2nd box and adds it to the chart because the legend and title plugins do not check if they are already attached to the chart.

I haven't yet figured out why the descriptors are gone. My thinking right now is that if the resize messages get buffered into the same animation frame, via `throttled`, two `updates()` in a row could cause the cache to be invalidated twice in a row such that the old list of plugins is cleared.

| Time | PluginService._cache | PluginService._oldCache |
| ---- | ---- | ---- |
| Before first invalidate | [plugin1, plugin2, ...] | `undefined` |
| After first invalidate | `undefined` | `[plugin1, plugin2, ...]` |
| After 2nd invalidate | `undefined` | `undefined` |

If an update occurs now, all the plugins look new and are re-started. But since the notify process never took place, the plugins were never stopped.

If this is the case, some thoughts on fixing this:

1. If the cache is already invalidated, subsequent calls to `invalid` inside the same update do nothing
2. Legend / Title plugins should check if `chart.legend` / `chart.title` exist before creating a new box on the chart.

I prototyped a fix to change `invalidate` to the following and it seemed to stop the issue from occurring. I'm not sure if this breaks anything else.

```javascript
invalidate() {
	if (!isNullOrUndef(this._cache)) {
		this._oldCache = this._cache;
		this._cache = undefined;
	}
}
```