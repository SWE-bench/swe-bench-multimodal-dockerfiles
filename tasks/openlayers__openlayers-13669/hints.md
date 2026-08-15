Hey @m-mohr - it looks like there might be some things we could do better here.  Should we reopen this?  I'm curious if you found a way around.

In addition to the nan issue, the experience isn't that great with non-tiled GeoTIFFs.
We currently use `NaN` to indicate that there is not a nodata value.  I can look into handling this a different way.