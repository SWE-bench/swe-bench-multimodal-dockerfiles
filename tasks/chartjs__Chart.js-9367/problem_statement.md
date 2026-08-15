LTTB algorithm, screen scaling and odd width
Hi, I've found myself in front of a peculiar bug when using decimation plugin with LTTB algorithm.

I currently have 2 screens:

- Screen 1: 
  - resolution: 3840x2160
  - size: 15.6"
  - scaling: 250%
- Screen 2: 
  - resolution: 2560x1440
  - size: 27"
  - scaling: 100%

Now, if I try to run the following fiddle on my 1st screen:
https://jsfiddle.net/1tsufkh6/1/

It fails with:
![image](https://user-images.githubusercontent.com/22025789/124572782-377f4a80-de49-11eb-8ddb-bb33e6bee179.png)

From what I could investigate on my own code, in the LTTB loop:
```javascript
// Adding offset
const avgRangeStart = Math.floor((i + 1) * bucketWidth) + 1 + start;
const avgRangeEnd = Math.min(Math.floor((i + 2) * bucketWidth) + 1, count) + start;
const avgRangeLength = avgRangeEnd - avgRangeStart;

for (j = avgRangeStart; j < avgRangeEnd; j++) {
   avgX += data[j].x;
   avgY += data[j].y;
}

avgX /= avgRangeLength;
avgY /= avgRangeLength;

// Adding offset
const rangeOffs = Math.floor(i * bucketWidth) + 1 + start;
const rangeTo = Math.floor((i + 1) * bucketWidth) + 1 + start;
const {x: pointAx, y: pointAy} = data[a];
```
On the previous code, I sometimes ends up with negative avgRangeLength and rangeTo > data.length

But it only fails on the 1st screen, on the 2nd screen, no problems at all.

After playing around a bit, I found out that it happens only if the width is odd and and if the screen scaling is not 100% (some exception may occur at different scaling)

It might not really be a ChartJS issue and more a windows thing and how it performs scaling, but I prefer to report it anyway



