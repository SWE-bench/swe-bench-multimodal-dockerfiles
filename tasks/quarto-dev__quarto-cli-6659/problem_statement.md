Figures from R code blocks don't render if `fig-cap: !expr …` evaluates to `character(0)`
With Quarto 1.4.330, quarto-r 1.2, and knitr 1.43 on R 4.2.1, the command `quarto render example.qmd --to html` renders the following Quarto document as expected:

    ```{r}
    #| fig-cap: !expr caption
    caption = "hello world"
    knitr::include_graphics("http://arfer.net/mlp/img/rara-jiggs.png")
    ```

But if `caption = "hello world"` is changed to `caption = character(0)`, the figure disappears from the output.

I originally hit this issue with a mistaken `sprintf` call, which can produce a zero-length character vector.
