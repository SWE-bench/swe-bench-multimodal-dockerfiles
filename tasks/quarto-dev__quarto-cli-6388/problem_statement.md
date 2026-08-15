Interaction issue with `pander` package as Markdown is not correctly formated in output
Simple example 

````markdown
---
title: "repex"
format: html
keep-md: true
---

```{r}
pander::pander(list("1", "2", 3, c(1, 2)))
```
````

Which gives us this results 

![image](https://user-images.githubusercontent.com/6791940/214011147-dca0577c-ba59-410b-abe8-782413d963e4.png)


Somehow the markdown list is not correctly formatted as sub bullet are introduced. 
Our intermediary md is the one messed up somehow
````markdown
---
title: "reprex"
format: html
keep-md: true
---


::: {.cell}

```{.r .cell-code}
pander::pander(list("1", "2", 3, c(1, 2)))
```

::: {.cell-output-display}
* 1
  * 2
  * _3_
  * _1_ and _2_


:::
:::

````

The knitted result with `knitr::knit("test.qmd")` gives us correct formatting 
````markdown
---
title: "reprex"
format: html
keep-md: true
---


```r
pander::pander(list("1", "2", 3, c(1, 2)))
```



  * 1
  * 2
  * _3_
  * _1_ and _2_



````

So some processing somewhere is not correctly parsing. 
