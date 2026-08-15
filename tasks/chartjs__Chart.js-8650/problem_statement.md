The rightmost data point gets cut off for line chart
## Expected Behavior
Line chart will be displayed in full from the first (left) to last (rightmost) data point. 

## Current Behavior
The data point to the far right gets cropped off. 
But the tooltip is displayed fine. 




<img width="1376" alt="Screenshot 2019-07-29 at 18 58 55" src="https://user-images.githubusercontent.com/35506344/62070777-17918600-b233-11e9-8f0a-fcfb41ff6fd8.png">


## Steps to Reproduce (for bugs)
This is a working example of this bug: 
https://codepen.io/LeoU/pen/gVLybO

## Context
I made a basic line chart using Chart.js version 2.8.0

## Environment

* Chart.js version: 2.8.0
* Browser name and version: Chrome on Mac: 75.0.3770.142

I've seen elsewhere that zoom plug-in has a known issue where dots get cropped off. But I am not using zoom or any other plug-in. 

