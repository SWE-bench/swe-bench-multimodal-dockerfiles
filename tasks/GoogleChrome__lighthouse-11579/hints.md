After reading the LH documentation, I found it's recommended to use the Chrome DevTools and it works well.
So can you replicate this in the extension still?  I ran it on the extension, and it seems to work fine.

![google_run](https://user-images.githubusercontent.com/6392995/46371168-81092e00-c63c-11e8-92b0-d6396534ea9e.png)

Chrome v69.0.3497.100/LH 3.2.1

Reinstalled the extension and it does not work for me still.
Could it depends on OS? I'm using the Ubuntu 18.04.1
Video of the process: https://youtu.be/pCoOqlKcrxw
> Reinstalled the extension and it does not work for me still.
> Could it depends on OS? I'm using the Ubuntu 18.04.1
> Video of the process: https://youtu.be/pCoOqlKcrxw

It doesn't work for me neither on Manjaro Linux.
Thanks very much for the video @serge22! This is very strange, it might be linux specific. It's especially odd given that the page load looks completely normal, there's just something wrong with the trace Lighthouse is getting from Chrome.
I spun up a Ubuntu 18.04.1 LTS VM and was unable to repro this with Chrome/71.0.3559.0 

Could you try updating Chrome @serge22 and let us know if that solves the issue?
I'll give it a go in the morning as well on my Ubuntu machine and Chrome stable 
ubuntu 18.04.1 on chrome 69.0.3497.100

![image](https://user-images.githubusercontent.com/1120926/46684273-a248bc00-cbf2-11e8-9c5e-dfd47c551708.png)

do you have it only on that machine? You could try chromium or canary and see if that works. How did you install chrome-stable on ubuntu?

Same here using Chromium: Version 69.0.3497.100 (Official Build) Arch Linux (64-bit)

But it does function correctly from the devtools
Chrome Version 69.0.3497.100 (Official Build) (64-bit)
Manjaro (so, arch) doesn't work as extension or dev tools. NO_FCP error
Doesn't work from either Dev Tools or the extension. Using Mint 18.3 and Chrome Version 69.0.3497.100 (Official Build) (64-bit).

![dev_tools](https://user-images.githubusercontent.com/5447028/47185300-03f7dd00-d2fb-11e8-9f3d-20b29df5fde3.png)

Seeing the same issue, computer details:

Chrome Version 71.0.3578.80 (Official Build) (64-bit)
Mac OS Mojave Version 10.14 (18A391)
MacBook Pro (Retina, 13-inch, Mid 2014)
Hi,

It happens all the time when you have the next situation:
* during the initial rendering page contains no text, e.g. only a spinner
* after some time 5-10s your app "starts" and renders the main content (UI, texts, etc.)

I've created a minimal reproducible demo for that https://github.com/webschik/lighthouse-no-fcp
P.S. In the production I've fixed that by adding of the small static text to the page.
I was trying to audit an old [website](http://www.sgs-schoenbuch.de/) that was receiving these errors as well. 
Curious what are some possible likely causes of this?

edit: 
- Mac OS Mojave Version 10.14.2
- Chrome 71.0.3578.98 
- MacBook Pro 
We've got a fix in v4 that should hopefully mitigate many of these cases. If you're experiencing this, give it whirl with the latest extension and let us know how it goes.
Same issue here, it doesn't work either from DevTools or Chrome extension, computer details:

- Mac OS Mojave v10.14.2
- Chrome 73.0.3683.75
- MacBook Pro

=============

**Error Report from Chrome extension:**

Lighthouse Version: 4.2.0
Lighthouse Commit: 35b285b87d681905777ed2545e48292312910485
Chrome Version: 73.0.3683.75
Initial URL: https://airhorner.com/
Error Message: NO_FCP
Stack Trace:
```
LHError: NO_FCP
    at chrome-extension://blipmdconlkpinefehnmjammfjpmpbjk/scripts/lighthouse-ext-bundle.js:21525:8
```
Same issue on Windows, it doesn't work either from DevTools or Chrome extension, computer details:
- Windows 10 (1809)
- Chrome 74.0.3729.131 x64

**Error Report from Chrome extension:**
```
Channel: DevTools
Initial URL: http://krooktjader.rproducts.eu/kontakt
Chrome Version: 74.0.3729.131
Stack Trace: LHError: NO_FCP
    at eval (chrome-devtools://devtools/remote/serve_file/@518a41c1fa7ce1c8bb5e22346e82e42b4d76a96f/audits2_worker/audits2_worker_module.js:1199:206)
```
Same issue on Mac

Enviroment:

- MacOS 10.12.6 (16G29)
- Chrome 74.0.3729.131 (Official Build) (64-bit)

Error:

```
Channel: DevTools
Initial URL: https://uworker.unicloud.com/web-oa/page/index.html#/dashboard
Chrome Version: 74.0.3729.131
Stack Trace: LHError: NO_FCP
    at eval (chrome-devtools://devtools/remote/serve_file/@518a41c1fa7ce1c8bb5e22346e82e42b4d76a96f/audits2_worker/audits2_worker_module.js:1199:206)
```
Same issue on Mac and Windows. Canary and Stable.  I'm actually not able to copy the error because the dialog overlays the information and is gone when I click cancel, but it is the same as the above
Same Issue, my setup:

MacBook Pro 2015
MacOS Mojave 10.14.4 (18E226)
Chrome Version 74.0.3729.157 (Official Build) (64-bit)

Am trying to audit a static site built with Gatsby.


Error message:

`NO_FCP
```
Channel: DevTools
Initial URL: https://digitalerbauer.de/
Chrome Version: 74.0.3729.157
Stack Trace: LHError: NO_FCP
    at eval (chrome-devtools://devtools/remote/serve_file/@7b16107ab85c5364cdcd0b2dea2539a1f2dc327a/audits2_worker/audits2_worker_module.js:1199:206)
````
Same issue on MacOS using Dev Tools. My setup is: 

- MacBook Air (13-inch, 2015)
- MacOS Mojave v10.14.4
- Chrome Version 74.0.3729.169 (Official Build) (64-bit)

**Error Report**
NO_FCP
```
Channel: DevTools
Initial URL: https://www.etsy.com/
Chrome Version: 74.0.3729.169
Stack Trace: LHError: NO_FCP
    at eval (chrome-devtools://devtools/remote/serve_file/@78e4f8db3ce38f6c26cf56eed7ae9b331fc67ada/audits2_worker/audits2_worker_module.js:1199:206)
```
I got this just now. 
Macbook Pro 15 inch 2018
MacOS Mojave 10.14.5
Chrome 74.0.3729.169
Ran LH from Chrome Dev Tools.

**Error message:** 
NO_FCP
```
Channel: DevTools
Initial URL: http://dinesen.com/
Chrome Version: 74.0.3729.169
Stack Trace: LHError: NO_FCP
    at eval (chrome-devtools://devtools/remote/serve_file/@78e4f8db3ce38f6c26cf56eed7ae9b331fc67ada/audits2_worker/audits2_worker_module.js:1199:206)
```
Getting the same Error

Macbook Air: 10.13.6
Chrome: Version 74.0.3729.169 (Official Build) (64-bit)

**Error Message:**
NO_FCP
```
Channel: DevTools
Initial URL: https://www.paisabazaar.com/cards-ssr
Chrome Version: 74.0.3729.169
Stack Trace: LHError: NO_FCP
    at eval (chrome-devtools://devtools/remote/serve_file/@78e4f8db3ce38f6c26cf56eed7ae9b331fc67ada/audits2_worker/audits2_worker_module.js:1199:206)
```
**NO_FCP** error too on my old Debian Jessie (8.11) thru dev tools, but it works on the command line.
Getting the same error when debugging in Localhost on IIS Express [Visual Studio]:


```
NO_FCP

Channel: DevTools
Initial URL: https://localhost.randomwebsite.com:44300/en-us/shop/samsung-65-inch-flat-4k-ultra-hd-hdr-smart-tv-un65nu6900fxza/apd/aa283176/tv-home-theater
Chrome Version: 74.0.3729.169
Stack Trace: LHError: NO_FCP
    at eval (chrome-devtools://devtools/remote/serve_file/@78e4f8db3ce38f6c26cf56eed7ae9b331fc67ada/audits2_worker/audits2_worker_module.js:1199:206)
```

**Computer Details:**
Dell Precision 15: Windows 10 Enterprise (10.0.17134 Build 17134)
Chrome: 74.0.3729.169
I have this issue *only* when the actual page isn't visible on my screen. If I move devtools to the side and have the window active, the FCP events etc. fire fine.
I already mentionned it wasn't working for my old Debian in <https://github.com/GoogleChrome/lighthouse/issues/6154#issuecomment-504127802> but as @danhilltech stated, it works if the browser is shown.
@danhilltech that's expected and unavoidable - Chrome will prioritize rendering completely if the window is not visible.
@connorjclark It was working before even if the browser window was hidden.
@millette it's possible there was a Chrome renderer optimization implemented then, though at least on the Mac it's been this way for quite a while.

There's not much we can do here: if the browser decides to lazily render only when the tab becomes visible again, Lighthouse can't reliably measure when it *would have* rendered if the tab had been visible.

Maybe we could improve the error message suggesting to check that the tab was in the foreground?
> Maybe we could improve the error message suggesting to check that the tab was in the foreground?

@brendankenny That would be appreciated :-)
Not working for me.
![Screenshot from 2019-07-11 10-06-07](https://user-images.githubusercontent.com/4492981/61038383-dd1b9280-a3c4-11e9-8c88-77465c361c78.png)

Had the same issue. @danhilltech's technique worked. Put the focus on the _actual page_ and it works.
just check no throttling and it should work even if it is a little bit slow
![image](https://user-images.githubusercontent.com/12363020/62238285-9240d980-b3ca-11e9-91bf-f54eca7f9e55.png)

lighthouse in vscode terminal is not working either! on windows 10 

vscode 2019
Thanks a lot @saifalfalah! The solution you explained worked for me too.
Reproduced on Chrome OS 76.0.3809.102, @danhilltech's solution worked without a problem.
@danhilltech and @saifalfalah solutions might only work when using GUI version. What if I am using chrome headless with puppeteer?
https://github.com/GoogleChrome/chrome-launcher/pull/170 should have solved this for the CLI. #9650 will add a warning if the tested tab was backgrounded and Lighthouse should be run again.