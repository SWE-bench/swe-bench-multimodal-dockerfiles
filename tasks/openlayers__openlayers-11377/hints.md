As far as I can tell, #11277 broke hit detection for regular shapes on Retina devices, i.e. the hit detection shapes are too big when the pixel ratio is > 1.

@sbrunner, can you take a look at this? The issue can easily be seen on http://localhost:8080/icon.html with a Retina device.
I just submitted #11336 to fix this.
There is still the same issue even in 6.4.2.

Here is the same example with 6.4.2.
https://codesandbox.io/s/green-brook-05wg9?file=/main.js
Thanks for sharing your findings @MichalK6677. I have reopened the issue and will do a `git bisect` to see what caused this performance drop.

As far as I can tell, only Chrome is affected by the performance drop. Am I right?
This problem was introduced by #11148, and I do see how it can be fixed. Hold on, I should be able to provide a fix in a few days, maybe later today already.