It looks like a bug.  If you change transparent to a semi-transparent shade and use the same simple `operation` as #14408 you can see it is drawing on top of the previous values instead of replacing them.  I suspect the same underlying cause as #14408.
It is the same underlying cause as #14408 and can also be seen if other WebGL layer types such as a Heatmap are used in a RasterSource.  Clearing the context before rendering fixes it

```
elevationTile.on('prerender', (e) => {
  e.context.clear(e.context.COLOR_BUFFER_BIT);
});
```

which also avoids the need to set an extent on the ImageLayer.

But to properly fix the bug this should happen automatically as it does when WebGL layers are rendered directly by the map.