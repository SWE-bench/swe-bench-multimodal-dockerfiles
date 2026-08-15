I think, Iframe blocks the `onload` event of parent from firing. 
Will it not affect the parent in any way if the iframe resource takes too long to fetch?
> I think, Iframe blocks the onload event of parent from firing.

this is true.

> Will it not affect the parent in any way if the iframe resource takes too long to fetch?

Well it'll delay the onload event so any script bound to that event will be delayed. But usually that is all low priority stuff, so it's not important for us.
 
Aside from the onload event, iframes don't have any layout-blocking characteristics. They can conceivably add network contention and main thread contention, though.

