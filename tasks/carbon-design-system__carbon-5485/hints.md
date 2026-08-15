Researching this a little... we could technically use a `size` attribute on the inner `select` element in the `Pagination` component. 🤔 So theoretically... with the `onfocus` event, you could add a size attribute to restrict the size of the inner `select` element to be however many lines you define, and then the total list of options can be scrolled to. Docs are here: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select (go down to `Attributes` > `size`)

It would definitely have to be something that is only used `onfocus` (and then removed with `onblur`). And it should only be applied if the end-user wants it (like via a prop, maybe they can choose to set the size themselves...)

I'll give this a try in a bit & see about a PR 👍 
Please bear in mind #4070 - with a large number of pages, it results in many `<option>` elements on the page - which crashes the browser > ~100000.

Also, it looks like `size` only works when the select type is `multiple` (and also still hits the above issue, as it's just controlling the size of the scrolling container)
Hello @nictownsend --

> it looks like `size` only works when the select type is `multiple`

I'm not sure what you mean here? Can you link to a spec / example?

I whipped up a quick codepen that demonstrates using `size={number}`, without `multiple`, and it works while limiting the VISIBLE size of available options.

https://codepen.io/jendowns/pen/bGGoxZL

From what I see, it looks like `size` does not require `multiple`,  but ~`multiple` requires `size`~ (EDIT: actually seems you can use `multiple` *without* `size` for a multi select, but the first part seems to remain true)

------

> and also still hits the above issue, as it's just controlling the size of the scrolling container

The example above, in this issue, has 69 pages and shows the `select` element overshooting the `Pagination` container. So setting `size` prevents the `select`'s `option`s from overshooting by limiting the visible options at a given time (in this context of *this* issue, where there are 69 pages... or even just, hypothetically, a reasonable number of `option`s -- or pages -- that doesn't crash a browser).

Maybe `size` doesn't solve your issue in #4070, or rather -- maybe it doesn't resolve the general problem of having many thousands of options. 

But that would require a much more extensive refactor of this component... and I wonder if it isn't something that should be presented in something *other* than a `DataTable`-like component with `Pagination`? 🙂

I'm just wondering what user would ever say "oh yes, I'd like to jump exactly to page 953261" or even just page through to that page? Seems like some dedicated research would be helpful in this scenario? 
>I'm not sure what you mean here? Can you link to a spec / example?

Apologies - you're right, for some reason the codepen I was using must not have been updating properly as when I was setting size it was still using the dropdown list.

And yes, I do agree that this is not a catch all solution for the large list - that case definitely requires a researched refactor. I just wanted to draw attention in case it influenced a decision on this particular use case (or if documentation could be updated with guidance on the prop that it doesn't solve the large options problem).
Agreed, it definitely needs some attention... 

For the Security team, we just prioritized a research spike to look into this (I mean, beyond a `size` attribute bandaid). So hopefully we can come up with an idea for a refactor that we can share upstream with Carbon.
@jendowns have y'all figured out any type of solution to this? It seems to still present when there are a large number of pages... 
As #5129 tells, having many `<option>` for each page causes the problem not only of the vertical size but also of the performance. My $0.02 is providing an option not to render the `<select>`, we we haven't implemented such option.
@tw15egan Sorry for the delay getting back to you -- we are slowly working this out in `@carbon/ibm-security` 😅 

The plan is to refactor the `Pagination` component to be more like "building blocks", similar to the `UIShell` for example, so that way folks have several options to deal with this issue:

* Option 1 - do not include a child component we are calling the `PageSelector` (i.e., the select element that gets REALLY big when you have a bunch of numbers) at all.
* Option 2 - pass a `size` attribute to the `PageSelector` to reduce the height of the selector (allow you to scroll within it). This was a proposal originally in https://github.com/carbon-design-system/carbon/pull/4378 but the reviewers weren't fond of it (understandably so, due to the way it looked) -- BUT on our end we are at least going to give people this option.
* Option 3 - allow a number input instead of a select (this is not implemented yet & needs to be added)
* Option 4?? - due to the building blocks style approach here, theoretically a consumer could make their OWN "Page Selector" or whatever the case may be, and then handle these large page numbers in their own way.

Anyway, now the plan is to polish this refactored pagination component -- currently called `UNSTABLE__Pagination` in our library & then propose it back up to Carbon. It would be a breaking change, for sure.

EDIT: our `UNSTABLE__Pagination` (work in progress) is here: https://ibm-security.carbondesignsystem.com/?path=/story/components-unstable-pagination--default
Again I'm still working on the optional number input. But right now you can leave out the select element, if you want, which would help people dealing with a LOT of pages that creates a performance hit.
@jendowns no worries, that sounds like a great plan. Looking forward to seeing the polished up version! 🎉 
@jendowns Number input sounds a viable option, if our designers agree. CC @carbon-design-system/design 
@asudoh We mentioned a number input solution way back in https://github.com/carbon-design-system/carbon/pull/4378#issuecomment-546019688 and thought a number input would be a good solution for a large number of pages.

Carbon designers haven't created design specs, @jendowns have you guys already done that for your option 3? 
> We mentioned a number input solution way back in #4378 (comment) and thought a number input would be a good solution for a large number of pages.

@designertyler My apologies for missing this. Looking forward to seeing a spec!
This cause the browser to hang as per https://github.com/carbon-design-system/carbon-components-vue/issues/831 for large total items

Chrome, Opera and Mozilla limited selects to 10000 options according to https://chromium.googlesource.com/chromium/blink.git/+/master/Source/core/html/HTMLSelectElement.cpp#77

The current workaround in @carbon/vue is not to specify the number of items.

A number input or similar would be the usual solution.
@designertyler Sorry for the delay getting back to you --

So unfortunately I have received no guidance on a "number input" inside my pagination refactor. The biggest thing I don't know, as I mentioned to you a while ago in that closed PR, is the "error" or invalid state -- would there be an error message, and where would it go?

For now I am just proceeding with what I can do. Linked issue is here: https://github.com/carbon-design-system/ibm-security/issues/295

And just to reiterate, I did refactor the `Pagination` component in our downstream library `@carbon/ibm-security` -- it's a modular/building blocks style, like the `UIShell`, and it doesn't require an inner "page selector" (which is the source of all these problems -- page crash, VERY tall options list, etc). The component is here:  https://ibm-security.carbondesignsystem.com/?path=/story/components-unstable-pagination--default And the non-page-selector demo is here: https://ibm-security.carbondesignsystem.com/?path=/story/components-unstable-pagination--with-no-page-selector-or-sizer

I was planning to try to contribute this pagination refactor back to Carbon core once I finished with the number input option -- but would it be better if I just open a draft PR *now* so we can get more eyes on it? I am very, very open to any and all opinions on implementation etc. I haven't received much in the way of design direction either (namely, with the number input), so would appreciate any help there as well. (@joshblack @tw15egan do either of you have an opinion?)
Definitely think Number Input (mobile variant may work best) is the way to go, but also curious how we would handle the error state. Design will need to work that out before we're able to implement anything, so a draft PR may help to get some eyes on the problem if you have the time 🙏 