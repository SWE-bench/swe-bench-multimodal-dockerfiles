Links aren't resolved in `index.qmd` on Confluence
### Bug description

For example, with the [example site](https://github.com/rstudio/quarto-confluence-test/blob/main/sites/example), editing `reports-folder/index.qmd` to be:
````
---
title: "Reports"
---

* [January](2022-01.qmd)
* [March](2022-03.qmd)
````

Looks and works fine on local preview:
<img width="353" alt="Screen Shot 2023-03-06 at 12 13 38 PM" src="https://user-images.githubusercontent.com/25964/223220302-fe7fa661-a50c-4c13-bacc-51bf6cd2e581.png">

But, no links appear on Confluence:
<img width="539" alt="Screen Shot 2023-03-06 at 12 14 12 PM" src="https://user-images.githubusercontent.com/25964/223220420-4b090d3b-1867-43b7-ac5f-3fe0eb63f34b.png">


### Checklist

- [X] Please include a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [X] Please [format your issue](https://quarto.org/bug-reports.html#formatting-make-githubs-markdown-work-for-us) so it is easier for us to read the bug report.
- [ ] Please document the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [ ] Please document the operating system you're running. If on Linux, please provide the specific distribution.
