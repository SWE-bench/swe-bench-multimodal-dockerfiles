That's indeed a good point and the operator would be quite simple, see https://maplibre.org/maplibre-style-spec/expressions/#id

Marking this as PR accepted if anyone wants to give it a try
@jahow Did someone start to work on this? I wish I could make PR on this 😄
I'm not familiar with style expression, tho..  So I'm not sure how the test code looks like, I mean I don't get the exact expectation of the work.

Do you think you could help me to start with a piece of test code or expected result of PR?

---

Firstly, let me write a piece of code below, as far as I understand:

When I get a GeoJSON file such like this
```json
{
"type": "FeatureCollection",
"features": [
  {
    "type": "Feature",
    "properties": {
      "id": "feature-ID",
...
```

People load upper geojson, and use it as follow, (brought code from [this](https://openlayers.org/en/latest/examples/style-expressions.html))
```js
const layer = new Layer({
      source: new Source({
        url: 'link-to-upper-geojson',
        format: new GeoJSON(),
      }),
      style: {
        'id': ['get', 'id'],
...

console.log(layer.getId())           // expected: `feature-ID` from the geojson file

```


am I on the right way?
"id" is not in properties, otherwise `['get', 'id']` would work.
```json
{
"type": "FeatureCollection",
"features": [
  {
    "type": "Feature",
    "id": "feature-ID",
    "properties": {
```
`['id']` is an expression without parameters. This should display the id as the text label:
```js
  style: {
    'text-value': ['id'],
  }
```
The [geojson id](https://stevage.github.io/geojson-spec/#section-3.2) can be int or string or it may not be set at all.
The [id expression](https://maplibre.org/maplibre-style-spec/expressions/#id) should return this value.
Not sure what the return value should be when not set.

Have a look in #15250 for some more pointers on where to implement this.
Correct me if I am wrong, but I believe the return value should always be a string or undefined. Even if the value gets set as some kind of number the ```text-value``` always expects a string back as that is what's going to be attempted to be set. According to the docs the ```text-value``` expects either a [StringExpression](https://openlayers.org/en/latest/apidoc/module-ol_style_flat.html#~StringExpression) or ```undefined```. I haven't tested to see if a null value would also be valid but likely might be fine and would not display anything.
Indeed, using a number as `text-value` may cause problems. In that case the [`to-string`](https://maplibre.org/maplibre-style-spec/expressions/#types-to-string) expression would also be needed.
```js
style: {
  'text-value': ['to-string', ['id']],
},
```
Or that the function that actually does the getting of the id will always do ```.toString()``` as this is what I had to do for all the data in the ```concat``` function.
I've looked around how the style expression works. (It's a bit of a challenge 😅)

And I figured out that feature's ID can be handled when `flatStylesToStyleFunction` returns styleFunction (src/ol/render/canvas/style.js:113)

But, I have no idea how to implement `compileExpression` because the parameters, such as `expression` and `context`, don't have any information of feature when it parses expression.

I think TBD operators (; `Ops.Zoom`, `Ops.Time`, `Ops.GeometryType` and so on) might have similar issue so that they're not implemented yet.

Is there something that I missed?
I guess you'll have to add the Feature to the EvaluationContext.
I got it. I think I'm about to finish. Thanks for many helps :)
Is this what you guys expect when `text-value` has `["id"]` expression?
The digits are from each feature's `ol-uid` because `feature.getId()` returns `undefined` even though I assigned `feature` to the `EvaluationContext` of style function.

https://github.com/openlayers/openlayers/assets/9066602/f6df5ce2-df54-4f12-8d4a-8a3cb376ef73

I'll make PR when it's correct.
I'd say it looks promising. If you take a look into the [used geojson](https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_populated_places_simple.geojson) for that example you'll notice that the Features do not have ids, so this is expected.