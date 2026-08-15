Hey scott! thanks so much for filing this.

Yes this is definitely a bug. We actually have addressed this behavior in other audits. For example: https://github.com/GoogleChrome/lighthouse/blob/bc9efba9b7b5c40a2886d6f1d366e272f420afb2/lighthouse-core/gather/gatherers/dobetterweb/tags-blocking-first-paint.js#L15-L17

But in the case of Critical Request Chains we didn't filter out `rel=preload` resources. We'll fix this. :)


And thanks so much for making this minimal repro. Super useful.