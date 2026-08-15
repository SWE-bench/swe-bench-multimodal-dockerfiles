You're using an entire spritesheet but it's only used a few times on the page which is why it's showing up here. In order to trigger our spritesheet logic, we have to see it being used at least 3 different times.

If you're loading an entire spritesheet for just a single image, consider splitting out that single image, so your users don't download all of them unnecessarily. That being said, it's just a suggestion and opportunities don't affect the score, so you can feel free to ignore this advice if you feel strongly about the sprite sheet decision.
Hi patrick, I counted and the spritesheet is being used for 18 times for my main page. 

A quick example is, you can see that it is used around 10 times when you open the menu named "Alışveriş". Below is the picture. Am I missing something here ?

![image](https://user-images.githubusercontent.com/25062864/57564749-e2a32f00-73b9-11e9-9b11-3fbeda24747e.png)



That's on interaction (after hovering/clicking the dropdown), correct? If the images won't be in the DOM when we just load the page without hovering, then Lighthouse will never know they're being used multiple times to know it's a spritesheet.
No it is not on interaction, the dom is already loaded when entered to my main page. 

My site is a live one, you can enter and check yourself. -> tisort.ist

Even if it would be on interaction, there are still 7 images I can count to you which uses spritesheet2

top logo
search magnifier
cover page text logo
footer credit cards image
social media icons at footer x 3 

Thanks for the additional info! Something weird is definitely going on in this gatherer for that page, and we'll have take a look. Apologies for the rote initial replies :)
Gatherer looks right, it does indeed limit the artifact to 2 images per url. It's just that there's no marker for "we think this is a sprite sheet" and thus no way in the audits to ignore them.

1) improve the heuristic

Currently we just say 3 usages = a sprite sheet.

We can also check that the unique usages are non-overlapping.

2) add `sprite: boolean` to each result in the artifact.

3) ignore the sprites in audits (haven't thought about how, if at all, they could be process differently)
Hm @Hoten I say something is going wrong because we're supposed to exclude the image entirely if it looks like it was a sprite sheet. We even have a [smoketest for it](https://github.com/GoogleChrome/lighthouse/blob/ffb1debfb6ed909c2d44b9c3cd578a5b6d17da8d/lighthouse-cli/test/fixtures/byte-efficiency/tester.html#L141).

Looking at the logic again though, it's very confusing and seems like there's a bug where it only accidentally works if there is a certain multiple of usages 😆PR pending :)