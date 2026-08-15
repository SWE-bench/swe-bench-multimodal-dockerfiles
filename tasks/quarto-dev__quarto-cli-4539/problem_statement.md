gt table spanners and quarto captions
````
---
format: html
---

```{r}
#| include: false
library(tidyverse)
library(gt)
```

```{r}
#| echo: false
#| tbl-cap: "Caption"
#| label: tbl-test
dat <- tribble(~a, ~x, ~y, ~z,
			   "A", 1, 12, 13,
			   "B", 2, 9, 11)

dat %>%
  gt() %>%
  tab_spanner(
	label = "Subheader",
	columns = c(x, y)
  )
```

@tbl-test
````

Produced output:

<img width="1153" alt="image" src="https://user-images.githubusercontent.com/285675/218155441-d762063a-3043-43f6-8543-8dd200e73854.png">

Desired output:

<img width="545" alt="image" src="https://user-images.githubusercontent.com/285675/218155490-0e0014c7-5dde-4ba8-8b6a-9a39f4405732.png">

This is either CSS or our table processing failing in the presence of spanners. Maybe a combination of both, since it only happens when we inject a caption.
