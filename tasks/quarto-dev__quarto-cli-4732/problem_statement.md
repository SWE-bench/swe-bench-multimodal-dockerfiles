revealjs does not work with knitr embed engine
### Bug description

Using Quarto 1.2.335 (which is included in recent RStudio dailies, including 2023.03.0+385). This problem can be recreated without using the RStudio IDE when rendering using Quarto from the command-line.

Given a `code.R` file:

```r
cat("this is code.R\n")
```

The following revealjs document does not show the embedded code:

````markdown
---
title: embedding with reveal
format: revealjs
engine: knitr
---

## Embed!

```{embed, file = "code.R"}
```
````

<img width="850" alt="image" src="https://user-images.githubusercontent.com/362187/223846591-cbcdd571-c6c3-484e-b323-54ec5e7c6ee6.png">

The generated HTML contains a block, but no code:

```html
<section id="embed" class="slide level2">
<h2>Embed!</h2>
<div class="cell" data-file="code.R">

</div>
<div class="footer footer-default">

</div>
</section>
```

In contrast, when we do not output to HTML, the embedded code is shown.

````markdown
---
title: embedding without reveal
engine: knitr
---

## Embed!

```{embed, file = "code.R"}
```
````

<img width="544" alt="image" src="https://user-images.githubusercontent.com/362187/223846616-9f633a3c-7c00-4bb2-9562-47f3740c15b0.png">

Using the most recent version of knitr from CRAN and R 3.6.3 on macOS 12.6.3.

```bash
R -s -e "packageVersion('knitr')"
#> [1] ‘1.42’
```

Discovered while trying to apply the workaround from https://github.com/quarto-dev/quarto-cli/issues/1237

### Checklist

- [X] Please include a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [X] Please [format your issue](https://quarto.org/bug-reports.html#formatting-make-githubs-markdown-work-for-us) so it is easier for us to read the bug report.
- [X] Please document the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [X] Please document the operating system you're running. If on Linux, please provide the specific distribution.
