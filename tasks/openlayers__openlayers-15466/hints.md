:package: Preview the website for this branch here: https://deploy-preview-14609--ol-site.netlify.app/.
Wouldn't it add more flexibility to add boolean `ignorePlacement` options to `ol.style.Image` and `ol.style.Text`? That's equivalent to [icon-ignore-placement](https://www.mapbox.com/mapbox-gl-js/style-spec/#layout-symbol-icon-ignore-placement) and [text-ignore-placement](https://www.mapbox.com/mapbox-gl-js/style-spec/#layout-symbol-text-ignore-placement) in the Mapbox Style specification.

To only declutter text, you would then configure all your `ol.style.Image` styles with `ignorePlacement: true`.
If `ignorePlacement` includes the ability to be `declutter`ed, yes, this would work more granularly. Thanks!
yes ,draw lessons from mapbox ，Good things
Talked to @ahocevar about this and we agree that probably allowOverlap is a better term here, we did find https://github.com/mapbox/mapbox-gl-js/pull/486 which gives an insight into the two different options, but we think a single option will suffice for now and allowOverlap is the better term for disabling the decluttering.
@bartvde Would this replace `declutter`, or be used in conjunction with it?
Good question @tomchadwin I'm not 100% sure, I think the option we are talking about is at the style level, and declutter is currently at the layer level. So I'm guessing this is in conjunction. @ahocevar can you confirm?
@bartvde That's my understanding, yes. If so, is the logic that `allowOverlap` only has an effect if `declutter` is set? No need to answer - it's the result I want (independent decluttering of text and image styles).
Yes indeed that would make sense to me
Yes, `allowOverlap` on the style will only have an effect when `declutter` is set on the layer.
This issue has been automatically marked as stale because it has not had recent activity. It will be closed if no further activity occurs. Thank you for your contributions.

Hi,
was the ignorePlacement  implemented? We can't find it in 6.0.1.

We have markers (where there might be multiple in a small area overlapping, which is ok) on a map and want text next to a marker, only if there is no other text or no other markers. We want just the text to declutter (and no overlapping of other markers), but can't seem to find a clean workaround.

Currently we have the 
1.) pins on one layer and 
2.) the text+"pin_rectangles (placeholders for the markers, which are on the 1st layer)" on another. 

We have high z-index on the pin_rectangle and low on the text, but the pin_rectangle, when overlapping with another pin_rectangle also gets decluttered and then text shows over the initial one as a consequence.

