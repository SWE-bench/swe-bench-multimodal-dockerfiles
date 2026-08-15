bisected to #9023
https://googlechrome.github.io/lighthouse/viewer/?gist=631af25962bb4848fbc21115ad173bad ~~hmmm maybe the viewer code is too old? try this:~~ Forgot to deploy 5.1 to the viewer. Fixed :)

Run this:
```
document.querySelector('.lh-report').prepend(document.querySelector('.lh-scores-header .lh-gauge--pwa__wrapper'));
```

You'll see that the check mark appears only after the sticky header is present.
It is strange that turning off `display: none` for `.lh-sticky-header` prevents the issue. I'll file a browser bug.

https://bugs.chromium.org/p/chromium/issues/detail?id=971907
This feels oddly reminiscent of the scrolling PWA SVG Chrome bug...
Hard to believe we're finding so many bugs with SVGs (well, 2, but that seems a lot for browser bugs). Are we doing something that unique? Or do most people not know they can report issues like this to Chromium?
Turns out this is not a chrome bug (the same thing happens in Firefox, though not in Safari).

The PWA score gauge [is using references for its badges and gradients](https://github.com/GoogleChrome/lighthouse/blob/5aeef234faf8a342bf5d195529019d61f5b05cbb/lighthouse-core/report/html/templates.html#L684-L685) (so it can do things like `<path fill="url(#lh-gauge--pwa__check-circle__gradient) d="..."></path>` to share a circle gradient between versions of the gauge). These are [defined in a `<defs>` element](https://github.com/GoogleChrome/lighthouse/blob/5aeef234faf8a342bf5d195529019d61f5b05cbb/lighthouse-core/report/html/templates.html#L633-L655) inside the gauge's svg element.

The problem is that these use `id`s for the reference, and `id`s are supposed to be unique...but we include three copies of the gauge in the page (scores header, sticky header, and category). When trying to render the gradient (or badge), the renderer looks up the referenced element by picking the first one it finds in the DOM, which (after #9023) happens to be `display: none` in the sticky header, so nothing is rendered for the referenced element.

There are a few ways of fixing this, but basically it comes down to one of
- don't use references
- dedupe the `<defs>`
- have unique IDs for all instances of the gauge