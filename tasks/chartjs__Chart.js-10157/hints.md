@kurkle @LeeLenaleee I traced this a bit. It's caused by https://github.com/chartjs/Chart.js/blob/master/src/controllers/controller.bar.js#L543-L545

When the chart is 150px high with the base at the bottom, the bar draws from 175px -> 125px. It looks like this code implicitly halves the size of the min bar length. This was added way back in https://github.com/chartjs/Chart.js/pull/7642

Looking again at #7642, it might work to change the `base` to be `actualBase` when the base is hidden and `minBarLength` is applying since we want to apply the bar length from the scale base.

Thoughts?
Maybe we need another option to configure that behavior. If the scale can go negative, then the current behavior could be desired. 
yaeh, it's been there for a long time and I don't recall a lot of issues with the min bar length feature so presumably it's working the way people expect
I've got a super minimal working solution right now that keeps the base within the chart area but not sure if it has broken other tests

```javascript
if (Math.abs(size) < minBarLength) {
  size = barSign(size, vScale, actualBase) * minBarLength;
  if (value === actualBase) {
    base -= size / 2;
  }
  const {right, left, top, bottom} = this.chart.chartArea;
  const max = vScale.axis === 'x' ? right : bottom;
  const min = vScale.axis === 'x' ? left : top;
  base = Math.max(Math.min(base, max), min);
  head = base + size;
}
```
If that works, I think it still needs to use the scale boundaries, to make it work with [stacked scales](https://www.chartjs.org/docs/latest/samples/scales/stacked.html)
Good point. This is also working but I'd need to test if it works with stacked scales. I'm not familiar with how the scale boundaries work so not sure if this is the right way to do it.

```javascript
if (Math.abs(size) < minBarLength) {
  size = barSign(size, vScale, actualBase) * minBarLength;
  if (value === actualBase) {
    base -= size / 2;
  }
  const start = vScale.getPixelForDecimal(0);
  const end = vScale.getPixelForDecimal(1);
  const min = Math.min(start, end);
  const max = Math.max(start, end);
  base = Math.max(Math.min(base, max), min);
  head = base + size;
}
```
I think you can use top,left,bottom,right of the scale. Its a layout box afterall.
Edit: your solution is cleaner though :)
my thinking on using the decimal 0/1 was that I can avoid checking if it's vertical or horizontal