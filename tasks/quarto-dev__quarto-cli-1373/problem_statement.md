`code-tools` doesn't work with URL for `source`
### Bug description

Here is a simple qmd file:

````
---
title: "Hello"
format:
  html: 
    code-tools:
      source: https://github.com/quarto-dev/quarto-web/blob/main/index.md
---

Some text.

```{r}
1 + 1
```
````

When rendered, the `code-tools` menu doesn't show up.

<img width="1552" alt="Screen Shot 2022-07-12 at 8 15 20 PM" src="https://user-images.githubusercontent.com/5965649/178663604-53528fea-7e3d-4d21-bedb-20cea6998618.png">

Things work fine if using `source: true`.

<img width="1552" alt="Screen Shot 2022-07-12 at 8 16 13 PM" src="https://user-images.githubusercontent.com/5965649/178663783-271ec5a1-8f2d-4fb8-8289-29c9942ecdea.png">

- RStudio version: RStudio 2022.07.0+548 "Spotted Wakerobin" Release (34ea3031089fa4e38738a9256d6fa6d70629c822, 2022-07-06) for macOS Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4_0) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.12.10 Chrome/69.0.3497.128 Safari/537.36
- OS: macOS 12.4


### `quarto check` Output

``` bash
[✓] Checking Quarto installation......OK
      Version: 1.0.16
      Path: /Applications/quarto/bin

[✓] Checking basic markdown render....OK

[✓] Checking Python 3 installation....OK
      Version: 3.10.1
      Path: /usr/local/bin/python3
      Jupyter: 4.9.1
      Kernels: python3

[✓] Checking Jupyter engine render....OK

[✓] Checking R installation...........OK
      Version: 4.2.0
      Path: /Library/Frameworks/R.framework/Resources
      LibPaths:
        - /Users/mine/Desktop/RStudio/quarto-tip-a-day/renv/library/R-4.2/x86_64-apple-darwin17.0
        - /Library/Frameworks/R.framework/Versions/4.2/Resources/library
      rmarkdown: 2.14

[✓] Checking Knitr engine render......OK
```

### `quarto tools check` Output

``` bash
Tool         Status                    Installed     Latest  
chromium     Not installed             ---           869685  
tinytex      External Installation     ---           v2022.07
```

### Checklist

- [X] [formatted your issue](https://yihui.org/issue/#please-format-your-issue-correctly) so it is easier for us to read?
- [X] included a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [X] documented the quarto version you're running, by pasting the output from running `quarto check` in the "Quarto Check Output" text area?
- [X] documented the version of the quarto tools you're running, by providing the output from running `quarto tools check` in the "Quarto Tools Check Output" text area?
- [X] documented the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [X] documented which operating system you're running? If on Linux, please provide the specific distribution as well.
- [X] upgraded to the latest version, including your versions of R, the RStudio IDE, and relevant R packages?
