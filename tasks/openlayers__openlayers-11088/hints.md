proj4js 2.6.1 is swapping axes which OpenLayers isn't expecting it to do.  But OpenLayers needs to know about the axis orientation to align the tile grid correctly, and a change to that part of OpenLayers would tie specific version of OpenLayers to specific versions of proj4js.  However removing the `+axis` from the the proj4 definition and setting `axisOrientation` in the Openlayers projection definition instead seems to be compatible with both versions of proj4js https://codesandbox.io/s/openlayers-ortofotomapa-4b2vm
I need to investigate this more. Maybe we're not reading all options from proj4 correctly, especially axisOrientation.

But if this is really a breaking change in proj4 (which I don't think - I am a maintainer there and tests did not break), I need to fix it in proj4 or publish a new major version.

If anyone can start a WIP pull request with failing tests that shows the issue, we can work on making them pass. It is also ok to require proj4 version >=2.6.1 (or >=3) in OpenLayers, if that allows for a clean fix.
After some investigation, I come to the conclusion that @mike-000's advice is correct. The projection definition of EPSG:2180 does not have `+axis=neu` in its definition. Now I need to investigate why setting the axisOrientation in the OpenLayers projection definition is required to make that WMTS work.
Here's another example from StackOverflow.  The sources are clearly using NE notation (otherwise the TopLeftCorner of the TileMatrix would be below the LowerCorner of the BoundingBox) despite https://epsg.io defaulting the `+axis` setting and without adding it the output would be misplaced as well as rotated https://codesandbox.io/s/wmts-openlayers-bgld-bwyb3
However http://epsg-registry.org **does** define northing (x) easting (y) in its definitions of the projections used there and EPSG::2180
http://www.epsg-registry.org/export.htm?wkt=urn:ogc:def:crs:EPSG::31259
http://www.epsg-registry.org/export.htm?wkt=urn:ogc:def:crs:EPSG::2180