RangeError: minimumFractionDigits value is out of range. (Thrown from `new Chart()`) 


Hi all,

Thanks for the great library. I don't have a repro for this (famous last words) but it seems to happen when a specific chart is created. The chart library is calculating `NaN` for the chart height (even though it should likely just be `0`)

## Expected Behavior

Error should not be thrown.

## Current Behavior


```
RangeError: minimumFractionDigits value is out of range.
    at new NumberFormat (<anonymous>)
    at getNumberFormat (helpers.segment.js:2155)
    at formatNumber (helpers.segment.js:2161)
    at LinearScale.numeric (chart.esm.js:3177)
    at callback (helpers.segment.js:89)
    at LinearScale.generateTickLabels (chart.esm.js:3710)
    at LinearScale._convertTicksToLabels (chart.esm.js:3870)
    at LinearScale.update (chart.esm.js:3620)
    at fitBoxes (chart.esm.js:2710)
    at Object.update (chart.esm.js:2827)
    at Chart._updateLayout (chart.esm.js:5460)
    at Chart.update (chart.esm.js:5441)
    at new Chart (chart.esm.js:5180)
    at SafeSubscriber._next (chart.component.ts:285)
    at SafeSubscriber.__tryOrUnsub (Subscriber.js:183)
```

First call to getNumberFormat:
![image](https://user-images.githubusercontent.com/362329/116908742-4101f180-ac11-11eb-9c15-f0e808189ccb.png)

Second call to getNumberFormat:
![image](https://user-images.githubusercontent.com/362329/116908782-4c551d00-ac11-11eb-8b79-dfbe585b56c9.png)


Intermediate values during chart construction:
![image](https://user-images.githubusercontent.com/362329/116909229-e9b05100-ac11-11eb-9e0c-21c0c0ca3f81.png)



RangeError is thrown.

## Possible Solution


## Steps to Reproduce


## Context


## Environment

* Chart.js version: ^3.2.1
* Browser name and version:
```
Google Chrome | 90.0.4430.93 (Official Build) (x86_64)
-- | --
Revision | 4df112c29cfe9a2c69b14195c0275faed4e997a7-refs/branch-heads/4430@{#1348}
OS | macOS Version 11.2.3 (Build 20D91)
JavaScript | V8 9.0.257.23
User Agent | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)


```
* Link to your project:
None yet.