Any suggestions would be highly appreciated.
Thanks!
This has not been implemented yet, but we're still accepting pull requests.
@ahocevar I am likely not experienced enough to be of any help here. Sorry. :(

Any suggestions for quick workarounds for now? Seems @tomchadwin had an idea  (quote: "I appreciate that this can be worked around,").......  as our workaround does not really work. :(

Thank you
The only workaround I meant was what you have implemented - labels and markers in different layers.
@tomchadwin thank you for your reply. Unfortunately that workaround - at least the way we have implemented it - is not clean, as the placeholders for the pins, which should block out the text from other pins, also get decluttered. And for the display to work properly we need the placeholders to stay, even if they overlap each other and only the text decluttered.
I can't think of a way to solve that, I'm afraid. Sorry.
@tomchadwin  :( thank you
Same here. We've been looking for such feature for long time because we also have markers with text labels and we are interested in decluttering text only for that layer. It would be nice to have an option to choose. At the moment we have to keep off the Openlayers decluttering feature and implement text decluttering ourselves which is not ideal at all.
Same here, this feature would be of great help.
This would be much easier to implement now than when I replied last time, because decluttering could now be set per geometry instead of per layer. With an `ignorePlacement` option on the `ImageStyle` and `TextStyle`, the `GEOMETRY_RENDERERS` in `renderer/vector.js` could decide for each style whether to render to the standard builder group or the declutter builder group.

If anyone wants to take this on, I'd be happy to review a pull request. Or see my [GitHub profile](https://github.com/ahocevar) for sponsoring options.

Please see pull request 13566.

It adds a property `declutterMode` to `ImageStyle`:
* `'declutter'`: declutter as before (same as mapbox `icon-allow-overlap = false` and `icon-ignore-placement = false`)
* `'obstacle'`: draw image, but still add it as obstacle (same as mapbox `icon-allow-overlap = true` and `icon-ignore-placement = false`)
* `'none'`: no decluttering (same as mapbox `icon-allow-overlap = true` and `icon-ignore-placement = true`)

Not implemented:
* mapbox `icon-allow-overlap = false` and `icon-ignore-placement = true`: is there a use case for this?
* `declutterMode` for `TextStyle` (but can easily be added): is there a use case for this?

This allows to e.g. show all tracks, but only non-overlapping labels in a map:
![image](https://user-images.githubusercontent.com/59872815/162892344-b0296715-ba76-465c-b8fd-cd954b597de1.png)

This is great! Thanks a lot!

Currently, I am using the work-around with labels and markers in different layers (as suggested in the thread). But I am really glad that this won't be necessary in the future.


> declutterMode for TextStyle (but can easily be added): is there a use case for this?

Maybe, I do have a use case for this.

I would like to create a point feature where the point is replaced by a small image. Additionally, there should be a label for that icon that gets decluttered.

The style would look like this:
```typescript
  const style = new Style({
    image: new Icon({
      imgSize: [25, 25],
      src: "someImage.svg",
      declutterMode: "none"
    }),
    text: new Text({
      text: "someLabel",
      declutterMode: "declutter"
    }),
  })

```

Not sure, if this would be the correct way to define that. But it would use both Image and Text (and only the text needs to be decluttered). 

Although, I don't quite get why this is not necessary in your example. Are the labels also ImageStyles? Could you maybe explain how you defined the features and their styles in the example that you provided?




The main problem I'm trying to solve is to have icons that are always drawn (overlapping each other), but still present an obstacle for decluttering, so that a label is never drawn on top of the icon (as also requested by @[pir1981](https://github.com/pir1981)). This is currently not possible.

However, by solving this problem, the PR solves the following problems:
* show all icons, but only labels that don't overlap the icons and each other (the text style is always decluttered, if the layer has `declutter: true`):
```javascript
new VectorLayer({
  ...
  style: new Style({
    image: new Icon({
      ...
      declutterMode: "obstacle",
    }),
    text: new Text({
      ...
    }),
  }),
  declutter: true,
});
```
* show all icons, declutter labels, but don't care if they overlap the icons: as above, but `declutterMode: "none",` (this is currently also possible, when splitting the styles onto two layers, an icon layer with `declutter: false` and a text layer with `declutter: true`) 
* declutter both icons and labels: same as now (layer with `declutter: true` with image style with undefined `declutterMode` or `declutterMode: "declutter"`)

All `declutterMode`s could also be mixed in one layer (with `declutter: true`), e.g. the point features are styled as follows:
* a light colored circle larger then the primary icon, which can be overlapped by the labels (`Circle` with `declutterMode: "none"`)
* the primary icon, which must always be displayed, even if overlapping other icons, but which must not be overlapped by labels (`Icon` with `declutterMode: "obstacle"`, must have the highest `zIndex`!)
* a secondary icon indicating the state of the object (offset from the primary icon), which should only be displayed, if there is available space, i.e. it is not overlapping primary icons or labels (`Icon` with `declutterMode: "declutter"`)
* the label, which must not overlap any of the icons or each other (`Text`)
* (by assigning `zIndex`es to the secondary icon and label style, it is possible to specify which takes precedence)

One special case is, if we have two or more (logical) layers (e.g. aircrafts and ships) and don't want either icons to be overlapped by either labels. In this case we need to split the layers so that all the icons are in layers on top of the label layers, e.g.:
* aircraft icon layer (`declutter: true`, `declutterMode: "obstacle"`) (top)
* ship icon layer (as above)
* aircraft label layer (`declutter: true`)
* ship label layer (as above) (bottom)

I see no use case, where the `Text`s in a layer with `declutter: true` would not be decluttered, hence a `declutterMode` for `Text` is not supported. It is decluttered, if and only if it is in a layer with `declutter: true`.

Your explanation is very helpful. Thanks!
@ahocevar: I want to add a PR for the declutterMode in ol-mapbox-style. However, there is no openlayers version I can depend on that includes the declutterMode. Can you create an openlayers test/beta version to depend on? Or is there another way to do it?
Just use `ol@dev`, that's fine. Ideally, ol-mapbox-style should continue to work with older versions.