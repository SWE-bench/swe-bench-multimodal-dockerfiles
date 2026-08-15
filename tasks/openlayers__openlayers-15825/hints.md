Your source tiles overflow the tile grid extent and the validity extent of the EPSG:4326 projection which is causing a problem as it is defined as a global projection.

In your application a workaround would be to define the built-in  projection as non-global

    const epsg4326 = getProjectiont('EPSG:4326');
    epsg4326.setGlobal(false);

or hardcode the source projection as a non-global copy of the projection

    projection: new Projection({
      code: epsg4326.getCode(),
      units: epsg4326.getUnits(),
      extent: epsg4326.getExtent(),
      axisOrientation: epsg4326.getAxisOrientation(),
      global: false,
      metersPerUnit: epsg4326.getMetersPerUnit(),
      worldExtent: epsg4326.getWorldExtent(),
      getPointResolution: (resolution, point) => getPointResolution(epsg4326, resolution, point),
    })


Using your source tile grid in a reprojected `ol/source/TileDebug` does not have the same problem, but with DataTiles as in https://openlayers.org/en/latest/examples/data-tiles.html it does, so a fix in DataTile reprojection should be possible.
@mike-000, thanks!
I've tried to use the proposed workaround, and indeed the map looks much better now.
However, there are still some minor artifacts. Is there a way to get rid of them quickly? 
![image](https://github.com/openlayers/openlayers/assets/50118328/9ccce0de-d49b-43d9-b441-f49b6b3fb484)

That can also be seen with a canvas layer using your tile grid, and a semi transparent fill - there are transparent artefacts at the reprojection triangulation edges either side of the antemeridian which are not present in the underlying OSM source.  I think it is due to the final source pixel column not being precisely aligned to the antemeridian.

![image](https://github.com/openlayers/openlayers/assets/49240900/8e6e5d5b-b44c-4427-b615-de33a96f19d6)

#15815 is a potential fix for this which avoids having to change the projection.

Artefacts are reduced from

![image](https://github.com/openlayers/openlayers/assets/49240900/31a6cb74-71a6-4539-a4b8-61b96f795494)

to

![image](https://github.com/openlayers/openlayers/assets/49240900/68407bea-180b-4acd-ab56-b03e7cfd1a7b)

but not eliminated.  Artefacts can also be seen when using

```
  new GeoTIFF({
    sources: [
      {
        url: 'https://s2downloads.eox.at/demo/EOxCloudless/2020/rgbnir/s2cloudless2020-16bits_sinlge-file_z0-4.tif',
        bands: [1, 2, 3],
        min: 0,
        max: 3000,
      },
    ],
  }),
```

with the same projection.  In that case the tiles exactly fit the projection extent so misaligned pixel columns is not the cause.
