It is indeed broken for negative scales. This is something that @mike-000 might be interested in fixing, since they made the change that introduced negative scales. There is another issue with negative scales that can be seen in the above codesandbox: when panning the map, the icon disappears.

For other scales, just make sure to configure your vector layer with a `renderBuffer` big enough to cover your symbol size. In the codesandbox you provided, `500` might be a good value. Also, to get hit detection for the drawn icon and not just its bounding box, configure the icon style with `crossOrigin: anonymous`.
I cannot see either of those issues in https://openlayers.org/en/latest/examples/icon-scale.html (observe change of cursor during pointermove on the lower fish, or click for a popup) - but even if I replace the penguin with the fish in the codesandbox both problems persist.
Thanks, @ahocevar, I updated the sandbox with your suggestions. I'm using more reasonably sized icons hosted on the same server.
I noticed the hit detection not working with some icons in my application and the negative scale is the reason.
I hadn't noticed the disappearing icons, but it is also happening in my application.

I want to add thought that both worked with 6.4.2.
@mike-000, Seems like the rotation in your example makes it work, if I remove it, the same problems occur.
As a workaround i added `rotation: Number.EPSILON` to the scaled icons then it works like it should.
Defining
```
  const rotatedOrFlipped = (
    rotation !== 0 ||
    scale[0] < 0 ||
    scale[1] < 0
  );

```
in `replayImageOrLabel_` and replacing both of the existing  `rotation !== 0` with `rotatedOrFlipped` seems to fix the problem for the icon, but there is still no hit detection on the flipped label in https://openlayers.org/en/latest/examples/icon-scale.html  when rotation is removed.
@mike-000 I think this requires a different fix, i.e. in `render/canvas.js`.`drawImageOrLabel`. There should be no extra case needed for rendering flipped images, at least no `translate` transform. This would require a different `originX` and `originY` calculation.