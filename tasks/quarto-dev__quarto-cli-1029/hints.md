Unfortunately reveal is doing the measuring to determine available height and it doesn't know about the quarto aside feature. I don't think we can fix this without re-writing the stretch feature entirely (not impossible but not a small amount of work). 

@cderv Should we disable auto-stretch when we see footnotes or asides on a page?
Yes I agree. I think we should deactivate auto stretch in this case. 

If we want to support it in more quarto specific feature we'll need to rewrite it and adapt to our need.
Thank you both! The most frequent use regarding this combination (single figure + aside)for me is when I need to show the credit of a figure. Currently, I am using css to define a custom div, which is then included after the figure. 
@jjallaire I have looked closer into this today to understand why this would not work. The measuring should be aware of the aside presence in the slide. I think it gets the measuring right, but Quarto aside is position as absolute, 20px from the bottom. 
https://github.com/quarto-dev/quarto-cli/blob/9bb09f5369e9945b11e3c4b55d0c39039ae344a5/src/resources/formats/revealjs/quarto.scss#L279-L285

I believe this is why its gets above the image as the measuring does not take into account this absolute position. Is that what you meant by "reveal is doing the measuring to determine available height and it doesn't know about the quarto aside feature" ?  Maybe we could 'patch' the height computation to remove this fixed 20px we are adding ? 

Let's note that adding an aside will automatically reduce the available size for an image and so it will also be above image if one manually set the height 
````markdown
---
title: "`aside` class"
format: revealjs
---

## Slide 1 {.nostretch}

![elephant](https://github.com/quarto-dev/quarto-web/raw/main/docs/authoring/elephant.png){height="600px"}

::: {.aside}
Something here. A figure without caption
:::

````

![image](https://user-images.githubusercontent.com/6791940/171199021-184b5e7c-9445-476f-bb33-cebc5406190f.png)

There is even a size which is not so big that will make the aside part be above the caption 
![image](https://user-images.githubusercontent.com/6791940/171199316-98e11e00-e31e-4d3e-9728-eb4f5df0c5f7.png)

At the end, this will be always the case when an aside is on slide. Content needs to be sized manually in this case to fit the remaining space without the aside. 

So I am doing a PR to remove the auto-stretch when aside is present, but this will mean that all images on those slide requires to be manually sized according to the space left considering aside part at 20px from bottom.
