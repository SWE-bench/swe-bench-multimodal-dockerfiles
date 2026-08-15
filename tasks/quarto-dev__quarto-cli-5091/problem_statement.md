Nonstandard image URL won't render (PDF)
### Bug description

I'm trying to render this page as PDF. 
```qmd
---
title: Non-standard URL
---


![](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F9b7345d9-5f62-46dc-8062-d704c2c014a5_289x174.jpeg)
```

Breaks with this error:

```
running xelatex - 1
  This is XeTeX, Version 3.141592653-2.6-0.999994 (TeX Live 2022) (preloaded format=xelatex)
   restricted \write18 enabled.
  entering extended mode
  
updating tlmgr

updating existing packages

compilation failed- error
Unable to load picture or PDF file 'badurl_files/mediabag/https://bucket.jpeg'.
<to be read again> 
                   }
l.159 ...adurl_files/mediabag/https://bucket.jpeg}
```


Quarto version 1.3.306
OSX 13.3




### Checklist

- [X] Please include a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [X] Please [format your issue](https://quarto.org/bug-reports.html#formatting-make-githubs-markdown-work-for-us) so it is easier for us to read the bug report.
- [ ] Please document the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [X] Please document the operating system you're running. If on Linux, please provide the specific distribution.
- [ ] Please provide the output of `quarto check` so we know which version of quarto and its dependencies you're running.
