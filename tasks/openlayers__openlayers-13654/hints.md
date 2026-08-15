Reprojection currently only works for RGBA image tiles.  Where there are two conflicting interpolation requirements it is possible to reproject image tiles (e.g. without interpolation) and use the reprojected canvas tiles that process produces as the source for a non-interpolated WebGL data source https://codesandbox.io/s/disable-image-smoothing-forked-ru97e?file=/main.js  I presume the opposite might also be possible, convert the data tiles from a GeoTIFF source to RGBA images and use those in an image tile source which can be reprojected.  An new API method for tile sources such as getTileImage would be nicer than using the non-API methods in that example.
Yes it is possible.  Here is a very basic (no tile load error handling, etc.) reprojection to EPSG:3857  https://jsbin.com/loxohux/edit?html,js,output (GeoTIFF is not working in CodeSandbox)
Thanks a lot! I'm playing around with it right now, but for other (non-public) examples, I get weird behavior (holes, wrong colors) so need to investigate why that happens.
So with https://openeo.vito.be/openeo/1.0/jobs/fbe109fb-01ca-449c-9d48-279c93d27652/results/bW0%3D/1c2ad7dce3b43938c86ab9a9dff9639f/openEO.tif?expires=1642516600 and UTM zone 32, it shows only half of the tile and the tile content seems incorrectly scaled. The number of pixels I get for the tile is exactly half the number of tiles the canvas asks for. Is that a resolution issue? Needs further investigation...

Anyway, I think this should be part of OpenLayers at some point. People will also want to easily show COGs on Web Mercator basemaps, I assume.
I agree, and I have created a `ol/source/DataTileImage` which take a DataTile or GeoTIFF source and returns canvas tiles, but the example is not ready yet.  My first example assumed 4 band RGBA with default UnpackAlignment. To convert other band counts and alignments to RGBA canvas I am using:

```
function dataToCanvas(data, size) {
  if (data && !(data instanceof Float32Array)) {
    const width = size[0];
    const height = size[1];
    const bytesPerRow = data.byteLength / height;
    const bandCount = Math.floor(bytesPerRow / width);

    if (bandCount <= 4) {
      const canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      const context = canvas.getContext('2d');
      const imgData = context.getImageData(0, 0, width, height);
      const pixels = imgData.data;

      let pixelIndex = 0;
      let rowOffset = 0;
      const colCount = width * bandCount;
      for (let rowIndex = 0; rowIndex < height; ++rowIndex) {
        for (let colIndex = 0; colIndex < colCount; colIndex += bandCount) {
          const dataIndex = rowOffset + colIndex;
          pixels[pixelIndex++] = data[dataIndex];
          pixels[pixelIndex++] = data[dataIndex + (bandCount < 3 ? 0 : 1)];
          pixels[pixelIndex++] = data[dataIndex + (bandCount < 3 ? 0 : 2)];
          pixels[pixelIndex++] =
            bandCount % 2 == 1
            ? 255
            : data[dataIndex + (bandCount < 3 ? 1 : 3)];
        }
        rowOffset += bytesPerRow;
      }
      context.putImageData(imgData, 0, 0);
      return canvas;
    }
  }
}
```
Ah, I see. Thanks a lot!

I also created a class from your examples:

```js
import XYZ from 'ol/source/XYZ';
import { toSize } from 'ol/size';

export default class ProjGeoTiff extends XYZ {

	constructor(opts, geotiff) {
		super(Object.assign({
			tileGrid: geotiff.getTileGrid(),
			url: '{z},{x},{y}',
			interpolate: false,
			tileLoadFunction: (imageTile, coordString) => this.tileLoadFunction_(imageTile, coordString)
		}, opts));
		this.geotiff = geotiff;
	}

	tileLoadFunction_(imageTile, coordString) {
		const coord = coordString.split(',').map(Number);
		const tile = this.geotiff.getTile(coord[0], coord[1], coord[2], 1, this.getProjection());
		const tileState = tile.getState();
		if (tileState == 2) {
			this.setImage_(tile, imageTile, coord);
		} else {
			const listener = () => {
				const tileState = tile.getState();
				if (tileState != 1) {
					tile.removeEventListener('change', listener);
					this.setImage_(tile, imageTile, coord);
				}
			};
			tile.addEventListener('change', listener);
			tile.load();
		}
	}

	setImage_(tile, imageTile, coord) {
		const size = toSize(this.geotiff.getTileGrid().getTileSize(coord[0]));
		const data = tile.getData();
		const canvas = this.dataToCanvas(data, size);
		imageTile.getImage().src = canvas.toDataURL();
	}

	dataToCanvas(data, size) {
		if (data instanceof Float32Array) {
			throw new Error("Float32 currently not supported.");
		}
		const width = size[0];
		const height = size[1];
		const bytesPerRow = data.byteLength / height;
		const bandCount = Math.floor(bytesPerRow / width);

		if (bandCount <= 4) {
			const canvas = document.createElement('canvas');
			canvas.width = width;
			canvas.height = height;
			const context = canvas.getContext('2d');
			const imgData = context.getImageData(0, 0, width, height);
			const pixels = imgData.data;

			let pixelIndex = 0;
			let rowOffset = 0;
			const colCount = width * bandCount;
			for (let rowIndex = 0; rowIndex < height; ++rowIndex) {
				for (let colIndex = 0; colIndex < colCount; colIndex += bandCount) {
					const dataIndex = rowOffset + colIndex;
					pixels[pixelIndex++] = data[dataIndex];
					pixels[pixelIndex++] = data[dataIndex + (bandCount < 3 ? 0 : 1)];
					pixels[pixelIndex++] = data[dataIndex + (bandCount < 3 ? 0 : 2)];
					pixels[pixelIndex++] =
						bandCount % 2 == 1
							? 255
							: data[dataIndex + (bandCount < 3 ? 1 : 3)];
				}
				rowOffset += bytesPerRow;
			}
			context.putImageData(imgData, 0, 0);
			return canvas;
		}
	}

}
```

