Markdown styling in table captions
### Bug description

Quarto does not seem to allow any styling of the text in table captions like _italics_ etc.
This problem does not occur with figure captions.

### Screenshot
![image](https://user-images.githubusercontent.com/6596512/191931023-8f3880ab-32a8-4d01-bb87-afe89f19bf82.png)

### .qmd file (can't attach):
````
---
title: "No markdown styling in table caption"
format:
  html:
    theme: default
    keep-md: true
---
```{r}
# captions for figure and table with md styling
caption_table <- "Can't use ^superscript^ or _italics_ in table caption"
caption_figure <- "Can use ^superscript^ or _italics_ in figure caption"
```


```{r}
#| tbl-cap:  !expr caption_table
# caption is set in qmd with: #| tbl-cap: !expr caption_table
library(kableExtra)
column_spec(kable(head(cars)),column = 1:2, width = "15em")
```


```{r}
#| fig-cap: !expr caption_figure
# caption is set in qmd with: #| tbl-cap: !expr caption_figure
plot(cars)
```

```{r}
sessionInfo()
```


````

Table captions are put inside some sort of div, which ignores markdown synthax (or latex syntax when rendering to pdf), for this reason I included the intermediate .md file.

###  .md file excerpt (also see attachment):
````
::: {.cell tbl-cap='Can\'t use ^superscript^ or _italics_ in table caption'}

```{.r .cell-code}
# caption is set in qmd with: #| tbl-cap: !expr caption_table
library(kableExtra)
column_spec(kable(cars),column = 1:2, width = "15em")
```

::: {.cell-output-display}
....
````
[reprex_table_formatting.md](https://github.com/quarto-dev/quarto-cli/files/9632422/reprex_table_formatting.md)


### Info
Rstudio IDE: 2021.09.0 Build 351

Session info:
```
R version 4.1.3 (2022-03-10)
Platform: x86_64-re
dhat-linux-gnu (64-bit)
Running under: Red Hat Enterprise Linux 8.5 (Ootpa)

Matrix products: default
BLAS/LAPACK: /usr/lib64/libopenblas-r0.3.15.so

locale:
 [1] LC_CTYPE=en_US.UTF-8       LC_NUMERIC=C              
 [3] LC_TIME=en_US.UTF-8        LC_COLLATE=en_US.UTF-8    
 [5] LC_MONETARY=en_US.UTF-8    LC_MESSAGES=en_US.UTF-8   
 [7] LC_PAPER=en_US.UTF-8       LC_NAME=C                 
 [9] LC_ADDRESS=C               LC_TELEPHONE=C            
[11] LC_MEASUREMENT=en_US.UTF-8 LC_IDENTIFICATION=C       

attached base packages:
[1] stats     graphics  grDevices utils     datasets  methods   base     

other attached packages:
[1] kableExtra_1.3.4

loaded via a namespace (and not attached):
 [1] rstudioapi_0.13   knitr_1.39        xml2_1.3.3        magrittr_2.0.3   
 [5] rvest_1.0.2       munsell_0.5.0     viridisLite_0.4.0 colorspace_2.0-3 
 [9] R6_2.5.1          rlang_1.0.5       fastmap_1.1.0     highr_0.9        
[13] stringr_1.4.0     httr_1.4.3        tools_4.1.3       webshot_0.5.3    
[17] xfun_0.31         cli_3.3.0         systemfonts_1.0.4 htmltools_0.5.2  
[21] yaml_2.3.5        digest_0.6.29     lifecycle_1.0.1   htmlwidgets_1.5.4
[25] glue_1.6.2        evaluate_0.15     rmarkdown_2.14    stringi_1.7.6    
[29] compiler_4.1.3    scales_1.2.0      jsonlite_1.8.0    svglite_2.1.0    ****
```


### Checklist

- [X] Please include a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [X] Please [format your issue](https://quarto.org/bug-reports.html#formatting-make-githubs-markdown-work-for-us) so it is easier for us to read the bug report.
- [X] Please document the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [X] Please document the operating system you're running. If on Linux, please provide the specific distribution.
