Would you be able to provide a minimal example? This would help finding the change that caused this by doing a `git bisect`.
Yes,[ here is barebones example](https://codesandbox.io/s/granule-layer-tile-loading-3vkktq?file=/main.js) of what we're doing.  For some reason the imagery isn't showing in this example (I must have something misconfigured) but, you can see the requests go out sequentially in the network tab which is the primary concern.

Edit: The change appears to have been introduced between 6.4.3 and 6.5.0
I've traced it down to what's listed as version `6.4.4-dev.1603221180680` in codesandbox.  I'm just not sure if/how this version translates to a commit to see what the change was.
Thanks for the investigation, @jasontk19. Then this was probably #11646. Not sure yet though if the old or the new behavior is the intended one.
Ok, the new behavior is the intended one. In versions prior to #11646, the tiles were not handled by the tile queue.

To get faster tile loading, you can use the map's `maxTilesLoading` property. The default value is 16, which means no more than 16 tiles are loading at any time. Try setting that to a (much) higher value.


Changing the `maxTilesLoading` to 64 seemed to have no impact on how many tiles were loaded at once.  Because of the way these layers are configured, a single layer may only cover a very small portion of the map and therefore there may only be one tile per TileLayer to be requested when you are zoomed all the way out.  Is there something about the fact that it's many different layers with so few tiles each that causes this loading behavior?  I guess I need to understand how the tile queue works better to know how we could get around this.
The tile queue manages all layers of the map, so it should not make a difference when you have many layers with few tiles.

Any chance you could fix the codesandbox you linked above? It would help if it actually showed a map. Also, I'm unclear why you're giving each layer a different className (which is bad for performance). Also, setting the `preload` option to `0` means that no lower resolution tiles will be preloaded. Not sure if this is what you want.
Sure thing, the codesandbox is working as expected now 👍🏻   Giving each a different className was just a shot in the dark on my part trying to see if it made a difference, we don't normally do that and I've since removed it.  The `preload: 0` was an intentional choice in the context of our larger app to cut down on total tile requests; we do our own preloading of tiles for prev/next days.