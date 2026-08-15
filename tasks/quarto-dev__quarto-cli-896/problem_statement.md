Can't place image in div in revealjs format
I can place an image in `.columns`, but when I try to define a general div with some arbitrary class, text goes in it, but the image is bumped to after the div.

Here's an example:

```
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
```

In all three slides, I expect the example image to be inside the classed div, between "Oh hello" and "Why not". But when I render, this only works in the second slide (where it's in the right column). In the first and third slides, it slips after the text, outside the div.

<img width="1015" alt="image" src="https://user-images.githubusercontent.com/6520659/168455225-72cb6644-9d69-4e15-9da4-3a183e19c6ff.png">

<img width="1015" alt="image" src="https://user-images.githubusercontent.com/6520659/168455229-318f2868-3573-4f42-a30b-70a7a8bb4275.png">

<img width="1015" alt="image" src="https://user-images.githubusercontent.com/6520659/168455233-1579b08c-b80e-47f2-98e8-57936043d0aa.png">





