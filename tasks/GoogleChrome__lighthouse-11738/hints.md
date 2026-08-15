Also, which might be more interesting: Because Google only waits 5125ms (or it was something like that in the past) it can not index the page at all, because data isn't loaded at all..

Would be nice if the Lighthouse report would actually report SEO indexable data that the Google Bot can see (not how it interprets it), because it is shrouded in mystery and people wrongly believe that because 'google can index js' it will wait indefinitely for a page to load.
Thanks for filing @paales!

A few notes:

For Lighthouse waiting long enough, this is a known trade-off between receiving results quickly and waiting for the page to be done. The default Lighthouse mode of operation errs on the side of speed and only waits for ~1s of quiet (2 or fewer requests inflight). This page has a blocking graphql request that seems to always take longer than that and is relatively quiet otherwise, so you're bumping into it.

![image](https://user-images.githubusercontent.com/2301202/82336470-3fafc880-99b0-11ea-8c1a-832839d1dc2b.png)

I have a few ideas on how to improve this heuristic for `--throttling-method=simulate` but they'd all be breaking-ish changes that will have to wait for v7 and in principle we still can't guarantee the page is always "finished", for whatever that means to the site owner. 

As a workaround, you can control the quiet threshold by using a [custom config](https://github.com/GoogleChrome/lighthouse/blob/master/docs/configuration.md) with the `networkQuietThresholdMs` set to something higher. It's worth noting that the quiet thresholds for `--throttling-method=devtools` are hard-coded into the metrics themselves, so waiting longer won't tend to affect anything.

> Would be nice if the Lighthouse report would actually report SEO indexable data that the Google Bot can see (not how it interprets it), because it is shrouded in mystery and people wrongly believe that because 'google can index js' it will wait indefinitely for a page to load.

For a fix to the mystery, use the [official Google Webmaster tooling](https://support.google.com/webmasters/answer/9012289?hl=en) that does this :)

As for us doing it, it's a nice idea, but I doubt we'll ever be able to do it. The primary Lighthouse lens is performance metrics which have their own set of loading criteria and AFAIK Google Bot loads sites in a very different manner from everyday Chrome users such that we would never be able to match it or come close to guaranteeing they're seeing it the same way. That's why they built their own tool for it.

Thanks for the detailed response and your time. It seems we'll have to wait for 7.0 to more accurately represent this. (that'll probably take a few years? 😛)
> that'll probably take a few years?

Hey now no need to get hostile @paales 😉 we've been around for ~4 years and published 6 major versions. I would suspect somewhere around November-January is the target for v7.

> It seems we'll have to wait for 7.0 to more accurately represent this.

Or you could use a single  `--throttling-method` flag or a two line config file 😛 
Hahaha, whoops, sorry! I think I got the releases confused with the `5` release of PageSpeed Insights which happened a few years ago...

I'll have to take a look at using the right configs to actually check it :)
I'm not sure why pending-close was added here, but this is something we'd like to pursue.