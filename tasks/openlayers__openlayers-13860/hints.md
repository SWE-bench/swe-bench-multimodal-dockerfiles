The geojson contains three empty entries in the coordinates array which can be found by searching for `,[]`.  If those are removed it will work.
@mike-000 Thank you. It works right after remove these empty entries.

```js
contours.features = contours.features.map(function(contour) {
    contour.geometry.coordinates = contour.geometry.coordinates.filter(polygon => polygon.length > 0)
    return contour
 })
```
Reopening, because empty coordinate arrays are valid GeoJSON.