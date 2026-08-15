It looks like the problem is here:
https://github.com/openlayers/openlayers/blob/af9f26b9d343e5496ea44a729265c4002616b240/src/ol/interaction/Modify.js#L843
`uid` should be geometry dependent:
```js
let uid = getUid(segmentDataMatch.geometry);
```
@michalzielanski If this does not break any tests or examples, can you create a pull request with this change? Your suggested change makes sense to me.
Yes, I will create a pull request tomorrow.