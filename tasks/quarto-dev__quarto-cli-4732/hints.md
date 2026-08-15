Have tried both `embed` and `verbatim`.
The reason the report in #1237 isn't resolved for include specifically is that the include shortcode resolution happens in typescript, before Pandoc. Other shortcodes like meta, var, etc, happen in Lua.

We need to add include processing to Lua in one shape or another, but this is easier said than done. We need to be aware of a number of issues, and it's also going to be the case that a "Lua `{{< include >}}`" will behave differently than a typescript one out of necessity. This is going to be very confusing for users.
@aronatkins Did you try pre release yet ? 

I can't reproduce with 1.3. From 
````markdown
---
title: embedding with reveal
format: revealjs
engine: knitr
---

## Embed!

```{embed, file = "code.R"}
```
````

I get 

![image](https://user-images.githubusercontent.com/6791940/223865829-8a406a7c-107e-4d08-839b-03eb59c8f01a.png)

But I can reproduce with verbatim. 

Using also knitr 1.42 

Either some adjusments in quarto or something with **knitr** - I can have a look to this @cscheid 

Oh I know - this is a side effect of a default we have for revealjs. 
This is the default for revealjs format in Quarto. 
````
execute:
  echo: false
````

We do that because minimal space on slides so by default we choose to hide code source. This is documented for this format. 
https://quarto.org/docs/presentations/revealjs/#code-echo

For `verbatim` or `embed` to work, `echo: true` is needed.  Add `#| echo: true` in your chunk (or `echo = TRUE` next to engine name)

We should probably handle specifically those engine with an option hook as they need to have `echo = TRUE` for knitr to output with source hook, and they have no output. 


In fact there is something new now since #3429 - v1.3 has added internally a `embed` handler for this feature thttps://quarto.org/docs/prerelease/1.3/embed.html 

For now we pass every cell handlers from quarto to **knitr**
https://github.com/quarto-dev/quarto-cli/blob/5e38e1e9f19868e5dd2cb9ff5773442e35cc71f4/src/resources/rmd/execute.R#L54-L68

This creates a conflict (and why I get something with 1.3 using `embed` on cell with knitr - but wrong output when looking at HTML produced). 

@cscheid @dragonstyle do all the language handler we have are supposed to pass to **knitr** ? Does setting 
````markdown
```{embed}
````
inside a document using knitr computation engine is supposed to be handled by our internal handler, or should we **NOT** overwrite knitr own `embed` engine ? 

@cscheid @dragonstyle I need your input before doing more I have a fix already for `verbatim` engine, but `embed` knitr engine was not used as I would expect. I understand why now. I have some ideas on what to do, but need the full context to be sure.

What I think we should do : `embed` should be filtered out `handledLanguages` to support as knitr's engine for cells

I'll go with that, unless you think otherwise.