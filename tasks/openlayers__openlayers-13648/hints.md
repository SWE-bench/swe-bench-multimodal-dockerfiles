Looks like the pixel scale meta data is not correctly applied.
https://exiftool.org/TagNames/EXIF.html <- 0x830e
![image](https://user-images.githubusercontent.com/56256405/163393400-803b13ed-f2e6-4afd-b174-74a0dabde740.png)

Add an osm layer to see that the image is incorrectly stretched:
```js
import OSM from "ol/source/OSM";

// ...

  layers: [
    new TileLayer({
      source: new OSM()
    }),
    new TileLayer({
      source: source
    })
  ],
```
@M393: Yes, indeed, if I do that in OpenLayers, the image is not located correctly. In QGIS and geotiff.io it is correctly located though:
![image](https://user-images.githubusercontent.com/8262166/163394901-4df498f5-ab32-4877-84ea-2b60b41dbf2c.png)

So is this an error in OL? Or is this a poorly generated COG and the other tools are more tolerant/robust?
I haven’t checked the metadata, but are these non-square pixels (x resolution different from y resolution)?

it is a current known limitation that OpenLayers requires square pixels for all raster types (not only GeoTIFF).  See also https://github.com/openlayers/openlayers/issues/13053#issuecomment-983125589
Looks like the pixels are indeed non-square. Should OpenLayers throw a warning or error in this case? It seems that if I read a COG and is displayed incorrectly due to a known limitation, I should get informed by the library so that I can make my users aware of it. OL (or geotiffjs?) is reading the metadata anyway in the Auto View request, so I assume the library can check the pixel size, too?
Closing as it is a known limitation.
@m-mohr - I agree we can improve the situation here.  If we can't resample or otherwise work with non-square pixels, we could make the error known.
@m-mohr - Do you still have that example data handy?  It looks like geotiff.io doesn't work with https://demo.nextgis.com/api/resource/5511/cog (the non-square data mentioned in #13053).  I'd be curious to see non-square pixels working on geotiff.io.
No, not at the moment. The server is currently offline, I hope they'll fix it over the weekend. @tschaub 
This is very untested, but it may be doable to support non-square pixels: #13593 

I've only tried using a GeoTIFF with nearly square pixels.  Need to find or generate some more extreme cases to work out what else will need to change.
@tschaub Here's a new signed link to the example file (expires in 7 days, so maybe download it in advance): https://openeo.vito.be/openeo/1.1/jobs/552e3e33-4fe0-42ca-b93c-7f1cd3a91224/results/assets/MjUyNTRjNGRiMTkzMGNhNzQwNjg0OTJmM2NhOWIyZjM0N2JhMWU3ZTI0ZTAzY2U0OTMzOTlmZWE1NmVhOTQzN0BlZ2kuZXU%3D/08f1bfaeeaa18448c3e02ca1d16cc5a8/openEO.tif?expires=1651313745

Rendered correctly on geotiff.io:
![grafik](https://user-images.githubusercontent.com/8262166/164890364-91718f94-43cb-4ad7-93cc-71ed218c28ba.png)
