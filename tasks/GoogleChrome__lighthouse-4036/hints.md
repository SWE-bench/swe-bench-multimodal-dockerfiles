Oh wow that's rough! Thanks for reporting @Splaktar! That definitely seems like a Chrome bug, mail application is correctly opened for Chrome on macOS. It seems like Chrome generally doesn't like `target="_blank"` with mailto links though, it doesn't [seem to work at all on iOS](https://bugs.chromium.org/p/chromium/issues/detail?id=682783&q=mailto&colspec=ID%20Pri%20M%20Stars%20ReleaseBlock%20Component%20Status%20Owner%20Summary%20OS%20Modified)

From our side we should definitely ignore these too, but it seems like it's a good idea to remove target=_blank from mailto links in general 👍 
That's really helpful @patrickhulce! I had no idea that `target="_blank"` was not supported on iOS (and Android) for `mailto:` links. `target="_blank"` causes problems, but the combination of `target="_blank" rel="noopener"` is even worse on iOS and Android.

It does appear that `rel="noopener"` is working for me when `target="_blank"` is removed.

Perhaps there should be an audit to warn against using `target="_blank"` on `href="mailto:"` links instead since it works fine on Desktop but not on mobile.
@patrickhulce should we only do checks on http & https protocol?
@wardpeet yeah seems like a good idea instead of playing whack-a-mole with everything we're forgetting :)
Hey gang, big fan - awesome work!  I've gained a lot from looking through your codebase.

I had a quick look at this issue last night and I might be able to submit a PR for it, is it still available please?
@sanjsanj yes please go for it! The latest approach we think we'd like here is just limiting this audit to looking at urls starting with `http` :)
@patrickhulce Excellent, thank you!  I could happily do that but would that not miss relative URLs or ones without protocols?  Or am I missing something here in my understanding?
Ah yes, the gatherer should already fully resolve the URLs for you so you don't have to worry about handling relative links within the audit code
Gotcha, cheers!