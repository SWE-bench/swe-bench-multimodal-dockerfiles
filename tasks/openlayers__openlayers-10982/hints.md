This issue has been automatically marked as stale because it has not had recent activity. It will be closed if no further activity occurs. Thank you for your contributions.

I also have the same problem !! I’m going to turn off image rendering tomorrow and see if it’s working.
When using _Image_ / _hybrid_ or _vector_ i still git the clipped vector

![image](https://user-images.githubusercontent.com/228655/77391853-0be26900-6d9a-11ea-8cfc-4721ddcc9cd9.png)

I fixed this by adding a bigger buffer to the tile vector
I am having this problem as well.
The screenshot that @jeroenvheel looks like the vector tile source might have polygons with the wrong winding order. That could be fixed by configuring the `MVT` format with `ol/Feature` as `featureClass`:
```js
import VectorTileSource from 'ol/source/VectorTile';
import MVT from 'ol/format/MVT';
import Feature from 'ol/Feature';

new VectorTileSource({
  format: new MVT({
    featureClass: Feature
  }),
})
Here are some examples:

**OL-latest** 
![ol-point](https://user-images.githubusercontent.com/3605988/80545398-39b26300-8981-11ea-9deb-0c1c9b232aff.gif)


**OL5.3.0** ✅ 
![ol5-point](https://user-images.githubusercontent.com/3605988/80545764-1cca5f80-8982-11ea-8b59-3e711a1cd386.gif)



**Code example**
https://codepen.io/benjaki/pen/zYvzGxd
@Benjaki2 ~~Your issue is caused by an invalid tilegrid. Probably due to #10974.~~ Thanks for the test case, that should help to isolate the issue.