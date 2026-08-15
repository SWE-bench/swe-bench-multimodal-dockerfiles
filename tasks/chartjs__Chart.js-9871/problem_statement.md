Polar Area Chart with single element is not clickable nor does it show a tooltip over colored area


## Expected Behavior
A PolarArea chart with a single item should show a tooltip and be clickable just like PolarArea charts with multiple items

## Current Behavior
The single item renders as a complete circle and the only area of the chart sensitive to mouseover is the vertical line which starts the item arc but that is only 1-2 pixels wide

## Possible Solution


## Steps to Reproduce
Create a Polar Area chart with just a single item. It will fill the entire circle but inly the leading edge will respond to mouseover

## Context
The chart with only a single segment is not usable as is since the end user is unable to click the segment to get more details

## Environment
Chart.js versions: 3.6.0 and 3.5.1
Browsers: Chrome (95.0.4638.69), Brave (1.31.88), Firefox (93.0)
Project link: Not available

![screenshot-737](https://user-images.githubusercontent.com/81261942/139717879-7797fb43-b437-4ee0-bea6-ca34cbf75a23.png)
![screenshot-738](https://user-images.githubusercontent.com/81261942/139717896-bd5ca61c-14a6-43f3-a5d1-d8f1a79977c0.png)

