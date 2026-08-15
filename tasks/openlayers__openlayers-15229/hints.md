> I tried to implement it as a test code, but I realized it cannot be expressed as a test code because the current test framework uses a square viewport. It only happens when with non-square viewport.

Rendering tests run in a 256 x 256 page viewport.  It should be possible to reduce the map viewport size within that, e.g. `map.setSize([256, 128]);`


The bug can also be seen when using

```
{
  "icon-src": "data/icon.png",
  "icon-width": 18,
  "icon-height": 28,
  "icon-color": "lightyellow",
  "icon-rotate-with-view": true,
  "icon-displacement": [
    0,
    9
  ]
}
```

in https://openlayers.org/en/latest/examples/webgl-points-layer.html
and fixed in https://deploy-preview-15229--ol-site.netlify.app/en/latest/examples/webgl-points-layer.html
