`hash-type: number` breaks alignment on title slide
### Bug description

Using `hash-type: number` misaligns the title slide on revealjs. Reprex:

````qmd
---
title: Test
subtitle: Test
author: Test
institute: Test
date: today
format:
  revealjs:
    hash-type: number # "title" works fine
---
````

Version with `hash-type: number`
![Broken_Version](https://user-images.githubusercontent.com/62679873/219854721-1916fb66-f79d-438f-aa6f-9f956af87ae9.png)

Version with `hash-type: title`
![Working_Version](https://user-images.githubusercontent.com/62679873/219854738-3b097a5d-85e7-45d6-a8e7-ee1572d265d4.png)


---

Using the latest nightly build on Fedora 37.



### Checklist

- [X] Please include a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [X] Please [format your issue](https://quarto.org/bug-reports.html#formatting-make-githubs-markdown-work-for-us) so it is easier for us to read the bug report.
- [X] Please document the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [X] Please document the operating system you're running. If on Linux, please provide the specific distribution.
