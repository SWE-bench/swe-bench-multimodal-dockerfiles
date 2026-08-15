I agree a empty extent should be empty in any projection.  However, it is likely any application would need to test `isEmpty` at some point in code such as yours.  Even if `applyTransform` made a special case (similar to `getArea`) for an empty extent you would still get a `Cannot fit empty extent provided as 'geometry'` assertion at the next line.  
Also if an extent does not contain `Infinity` but is considered empty because it has negative width or height, a transform will not be empty as it will use the bounding extent of the corners regardless of their original order.

That also happens if an identity transform is used on an empty extent:

```
let extent = createEmpty();
extent = transformExtent(extent, 'EPSG:4326', 'EPSG:4326');
console.log(isEmpty(extent), extent);  // false, [-Infinity, -Infinity, Infinity, Infinity]
```