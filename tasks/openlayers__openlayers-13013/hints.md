Does [770, 767] work?   `770 * 767 + 258 = 577 * 1024` suggests the data has been truncated and the final row is not complete.
> Does [770, 767] work? `770 * 767 + 258 = 577 * 1024` suggests the data has been truncated and the final row is not complete.

The warning goes away, but the data still doesn't get rendered.

I attached a listener to `tileloadend` and that is the output:

![Screen Shot 2021-11-13 at 10 05 37 AM](https://user-images.githubusercontent.com/6855297/141648827-559f1bb0-a478-45d5-a6c4-90d02c03a43f.png)

The length of the data seems to be correct.

What's interesting, however, is that there are additional tiles requested at coordinates `[0, -1, 0]` and `[0, 1, 0]` and the data for those tiles is `undefined`:

![Screen Shot 2021-11-13 at 10 09 38 AM](https://user-images.githubusercontent.com/6855297/141648945-d1f3a061-291d-4961-9a0f-a50e5436d5b1.png)

The reason the data is `undefined` is because my loader returns `undefined` for tile coordinates that don't exist. However, if I instead return white tiles (i.e., create an empty array of the given size and fill all pixels with 255), the tiles are still rendered black.

![Screen Shot 2021-11-13 at 10 41 37 AM](https://user-images.githubusercontent.com/6855297/141649953-0da914bf-1701-4852-81da-004f32478c39.png)



There seems to be a problem with tile widths which are not multiples of 4 when there a 3 bytes per pixel, or not multiples of 2 when there are 1 or 2 bytes per pixel. 
The problem is explained in https://stackoverflow.com/questions/51582282/error-when-creating-textures-in-webgl-with-the-rgb-format

If you are using a dev version which includes #12933 you could use

```
layer.on('prerender', function (event) {
  const gl = event.context;
  gl.pixelStorei(gl.UNPACK_ALIGNMENT, 1);
});
```

But maybe that should be made the default setting?  The calculation of `bandCount` https://github.com/openlayers/openlayers/blob/391af5a466115cb974665d5ad7adbbce6924b62e/src/ol/webgl/TileTexture.js#L169 is assuming an `UNPACK_ALIGNMENT` setting of 1.
> But maybe that should be made the default setting? The calculation of `bandCount`

@mike-000 should the calculation consider `DataTileSource.bandCount`, which can be specified upon construction of the source via the [bandCount](https://github.com/openlayers/openlayers/blob/391af5a466115cb974665d5ad7adbbce6924b62e/src/ol/source/DataTile.js#L29) option.
That option appears to be used only for defining styles.  An `unpackAlignment` option (with default of 1?) would be useful to ensure the calculation of `bandCount` for `TileTexture` corresponds to the `gl.pixelStorei` setting.
I'll set up a dev version using the master HEAD and let you know whether `gl.pixelStorei(gl.UNPACK_ALIGNMENT, 1)` works.
@mike-000 It works!