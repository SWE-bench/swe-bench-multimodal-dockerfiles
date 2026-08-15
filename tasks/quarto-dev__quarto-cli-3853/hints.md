A quick grep of quarto's source code for `leavevmode` yields this:

```
$ rg leavevmode -l
tests/docs/templates/acm/acm_proc_article-sp.cls
tests/docs/templates/elsevier/elsarticle.cls
tests/docs/extensions/format/academic/_extensions/quarto-journals/elsevier/elsarticle.cls
tests/docs/extensions/format/academic/_extensions/quarto-journals/acm/acm_proc_article-sp.cls
tests/docs/extensions/project/_extensions/quarto-journals/springer/sn-jnl.cls
```

So we're not inserting `leavevmode` ourselves. Searching for `leavevmode pandoc` on google yields this:

https://github.com/jgm/pandoc/issues/2704

This doesn't appear to be a bug on our side.
Comparing with bookdown, the following labeled definition environment

```
::: {.definition #mydef}
foo
:::
```
generates
```
\begin{definition}
\protect\hypertarget{def:mydef}{}\label{def:mydef}foo
\end{definition}
```
which is different to quarto, and it doesn't add any additional space before the environment.

Both bookdown and quarto uses pandoc, so i guess their are just invoking pandoc with different arguments.
A possible solution would be to know if there is some specific argument that causes pandoc to behave different, and instruct quarto to do the same.

What do you think?
For what it's worth, bookdown uses a [lua filter to deal with custom environments](https://github.com/rstudio/bookdown/blob/dfe92a227b1dce5b8f0a2f758fb545e7df1b7e62/inst/rmarkdown/lua/custom-environment.lua#L129-L156). 


Here is some context about this `\leavevmode` insertion. 

## TL;DR

* When processing those block in Quarto we keep a Div with an id and only modify the content to add the raw latex needed
* This will let Pandoc writer handle the id part by inserting `\hypertarget` and add the `\leavevmode` part causing the issue then in LaTeX

* Removing the id on the Div could be the solution

## Details

This is added by Pandoc writer following the fix of the issue Carlos pointed to (
https://github.com/jgm/pandoc/commit/46135ac8758c4fbb9dfe676b1462463f5476bbff). It was added with one purpose at the time. See [comment](https://github.com/jgm/pandoc/issues/2704#issuecomment-283651736)
> The fix I've committed adds the `\leavevmode` in one particular case only:  when  you have a Div with an id (which will trigger a hypertarget) and the first block in the Div is a paragraph.  That at least handles the pandoc-citeproc case well,  without causing any problems I've yet noticed...

One user did warn about the vertical spacing that could happen though. (https://github.com/jgm/pandoc/issues/2704#issuecomment-283644668) 

The `\vadjust pre` is from https://github.com/jgm/pandoc/issues/7078 after a discussion about whether this `\leavemode` is still needed. 

It seems it was only aimed at Beamer for citation links - we are not in this case. So maybe this is an argument to ask for change ? 

Anyway, we could maybe fix on our side based on the why above and difference with **bookdown**. 

In **bookdown**, you don't have the issue because we are by passing the Pandoc writer on the insertion the `hypertarget`. We are inserting ourself the raw LaTeX in the custom block created. 
https://github.com/rstudio/bookdown/blob/dfe92a227b1dce5b8f0a2f758fb545e7df1b7e62/inst/rmarkdown/lua/custom-environment.lua#L137
So no `\leavevmode` introduced by Pandoc because of a Div with an id - you get the result shared just above. 
I think we did that to keep the `\hypertarget `with the `\label`

Removing the id on the Div in `theorem.lua` would probably fix the issue. I don't know if the `\hypertarget` part is really needed here. 🤔 We could add inside the content, as in **bookdown** or not; 

@cscheid @dragonstyle if we remove the id on the div, could this break crossref or is it read already and process by the internal value ? 
https://github.com/quarto-dev/quarto-cli/blob/f7fce46f348aeadb7fa902e3ca88568a27158f45/src/resources/filters/crossref/theorems.lua#L47-L50

I'll try a PR and we can adapt
