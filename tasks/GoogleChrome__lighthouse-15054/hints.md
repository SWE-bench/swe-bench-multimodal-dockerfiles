> cycle through execution contexts for the queries for this kind of audit (probably good in general)

Target manager can listen to `Runtime.executionContextCreated` (and keep association with what session/target it came from), and `GlobalListeners` gatherer can loop through each when collected the listeners for the main target's `window`.

Eventually bfcache failures reasons will cite source locations, which would have really helped here. (@brendankenny could link to it)
> cycle through execution contexts for the queries for this kind of audit (probably good in general)

This seems like a good path forward. We will go through just the main frame contexts.