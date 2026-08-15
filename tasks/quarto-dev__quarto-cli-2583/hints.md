No sure if it's a bug or a feature request. 
I would also be interested in any workarounds for this problem!
I don't think that's coming from quarto; I think that's coming from the way kable handles captions. Did this work for you in RMarkdown?
@cscheid This is my understand of this issue - not sure by what you are referring with `third-party`

when `fig-cap` is provided, it is used as Caption in Pandoc's Markdown syntax for image. Meaning we will have this in the md file 
````
::: {.cell-output-display}
![Can use ^superscript^ or _italics_ in figure caption](test2_files/figure-html/unnamed-chunk-3-1.png){width=672}
:::
````

The caption here will be process by Pandoc and converted appropriatly. 

For `tbl-cap` though, this is a Quarto feature, meaning the content will be handle by Quarto. We will have this in the intermediary markdown after knitting 
```````markdown
::: {.cell tbl-cap='Can\'t use ^superscript^ or _italics_ in table caption'}

```{.r .cell-code}
# caption is set in qmd with: #| tbl-cap: !expr caption_table
library(kableExtra)
column_spec(kable(head(cars)),column = 1:2, width = "15em")
```

::: {.cell-output-display}

`````{=html}
<!-- html table here -->
`````
:::
:::
```````

`tbl-cap` is handled by us through Lua filter I believe, and it seems possible that we don't convert that - could be an issue or something we missed (I think we should handle that as Markdown right ? )

hope it helps understand this 

>  it seems possible that we don't convert that 

`tbl-cap` will be correctly read as Markdown into the AST, but we loose the formatting when we `stringify`
 
https://github.com/quarto-dev/quarto-cli/blob/0917949e5b6f8005e02c89b1ef8a834f170f446a/src/resources/filters/quarto-pre/table-captions.lua#L169-L170

I'll send you a PR with a proposition to handle this correctly I think. 