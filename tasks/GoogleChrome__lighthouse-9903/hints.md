Thanks for filing @gulatigautam! Good find, we should stop suggesting origins once 6 have been added. 👍 
If anyone is interested in helping us out with this, it'd be adding something along the lines of 

```js

if (preconnectLinks.length >= 6) {
  return {score: 1, warnings: preconnectLinks.length >= 8 ? [str_(UIStrings.tooManyPreconnectLinksWarning)] : []};
}
```
right at
https://github.com/GoogleChrome/lighthouse/blob/2953c0c1b62afe7cf88ba8718a221d74962d6640/lighthouse-core/audits/uses-rel-preconnect.js#L135-L139
Thanks @patrickhulce Even before we made the change, we noticed that the report shows different urls every time we run it. We picked the most common ones and added those. Just curious, How does Lighthouse pick the ones to show in this suggestion? Does it depend on that specific run of the report and that's why the suggestions might change every time?
Ok, i will take care of it