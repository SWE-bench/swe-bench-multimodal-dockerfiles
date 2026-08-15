RevealJS link (anchor) on a standalone image is not rendered
### Bug description

(Apologies for the initially empty bug report -- I pressed "return" on the template after typing the title and it submitted the bug).

On a slide of a RevealJS presentation, an image that has a hyperlink will render without the hyperlink if it's by itself.

```markdown
---
format:
  revealjs:
    center: true
---
## Slide (link won't work)

[![](https://quarto.org/docs/blog/posts/2023-04-26-1.3-release/arthur-chauvineau-Dn7P1U26ZkE-unsplash.jpeg)](https://google.com) 

## Slide (link will work)

Blah [![](https://quarto.org/docs/blog/posts/2023-04-26-1.3-release/arthur-chauvineau-Dn7P1U26ZkE-unsplash.jpeg)](https://google.com) 

```

I suspect that this is caused by the logic of how standalone images are rendered (and the link is ignored/stripped).

Quarto 1.3.185 on Windows 10.

```terminal
$ quarto check

[>] Checking versions of quarto binary dependencies...
      Pandoc version 2.19.2: OK
      Dart Sass version 1.55.0: OK
[>] Checking versions of quarto dependencies......OK
[>] Checking Quarto installation......OK
      Version: 1.3.185
      Path: C:\Users\Cris\AppData\Local\Programs\Quarto\bin
      CodePage: 1252

[>] Checking basic markdown render....OK

[>] Checking Python 3 installation....OK
      Version: 3.10.4
      Path: C:/Users/Cris/AppData/Local/Programs/Python/Python310/python.exe
      Jupyter: 5.3.0
      Kernels: python3

[>] Checking Jupyter engine render....OK

[>] Checking R installation...........OK
      Version: 4.1.2
      Path: C:/PROGRA~1/R/R-41~1.2
      LibPaths:
        - C:/Program Files/R/R-4.1.2/library
      rmarkdown: (None)

      The rmarkdown package is not available in this R installation.
      Install with install.packages("rmarkdown")
```


### Checklist

- [x] Please include a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [x] Please [format your issue](https://quarto.org/bug-reports.html#formatting-make-githubs-markdown-work-for-us) so it is easier for us to read the bug report.
- [ ] Please document the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [x] Please document the operating system you're running. If on Linux, please provide the specific distribution.
- [x] Please provide the output of `quarto check` so we know which version of quarto and its dependencies you're running.
