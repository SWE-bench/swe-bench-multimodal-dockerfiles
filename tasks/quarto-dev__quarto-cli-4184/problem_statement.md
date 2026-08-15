tabset and nav-fill not rendering correctly in prerelease
### Bug description

Not sure how this relates to #4068, but the combination of panel-tabset and [nav-fill](https://getbootstrap.com/docs/5.0/components/navs-tabs/#fill-and-justify) doesnt work anymore.

```
---
title: "Untitled"
format: html
---

:::{.panel-tabset .nav-fill}

## A

## B

:::
```

With quarto 1.2.335:
![Screenshot1](https://user-images.githubusercontent.com/17147355/215998958-4276977f-1c65-40f7-908f-f9c6e8146572.png)

and with quarto 1.3.146
![Screenshot2](https://user-images.githubusercontent.com/17147355/215999100-58883d5c-4081-494f-abef-6f5e89fbc95b.png)


Edit: This appears to work

```
:::{.nav-fill}
:::{.panel-tabset}

## A

## B

:::
:::
```


### Checklist

- [X] Please include a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [X] Please [format your issue](https://quarto.org/bug-reports.html#formatting-make-githubs-markdown-work-for-us) so it is easier for us to read the bug report.
- [x] Please document the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [x] Please document the operating system you're running. If on Linux, please provide the specific distribution.
