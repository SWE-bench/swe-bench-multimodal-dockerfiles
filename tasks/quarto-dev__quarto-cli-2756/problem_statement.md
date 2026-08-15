Theorems and Proofs with code blocks and no header/label cause Lua filter to error out
### Bug description

It's been a while since I reported a bug, here is a new one introduced in v1.1 (introduced between v1.1.67 and v1.1.149, and still in v1.1.165 or v1.2.15, likely to be c56d23e7690a5aec4e99b26310ffe12783807709).
This issue is platform/IDE independent.
Issue possibly related to #2166.

````
---
format: html
---

::: {#thm-line}

## Line (with or without the Lua filter error occurs)

```
1+1
```

:::
````

```bash
pandoc 
  to: html
  output-file: Untitled-1.html
  standalone: true
  section-divs: true
  html-math-method: mathjax
  wrap: none
  default-image-extension: png
  
metadata
  document-css: false
  link-citations: true
  date-format: long
  lang: en
  
Error running filter /Applications/quarto/share/filters/crossref/crossref.lua:
/Applications/quarto/share/filters/crossref/crossref.lua:97: bad argument #1 to 'insert' (table expected, got nil)
stack traceback:
        /Applications/quarto/share/filters/crossref/crossref.lua:97: in function 'tprepend'
        /Applications/quarto/share/filters/crossref/crossref.lua:2057: in local 'fn'
        /Applications/quarto/share/filters/crossref/crossref.lua:1154: in function </Applications/quarto/share/filters/crossref/crossref.lua:1148>
```

Currently the only way to use "Theorems and Proofs", is to fully specify those.

````
::: {#thm-line}

## Label

Some text

```
1+1
```

:::
````

### Checklist

- [X] Please include a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [X] Please [format your issue](https://yihui.org/issue/#please-format-your-issue-correctly) so it is easier for us to read the bug report.
- [X] Please document the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [X] Please document the operating system you're running. If on Linux, please provide the specific distribution.
Heading in theorem is included as item in list in theorem body
I was sketching a theorem using a bullet point list inside a div and stumbled upon the following issue.

The following minimal example using (un-)ordered lists inside a theorem div

```markdown
---
title: "unexpected caption item"
---

::: {#thm-unordered-list}
## This heading shouldn't have a bullet point

* This 
* unordered list (unexpectedly) includes the caption
:::


::: {#thm-ordered-list}
## This heading shouldn't have a bullet point

1. This 
2. ordered list (unexpectedly) includes the caption
:::
```
renders the  theorem caption as part of the list:
![unexpected_caption_item](https://user-images.githubusercontent.com/1757177/187035748-f024d444-d095-4b39-8627-c5dd787b311d.png)


