A single bokeh plot will be wrongly identified as several subfigures. 
### Bug description

Code:

````md
---
title: "test webpage"
format:
  html:
    code-fold: true
execute:
  cache: true
jupyter: python3
---


```{python}
#| label: fig-demo
#| fig-cap: "This is a demo figure for debug"

from bokeh.io import output_notebook
output_notebook(hide_banner=True)

from bokeh.palettes import Spectral5
from bokeh.plotting import figure, show
from bokeh.sampledata.autompg import autompg as df
from bokeh.transform import factor_cmap

df.cyl = df.cyl.astype(str)
group = df.groupby('cyl')
cyl_cmap = factor_cmap('cyl', palette=Spectral5, factors=sorted(df.cyl.unique()))
p = figure(height=350, x_range=group, title="MPG by # Cylinders", toolbar_location=None, tools="")
p.vbar(x='cyl', top='mpg_mean', width=1, source=group, line_color=cyl_cmap, fill_color=cyl_cmap)
show(p)
```
````

Output:

![image](https://user-images.githubusercontent.com/5415510/186504610-7b9a4437-45b5-461d-b2bc-570ee8a45dd0.png)


The subfigure 1b and 1c is empty and should be exist. 

### Checklist

- [x] upgraded to the [latest nightly quarto version](https://github.com/quarto-dev/quarto-cli/releases)?
- [x] [formatted your issue](https://yihui.org/issue/#please-format-your-issue-correctly) so it is easier for us to read?
- [x] included a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [x] documented the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [x] documented which operating system you're running? If on Linux, please provide the specific distribution as well.
