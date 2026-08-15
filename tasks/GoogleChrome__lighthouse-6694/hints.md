Good find thanks @ebidel :)
I've found a few things i'm not sure if we should fix it.

1) you're not preconnecting `fonts.googleapis.com` but you are preconnecting `https://fonts.gstatic.com` https://fonts.gstatic.com is used for the woff file and fonts.googleapis.com for the css file.
2) https://www.google-analytics.com should indeed be preconnected but somehow on a cold chrome it isn't. When running it through cli I get these origins as flagged but from devtools or extension I do not.

When going into chrome://net-internals/ and clear all caches I have the same issue as cli with devtools & extension. So the only fix is to check the DOM and HTTP-headers to see if they are marked as preconnected. This would make the audit easier to read too. WDYT to write a gatherer for this?
I'm able to reproduce this bug from the command line if i use `--chrome-flags="--headless"`. When I run lighthouse in normal mode, it seems to preconnect normally.
@patrickhulce what do you think of making a gatherer of preconnect tags? 
@wardpeet in general I'm not a fan of going the static analysis route for these especially since it's hard to determine what's worth the effort to be "extra safe" and what's not. Also because it's difficult to know that you've done preconnect right! i.e. if you correct `crossorigin` value such that the connection can be reused. It'd be difficult for us to know that it required `crossorigin="use-credentials"` for example.

I think we should try to investigate why it's not being preconnected to google-analytics and solve that bug before resorting to manual static overrides.
I think I'm seeing the same. The report has `Lighthouse 4.0.0-alpha.1` at the top.

I'm using the Lighthouse Chrome ext:

![ps3](https://user-images.githubusercontent.com/16349203/48564215-df892380-e8ed-11e8-936c-1da430e728a4.jpg)

I have some `preconnect` `link`'s in the HTML:

![ps2](https://user-images.githubusercontent.com/16349203/48564283-fdef1f00-e8ed-11e8-9206-fa3d897df321.jpg)

But Lighthouse is suggesting I add them:

![ps1](https://user-images.githubusercontent.com/16349203/48564314-0fd0c200-e8ee-11e8-976b-4b29866d99c1.jpg)

@wardpeet are you working on this or can I steal it from you? :)
FWIW, my investigation on #6676 has sufficiently convinced me your static analysis route is worth it, so if you already had something along those lines be my guest!
@patrickhulce feel free to take over. I haven't done anything yet 