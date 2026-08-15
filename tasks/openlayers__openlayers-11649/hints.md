OpenLayers only takes what it gets from proj4. In your above example, there is no axis order specified. If the above projection definition had an axis order and units specified, it would look like this:

    +proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +axis=neu +no_defs

For the above definition, OpenLayers will correctly store the axis orientation as property in the projection definition derived from proj4, but internally it always uses x, y order.

For reprojecting coordinates, the units are not used. The proj string above does not specify any units, and the projection definition generated from the string does not have units. So OpenLayers does not get any units from proj4.

However, since units are not used for reprojecting coordinates, this should not be a common problem.

In which case do you see an incorrectly rendered map? It would be good if you could provide a working example that shows the issue.
Well the problem is, that commonly used sources like epsg.io and spatialreference.org do not serve that information (no axis and no unit, e.g. http://epsg.io/4258 or http://epsg.io/4326).

I prepared a fiddle:
https://jsfiddle.net/45ukp0wj/

That fiddle should but will not display a map. Look at the console to see the ol.Projection output, its missing units and defaulting to wrong axis.

Then uncomment line 9-15 and replace the projectionstring in line 29 with the variable `projection`.
The map will appear.