Which can be used as follows:

```js
let geotiff = new GeoTIFF({ sources: [{url: '...'}] });
let view = await geotiff.getView();
let source = new ProjGeoTiff({projection: view.projection}, geotiff);
```
Here is my `ol/source/DataTileImage` approach https://jsbin.com/hesodep/edit?html,js,output  The `imageSource` could be used directly, but I have also added a `getTileImage` method for all image tile sources so reprojected tiles can be used in other sources or with different interpolation settings, or in the case of your 2 band source, converting back from RGBA to 2 band.  For data tiles interpolation of RGBA bands during reprojection should be avoided, and reprojection quality could be improved by setting a suitable TileGridForProjection to avoid over or under zooming when creating the reprojected tiles.
Thanks, looks interesting, but overwhelming on first sight. What's your plan with that class? Is that meant to be part of OL at some point? And of course, I'm wondering why projection is not done directly via WebGL and instead the Canvas route has been chosen?
Reprojection has been done in canvas since OpenLayers 3, and there would little to be gained by redoing it in WebGL plus canvas reprojection of `GeoTIFF` could be used with `ol/layer/Tile` on systems without WebGL..  `DataTileImage` could be like a normal source and not need any extra application code to handle the asynchronous loading as long as any projections needed were predefined and you did not want to recenter the view.

```
const map = new Map({
  target: 'map',
  layers: [
    new WebGLTileLayer({
      source: new DataTileImage({
        source: new GeoTIFF({
          sources: [{ url: './data/example.tif' }]
        }),
        interpolate: false,
        wrapX: true,
      })
    })
  ],
  view: new View({
    center: [0, 0],
    zoom: 0,
  })
});
```
> there would little to be gained by redoing it in WebGL

I want to make sure nobody else mistakes this for consensus.

It is true that currently, image tile sources are reprojected in Canvas.  Reprojection of data tile sources (including GeoTIFF) is not yet supported.
> It is true that currently, image tile sources are reprojected in Canvas. Reprojection of data tile sources (including GeoTIFF) is not yet supported.

Yes, converting to canvas, reprojecting using the existing code then converting back to data tiles as in my examples is limited to <=4 band Uint8Array data sources.  The 5 band Float32Array example would need a different approach, which could also be used for any data or image source.


This issue has been automatically marked as stale because it has not had recent activity. It will be closed if no further activity occurs. Thank you for your contributions.

Still a valid feature request that COGs can be reprojected on the fly so that COGs with different CRS can be shown on the same map...
Reprojection can be achieved even with multiband Float32 data, but requires multiple intermediate TileImage sources each reprojecting 3 bytes per pixel.  A 5 band Float32 source uses 20 bytes per pixel, which needs 7 intermediate sources and is understandably rather slow!  Here is the Band Contrast Stretch example reprojected from EPSG:4326 to EPSG:3857 https://codesandbox.io/s/cog-stretch-reproj2-clopqg?file=/main.js

Performance is improved by handling the intermediate sources sequentially https://codesandbox.io/s/cog-stretch-reproj3-v920ub  It is also necessary to manage the requests for original projection GeoTIFF tiles as reprojection can use many more than when not reprojected, especially on a full page map.  Although the OpenLayers default in 16 tiles loading simultaneously when using the example source I encountered corrupted tiles unless that was reduced.