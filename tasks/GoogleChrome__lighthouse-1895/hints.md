What version of Chrome are you using?
I get it when using the CLI as well
I saw this error as well using Chrome Canary version 57.0.2959.0 canary (64-bit) on Mac OS X 10.11.6 testing the URL https://whoistheorchid.com/.

I _did not_ see this error using Chrome version 55.0.2883.95 (64-bit) on Mac OS X 10.11.6 testing the same URL.
@paulirish for when he's back from vacation :)

This is sort of a consequence of some of the changes introduced by #1152, which improved correctness of these audits but also turned what were incorrect but *seemingly* correct scores into explicit errors. It's a better situation than before even though we're getting more error results.

The cause is that some of the events we look for in a trace sometimes aren't there. I've noticed that this can especially be a problem for faster loading sites. You shouldn't be getting this on *all* pages, though, or even all runs of a particular page, so please do comment if that is what you're seeing.

More robust handling of problematic traces is something we're going to have to focus on in the new year, both on our side (doing what we can to (correctly) infer missing events, and [giving better advice](https://github.com/GoogleChrome/lighthouse/issues/812) if something needs to change to test correctly) and on Chrome's side (e.g. [this recently fixed bug](https://bugs.chromium.org/p/chromium/issues/detail?id=674228)).
@brendankenny I see this bug on all the runs on my page, I also tried with different sites like housing.com and I see the problem there too :(
@ebidel I use the Chrome Version 54.0.2840.71 (64-bit) on Mac OS X.
I'm seeing this on all my runs since the update as well. I am running Chrome 55.0.2883.87 on Win7 64-bit. I see "Cannot read property 'ts' of undefined" on first paint and time to interactive metrics. I get stats on perceptual speed and latency however.
I've only just started getting this error while testing my website www.lunait.solutions, it started appearing after I converted it to a static site to improve speed (that may or may not be a red herring, alternatively chrome may of updated without me realising).

Also tested on airhorner.com and I get the same error.

Running chrome Version 55.0.2883.95 (64-bit) on Mac OSX Yosemite Version 10.10.5
The error happens when firstMeaningfulPaint (fMP) is fired before firstContentfulPaint (fCP). fMP will be undefined. i'll cook up a fix 😄 

The audit does a correct check for not passing time to first fMP but maybe we should switch to the last fCP? As you can see on the screenshots below. fMP is pretty quick but than things change
![image](https://cloud.githubusercontent.com/assets/1120926/21492918/a4b08d42-cc08-11e6-8cc0-276830b8be9c.png)



see [audits/first-meaningful-paint.js](https://github.com/GoogleChrome/lighthouse/blob/0dff5efef196c5d9ecfab223cd1a54b1e2b169de/lighthouse-core/audits/first-meaningful-paint.js#L136-L137)
Any idea when this fixed will be released?
@JGSolutions For now you can use previous verison, use the cli one. `npm install -g lighthouse@1.2.2` this works perfectly fine.
ok thanks
Sorry holiday season :) I think new release will be next week
@wardpeet was there a PR that got cooked up or did I miss it? Otherwise, we can close if this is fixed and just waiting on a new release.
@ebidel added the pr, which doesn't really fix this issue but gives a better error message

for a real fix we should look at

> The audit does a correct check for not passing time to first fMP but maybe we should switch to the last fCP? As you can see on the screenshots below. fMP is pretty quick but than things change

//cc @paulirish wdyt?
> The cause is that some of the events we look for in a trace sometimes aren't there. I've noticed that this can especially be a problem for faster loading sites. You shouldn't be getting this on all pages, though, or even all runs of a particular page, so please do comment if that is what you're seeing.

Just to clarify, is it a good or bad thing that this error pops up? That is, is my site loading "too fast" and is passing the test, or is there a problem with my site I should investigate?

@doctyper could you tell us your url so I can have a looksy :)
@wardpeet Oh yeah :)

https://www.nfl.com/super-bowl
@doctyper mmh I tried running in extension, cli & also tried extension in chrome stable. I get an fMP just fine. Maybe because of my latency.

Could be indeed that site loads to fast. Can you use the cli by `npm install -g lighthouse` and run it with `lighthouse https://www.nfl.com/super-bowl --save-artifacts --save-assets` and give us the screenshot and trace file when you have the issue.
Strange. I just tried reinstalling the Chrome extension and got the same result:
![screenshot 2017-01-04 09 50 26](https://cloud.githubusercontent.com/assets/6960/21652847/499015fc-d263-11e6-9daa-023c50a84261.png)

The CLI gave me actual results for these values, but it seems to have thrown an error:

```
Page load performance is fast: t parse content: Parsing error: Please check validity of the block starting from line #1
 ── 100 First meaningful paint (264.1ms)
 ── 100 Perceptual Speed Index (569)
    - First Visual Change: 277msk { color: #000000 }a:visited { color: #000000 }a:hover { color: #000000 }a:active { color: #000000 }  -->
    - Last Visual Change: 8082ms
 ── 100 Estimated Input Latency (33.1ms)
 ── 92 Time To Interactive (alpha) (2284.3ms).3.1 +86ms
```

CLI output attached: 
[www.nfl.com_2017-01-04_09-44-25-0.zip](https://github.com/GoogleChrome/lighthouse/files/685458/www.nfl.com_2017-01-04_09-44-25-0.zip)

Thanks @doctyper! I confirmed that #1404 fixes things for your nfl trace. 

Thanks very much for posting that. :)
I am still seeing this issue in the chrome extension 1.4.1
@KaboomFox new issue to follow is #1567, sorry
Is this fixed? I am seeing it in `Version 56.0.2924.87 (64-bit)`
Apparently not fixed. 

@denar90 has also debugged this one and identified that the firstPaint trace event is missing in some contexts. :/

https://github.com/paulirish/pwmetrics/pull/50#issuecomment-280493387
@AvraamMavridis can you provide us with more details? 
Do you use extention or API? 
Which version do you use? 
What site do you measure?
@paulirish @wardpeet I think I finally can reproduce error but in scope of pwmetrics repo. Its kinda tricky to catch but it happens 100% sure. So I can create standalone example to have clean experiment.
Will it be helpful for you?
@denar90 extension, latest, simple PWA single page react app.
@AvraamMavridis  thx :)
@denar90 it would be yes
https://github.com/denar90/ligthouse-issue-1253

Try to go through instructions.

If you will not get the problem
 - try several times
 - increase [CPU_THROTTLE_METRICS](https://github.com/GoogleChrome/lighthouse/blob/a5416c46c957b9f57824117bc3928c5c80fdd75e/lighthouse-core/lib/emulation.js#L70) to 20 (worked for me) and try several times one more time

If so, don't hesitate for asking additional stuff, maybe record video or something.

P.S. This case is too tricky...
Fresh news. Just got issue using extension.

So the case is: go to page -> Press 'Generate report' -> Serf internet (go on github to review either some pr or respond on issue) -> go back to page you wanted to trace

![lighthouse report2017-02-28 12-55-35](https://cloud.githubusercontent.com/assets/6231516/23402715/756f1db2-fdb5-11e6-9a00-0c309d432e25.png)
