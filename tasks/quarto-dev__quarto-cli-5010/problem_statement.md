Non-standard URLs display correctly inline but not on image grid
### Bug description

Note the weird non-standard URL below (contains commas and other punctuation)



```
---
title: Clabbered milk
date: '2017-02-02'
categories:
  - food
---

Here is a blog post, blah blah.

Note how the following images both display just fine from within this post.

![another image from the web](http://assets.bonappetit.com/photos/57bf31396a6acdf3485df7f9/5:4/w_1028,c_limit/koji-steak-1.jpg)

![](diet-assets/clabberedMilk.jpg)

But inside the grid view, the image preview is broken.

```
Find a working full example at this repo: [richardsprague/quartosample: extrapage](https://github.com/richardsprague/quartosample/tree/extrapage)

Using 1.3.294 on a Mac OS 13.2

### Checklist

- [X] Please include a minimal, fully reproducible example in a single .qmd file? Please provide the whole file rather than the snippet you believe is causing the issue.
- [X] Please [format your issue](https://quarto.org/bug-reports.html#formatting-make-githubs-markdown-work-for-us) so it is easier for us to read the bug report.
- [ ] Please document the RStudio IDE version you're running (if applicable), by providing the value displayed in the "About RStudio" main menu dialog?
- [X] Please document the operating system you're running. If on Linux, please provide the specific distribution.
- [ ] Please provide the output of `quarto check` so we know which version of quarto and its dependencies you're running.
