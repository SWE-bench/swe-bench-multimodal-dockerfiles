I think we'll want to address context sharing (or otherwise solve #12800) whether or not we add a new source or layer type to represent GeoTIFF (or other source) pyramids.

One issue with GeoTIFF pyramids is that there is no guarantee that the underlying tile grids will be uniform for a given resolution or zoom level.  The renderers currently assume that there is a single tile grid.  If you constructed a GeoTIFF pyramid where two GeoTIFFs at the same resolution had internal overviews or tile layouts that differed from one another, this would break the assumption by our renderers.  I think that currently a GeoTIFF (or other source) pyramid is best represented by a layer group in OpenLayers (as @ahocevar did in the COG pyramid example).

It feels to me like we should first address context sharing - making it possible to render many WebGL tile layers without exhausting the context limit.  Then I think we could add a new layer group type that makes it easy to work with GeoTIFF pyramids.  A layer group constructor for working with tiled STAC assets could make sense (and it would be nice to work on updating the [STAC Tiled Asset Extension](https://github.com/stac-extensions/tiled-assets) to reduce duplication and conflicts with the evolving [OGC 2D TMS spec](https://github.com/opengeospatial/2D-Tile-Matrix-Set), or perhaps just use the [OGC API - Tiles spec](https://github.com/opengeospatial/ogcapi-tiles) instead of needing another, but that is a different issue).
> One issue with GeoTIFF pyramids is that there is no guarantee that the underlying tile grids will be uniform for a given resolution or zoom level. The renderers currently assume that there is a single tile grid. If you constructed a GeoTIFF pyramid where two GeoTIFFs at the same resolution had internal overviews or tile layouts that differed from one another, this would break the assumption by our renderers. I think that currently a GeoTIFF (or other source) pyramid is best represented by a layer group in OpenLayers (as @ahocevar did in the COG pyramid example).

That is true, but I'd compare this again with the WMTS use case, where the tile-grid defined in the capabilities is authoritative and the images in pyramid are expected to follow. So I guess in this case we should just assume the GeoTIFFs follow this external TileGrid. Maybe I should have made this more clear.

Regarding the context sharing: This definitely seems like a good idea and important to fix. I'm curious of how the API will look in the end. This solution definitely seems like the more general approach, and I hope it does not come with too many drawbacks.

> A layer group constructor for working with tiled STAC assets could make sense

Yes, or at least with the information obtained by such a STAC Item.

Alright, shall I leave this issue open, or do we want to close it in favor of #12800 ?
@constantinius - I think it makes sense to have this open.

A pyramid of GeoTIFFs is a bit different than WMTS.  In the case of WMTS (or other well constrained tile specs), the tile grid (or tile matrix set) is defined in terms of tiles that are loaded by the client.  If I understand what you're interested in with a GeoTIFF pyramid, there are two levels of tile grid (or two levels of tile matrix sets).  The first tile grid determines which GeoTIFFs should be used for what resolution and coordinate range.  And then after reading the GeoTIFF metadata, there is a second tile grid (or tile matrix set) that defines the actual "tiles" that should be loaded.  Terminology is limiting me here, but I hope we're understanding this the same way.

My understanding is that your GeoTIFF pyramids are only defined by a tile grid that points to which GeoTIFF to load.  Then there are no guarantees at all about what the internal tiling scheme may be for any one of those individual GeoTIFFs.

I'm not saying that I don't see the value in an easy way to render a GeoTIFF (or other source type) pyramid.  Just saying that I think it might map better to a layer group rather than a single source given the current assumption made by our renderers.
@constantinius - I'd be curious to hear how things work with bigger pyramids now that #12965 is in.  You can try it out with the latest `ol@dev` release.  If things look ok performance-wise, the next step will be to add convenience around configuring the layer(s).
@tschaub Thanks for the update. I'll try it with our bigger pyramids!
@tschaub from our frontend guy I hear that the issue with the dropped context is now gone. Thanks a lot for the solution.

I will now close this issue, as an alternative is found.