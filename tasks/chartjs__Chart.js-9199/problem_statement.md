Rtl regresssions in v3
## Expected Behavior
`rtl: true` in legend should draw it rtl (box to the right of the text) like in charts v2.

## Current Behavior
text goes off screen, not rendered at all.

## Possible Solution
I have no idea. The refactor to v3 completely changed (ruined?) the original rtl helper that I've written.  
There are major regressions, like `renderText` rendering multiples lines always aligned to the left, while it should be alignment-aware.
And everything else has changed.

Looks like `_textX` should be updated to be rtl-aware.

## Steps to Reproduce
https://codepen.io/danielgindi/pen/eYveogd

## Context
Cannot upgrade to v3 due to rtl issues.

## Environment
* Chart.js version: 3.3.2
* Chrome 91.0.4472.77

