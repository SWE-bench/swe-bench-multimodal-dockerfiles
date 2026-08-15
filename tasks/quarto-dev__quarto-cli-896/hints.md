This is by design (but perhaps still not acting optimally). The image is getting handled by our auto-stretch logic (which ensures that slides with a single image provide maximum space for that image). If you add the `.nostretch` class to the slide this won't happen:

```markdown
## Test A: custom block {.nostretch}
```

You can disable auto-stretching entirely with `auto-stretch: false` (see https://quarto.org/docs/presentations/revealjs/advanced.html#stretch)

That said, it seems like wrapping images in a div should be turning off this behavior. @cderv , perhaps the logic we have to detect images wrapped in `.cell-output-display` is catching these? Perhaps we should narrow this logic a bit to look explicitly for that class?

Ahh yep, adding `{.nostretch}` to the slide fixes it! Thanks!
> That said, it seems like wrapping images in a div should be turning off this behavior. @cderv , perhaps the logic we have to detect images wrapped in .cell-output-display is catching these? Perhaps we should narrow this logic a bit to look explicitly for that class?

For the stretching to work, the `<img>` needs to be at first level below `<section>`. So to make it work we are moving the `<img>` node at first level, but not only for `.cell-output-display` divs, but any parents. I believe we do that because sometime the single image is below another set by Pandoc, Knitr or Quarto. Only exceptions for now are for some know divs 
https://github.com/quarto-dev/quarto-cli/blob/af5c051e8251d3a0535f2e8dcf62d011259c8fb2/src/format/reveal/format-reveal.ts#L630-L641

So yes maybe it is too generic and we should do the other by being more selective of known situations ? 
Especially because it will be hard for us to detect a custom div set by a user from any other with the current structure. 
I guess that is what you mean by narrowing the logic, right ? 

This would mean that auto stretch would apply on: 

1. Simple mage set in slides inside no div 
````markdown
## Test D: No div

Oh hello

![](https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg)

Why not?
````
These are included by Pandoc inside `<p>` node 

2. Image with caption inside no div 
````markdown
## Test D: No div

Oh hello

![Caption](https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg)

Why not?
````
Those will be processed by Pandoc & Quarto and will be included in a div of class `quarto-figure` that we should handle

3. Image created using computation code

````markdown
## Test E: Knitr

Oh hello

```{r, echo = FALSE}
knitr::include_graphics("https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg")
```

Why not?
````

Those would be rendered as case 1 or 2 above, but all inserted into a div of class `cell` and a div of class `cell-output-display`. 
However, if those would be inserted into another div, it would be probably a custom one and we should ignore them. 

I'll change to this more narrow logic which seems to cover main cases. This means that any other cases would not allow applying `stretch` - unless we make the revealjs feature a bit more generic maybe.


<details>
<summary>Full example for testing</summary>

````markdown
---
title: "My talk"
author: "jimjamslam"
format: revealjs
---

## Test A: custom block

:::{.qrcodeblock}

Oh hello

![](https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg)

Why not?

:::

## Test B: columns

:::: {.columns}

::: {.column width="50%"}

Some left column comment

:::

::: {.column width="50%"}

Oh hello

![](https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg)

Why not?

:::
::::

## Test C: outer div

:::: {.anotherblocks}

:::{.qrcodeblockagain}

Oh hello

![](https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg)

Why not?

:::

::::

## Test D: No div

Oh hello

![](https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg)

Why not?

## Test D-2: No div - caption

Oh hello

![caption](https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg)

Why not?

## Test E: Knitr

Oh hello

```{r, echo = FALSE}
knitr::include_graphics("https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg")
```

Why not?
````


</details>


Yeah I think to be on the safer side we should have more narrow logic. I guess the user could also apply the `.r-strech` class explicitly as a signal to us that they want it unwrapped?
> I guess the user could also apply the .r-strech class explicitly as a signal to us that they want it unwrapped?

Ok I'll add that. For now in current dev branch, I implement the logic described above. Trying to add tests right now to document and check all this;