 Pre-release v3.0.0-rc.3 - scatter chart: Render Graph Error on  scatter :  RangeError: ...


## Expected Behavior

Error: Render Graph Error on  scatter :  RangeError: minimumFractionDigits value is out of range.

![Bildschirmfoto 2021-03-24 um 07 20 56](https://user-images.githubusercontent.com/30198737/112266299-161c9900-8c74-11eb-9ea9-9c05719f195a.png)



this.chart.options.locale = 'de_DE'

```
  numeric(tickValue, index, ticks) {
    if (tickValue === 0) {
      return '0';
    }
    const locale = this.chart.options.locale;
    let notation;
    let delta = tickValue;
    if (ticks.length > 1) {
      const maxTick = Math.max(Math.abs(ticks[0].value), Math.abs(ticks[ticks.length - 1].value));
      if (maxTick < 1e-4 || maxTick > 1e+15) {
        notation = 'scientific';
      }
      delta = calculateDelta(tickValue, ticks);
    }
    const logDelta = log10(Math.abs(delta));
    const numDecimal = Math.max(Math.min(-1 * Math.floor(logDelta), 20), 0);
    const options = {notation, minimumFractionDigits: numDecimal, maximumFractionDigits: numDecimal};
    Object.assign(options, this.options.ticks.format);
    return formatNumber(tickValue, locale, options);
  },
```
## Current Behavior

 ---> **locale undefined**
```
return formatNumber(tickValue, locale, options);
```

## Environment

* Chart.js version:  Pre-release v3.0.0-rc.3
* Browser name and version: any


