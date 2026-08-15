[revealjs]: `aside` class
When `aside` is used on a slide with a single figure, there seems a clash between `aside` and `r-stretch`: the figure is stretched too much and the `aside` content overlaps the bottom of the figure. If there is a caption for the figure, the caption even goes below the `aside` content.

Desired behavior is that `aside` contents have priority, and they always take the bottom part of the slide; if a single figure is included, it should be stretched to the top of the `aside` block. Is this something that can be implemented? @cderv 

Try the MRE below.
```markdown
---
title: "`aside` class"
format: revealjs
---

## Slide 1

![](./img/kitten.png)

::: {.aside}
Something here. A figure without caption
:::


## Slide 2

![Kitten](./img/kitten.png)

::: {.aside}
Something here. A figure with caption
:::


## Slide 3

There is no figure on this slide.

::: {.aside}
`aside` works well.
:::

## Slide 4 

::: {layout-ncol=2}
![Kitten](./img/kitten.png)

Mix text and figures.
:::

::: {.aside}
`aside` works well.
:::

```
![Screenshot from 2022-05-28 13-45-46](https://user-images.githubusercontent.com/60116296/170842313-a1c7d279-0d9a-487c-9b26-de99e50ce9b9.png)

![Screenshot from 2022-05-28 13-46-34](https://user-images.githubusercontent.com/60116296/170842336-e9d80b2a-a142-423b-bc4e-7052179e5a48.png)



