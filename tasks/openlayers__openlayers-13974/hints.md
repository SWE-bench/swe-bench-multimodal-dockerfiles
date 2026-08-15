I also encounter this with a 5 band GeoTIFF (returning 6 bands including the alpha).  The workaround there is to explicitly specify the bands and duplicate one of them:

```
  sources: [
    {
      nodata: 0,
      bands; [1, 2, 3, 4, 5, 5],
      url: 'xxxx.tif',
    },
  ],
```