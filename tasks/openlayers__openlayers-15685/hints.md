Hard to say what's wrong without runnable code, but what happens if you remove the `backgroundFill` and `backgroundStroke`?
> Hard to say what's wrong without runnable code, but what happens if you remove the `backgroundFill` and `backgroundStroke`?

I tried to remove both backgroundFill and backgroundStroke but still issue with `fill`

If I remove last line in Style `fill: new ol.style.Fill({ color: 'rgba(255, 255, 255, 0.5)' })`, then it is not colouring element and all is ok with text label everywhere, but if you want to colour those VectorTiles with `fill: new ol.style.Fill({ color: 'rgba(252, 220, 215, 0.5)' })`, it will draw that Ghost layer above some text labels.

If I leave "fill" option in Style I have to remove from ol.layer.VectorTile renderMode: 'vector' and to default it to 'hybrid' which render everything correctly.
It would be good to have a minimal example (jsfiddle, codepen, codesandbox or similar) that shows the problem. Maybe you can click "Edit" on https://openlayers.org/en/latest/examples/vector-tile-selection.html and modify it to expose the issue?
Check image and try this code. Zoom 3-4 times and move to Spain for example. Line 45 paint countries to red color, but also render on some text labels some ghost boxes. If you remove that line (fill: new Fill({color: 'rgba(252, 220, 215, 0.5)'}),) boxes disappears but countries are not filled with color. :(

https://codesandbox.io/p/sandbox/vector-tile-selection-forked-2l6llr

<img width="518" alt="Screenshot 2024-03-28 at 7 11 41 PM" src="https://github.com/openlayers/openlayers/assets/27783775/c8c19e54-9204-4622-8e0c-5be08ecf3a75">

If you move map you will notice some labels have those ghost boxes and that is random, not everywhere.

<img width="226" alt="Screenshot 2024-03-28 at 7 20 31 PM" src="https://github.com/openlayers/openlayers/assets/27783775/5a8dd084-4f82-4ec9-a63e-bbc992fa3f4e">

This is not just cosmetic issue, but in more complex situation where you have mouse hover it start flickering, like changing randomly labels and VectorTiles background transparency.
Thanks for the reproduction case. `git bisect` shows that eeb4c3e2f0db9cbf417e850873198695815da9a8 is the first bad commit.
@mihailokg An easy workaround for now is to split the style into two styles, and give the text style a z-index higher than that of the fill and stroke:
```js
const selectedCountry = [
  new Style({
    stroke: new Stroke({
      color: '#000',
      width: 2,
    }),
    fill: new Fill({
      color: 'rgba(252, 220, 215, 0.5)',
    }),
  }),
  new Style({
    zIndex: 1,
    text: new Text({
      text: 'text',
      overflow: true,
      font: `12px sans-serif`,
      padding: [5, 10, 5, 10],
      textAlign: 'center',
      justify: 'center',
      textBaseline: 'middle',
      fill: new Fill({
        color: '#fff',
      }),
      backgroundFill: new Fill({
        color: '#454545',
      }),
      backgroundStroke: new Stroke({
        color: '#fff',
        width: 1,
      }),
    }),
  }),
];
Thanks for the info. Will try and see if this will resolve also flickering when mouse move. Will let you know asap.