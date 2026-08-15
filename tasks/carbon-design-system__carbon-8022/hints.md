Note: We need the fix for this issue quickly, for IBM SPSS Statistics
Any updates on this one?
visible tooltip on hover and focus is an accessbility requirement, so I don't know if we can change that behavior (related https://github.com/carbon-design-system/carbon/issues/5069)

the pattern for showing/hiding tooltips when multiple tooltips are present is still a WIP (refs w3c/aria-practices#127 w3c/wcag#914 w3c/wcag#915)

currently there is a PR open for dismissing all tooltips via <kbd>Esc</kbd> which is a stopgap solution until the pattern is fleshed out (https://github.com/carbon-design-system/carbon/pull/5147)
Thank you for detailed update, @emyarod. Really appreciate it! 👏 
I'm going to mark this as blocked until the w3c delivers a solution to this pattern
A workaround @emyarod told me is changing the alignment to avoid overlapping.
@asudoh Since we have many buttons like this next to each other (toolbar) near top left or top right edge of window,  I don't have option to change alignment. When I change some to be left or right, tooltip will cover other buttons and interaction with them will be spoiled, top can't be used (top edge of screen), left together with right also, since tooltip will overflow window window edge, and wan't be visible.
the w3c issues referenced above have not been resolved yet, but #5147 added <kbd>Esc</kbd> key support for dismissing any open tooltips which may be a workaround. if that is not sufficient, then we will need some design guidance on what to do in this situation as there are multiple ways to trigger multiple tooltips on a page
I don't think `Esc` is a good way to dismiss `focus`ed tooltips. First, it's not easily discoverable; secondly, there seem to be a ton of issues around it (e.g. tooltip within a modal dialog? See linked w3c issues above).

I think this is due to "competing" implementations for keyboard- vs mouse-based navigation. For keyboard nav, we use `focus` to show the tooltip; for mouse nav, `hover`. However, when clicking on an icon-only button with the mouse, this also activates the `focus` handler.

One possible fix for this would be to ensure that only a single icon-only button (or any other widget?) can have an "active" visible tooltip. This could be accomplished by surrounding such buttons in a `ButtonGroup` parent component, whose only purpose would be to detect `mouseover` events and remove any existing focus.

This could even be extended to work on the entire page -- make it implicit in the tooltip impl, so that developers don't need to worry about adding a "button group".

I haven't tried to implement this and there may be some gotchas I haven't thought about. But it seems that having multiple tooltips visible at the same time isn't necessary for mouse-based navigation.
Please unblock this. Don't wait for w3c, because you will be waiting a very long time. :)

In the meantime, having 2 tooltips visible at the same time is a bug that should be fixed.

I think it can be fixed and still meet [WCAG 2.1 1.4.13 Content on hover or focus](https://w3c.github.io/wcag21/guidelines/#content-on-hover-or-focus) by doing the following:
- if the tooltip is initially triggered by _focus_, then it should be dismissed when _focus_ is removed (or if a different tooltip is triggered by hover)
- if the tooltip is initially triggered by _hover_, then it should be dismissed when **_hover_** is removed (even if the button still has focus)

See also: https://github.com/carbon-design-system/carbon/issues/7040