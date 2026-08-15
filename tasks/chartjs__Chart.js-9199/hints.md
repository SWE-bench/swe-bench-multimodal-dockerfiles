@danielgindi during v3 development, I do not recall changing the rtl adapters. They are still used in both the legend and tooltip plugins. It looks like there is one line where the `textAlign` is not translated. https://github.com/chartjs/Chart.js/blob/master/src/plugins/plugin.legend.js#L374

I think this should become
```javascript
textAlign: rtlHelper.textAlign(legendItem.textAlign)
```

As an immediate work-around, you can override the `generateLabels` callback to return the correct alignment. Example: https://codepen.io/etimberg/pen/rNyYggP
@etimberg well there is a new `_textX` function which is not rtl aware on itself (but may expect rtl-normalized arguments?)

Also I was mistaken about `renderText` and the `lines`, as the canvas context automatically starts from the right based on the alignment passed so the arguments need to be rtl-ed, not the function itself.
Which means you may be right and the `textAlign` is the whole issue here :-)

Your fix seems to work fine!

I'll wait for it to be fixed on `master` so I don't have regressions when updating.
I quickly tested my fix, but it broke two tests when the `textAlign` is directly set in the options. I think you are correct that `_textX` will need to be updated as well. 