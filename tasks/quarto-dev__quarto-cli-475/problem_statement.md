Process markdown in callout block caption and correctly escape for LaTeX output
This was first report by @t-kalinowski on slack. 

In callouts, the caption defined as header inside the block will create some errors when rendered to PDF. 

Example: 

````markdown
---
title: "A Bug"
format: pdf
---

::: callout-note
## Using the multi-assignment `%<-%` operator

The `%<-%` operator is ...
:::

````

This will throw issue because the caption is using some special characters, and currently text of caption is used _as is_ with no markdown processing. The caption will be `Using the multi-assignment %<-% operator` in the latex block below.

````latex
\begin{tcolorbox}[standard jigsaw,bottomtitle=1mm, opacityback=0, colframe=quarto-callout-note-color-frame, titlerule=0mm, toptitle=1mm, title=\textcolor{quarto-callout-note-color}{\faInfo}\hspace{0.5em}Using the multi-assignment %<-% operator, colback=white, coltitle=black, opacitybacktitle=0.6, arc=.35mm, rightrule=.15mm, bottomrule=.15mm, toprule=.15mm, left=2mm, colbacktitle=quarto-callout-note-color!10!white, leftrule=.75mm]
The \texttt{\%\textless{}-\%} operator is \ldots{}
\end{tcolorbox}
````

When not using a special character, it will throw an error but not markup will be applied

````markdown
---
title: "A Bug"
format: 
  pdf:
    keep-tex: true
---

::: callout-note
## Text in **strong**, and some `code`

Text in **strong**, and some `code`
:::
````
Text in header is not strong, nor formatted as code verbatim.
![image](https://user-images.githubusercontent.com/6791940/160381548-078fc482-0265-4c38-a464-a5b4ac150016.png)

Also, having characters like a comma `,` will also create issue because text is inserted _as is_ by the lua filter. 

````markdown
---
title: "A Bug"
format: 
  pdf:
    keep-tex: true
---

::: callout-note
## Text, separated with comma

content
:::
````
Error will be 
````
Package pgfkeys Error: I do not know the key '/tcb/separated with comma' and I am going to ignore it. Perhaps you misspelled it.
````
because the comma in title is seen as a new option in the block
````latex
\begin{tcolorbox}[standard jigsaw,bottomtitle=1mm, toptitle=1mm, colframe=quarto-callout-note-color-frame, arc=.35mm, coltitle=black, titlerule=0mm, colbacktitle=quarto-callout-note-color!10!white, toprule=.15mm, colback=white, title=\textcolor{quarto-callout-note-color}{\faInfo}\hspace{0.5em}Text, separated with comma, leftrule=.75mm, bottomrule=.15mm, rightrule=.15mm, left=2mm, opacitybacktitle=0.6, opacityback=0]
content
\end{tcolorbox}
````

I believe the lua filter should be apply, at least for PDF so that those cases above are working ok. 

## Proposed changes


Regarding the title, I believe some brackets should be added around the argument content

````diff
diff --git a/src/resources/filters/quarto-pre/callout.lua b/src/resources/filters/quarto-pre/callout.lua
index b021363d1..f2a69be31 100644
--- a/src/resources/filters/quarto-pre/callout.lua
+++ b/src/resources/filters/quarto-pre/callout.lua
@@ -307,7 +307,7 @@ function latexCalloutBoxDefault(caption, type, icon)
     bottomrule = borderWidth,
     rightrule = borderWidth,
     arc = borderRadius,
-    title = caption,
+    title = '{' .. caption .. '}',
     titlerule = '0mm',
     toptitle = '1mm',
     bottomtitle = '1mm',
````

Regarding, markdown processing,  currently, `pandoc.utils.stringify()` is used on header content. I believe using `pandoc.write()` would be better for this.

````diff
diff --git a/src/resources/filters/quarto-pre/callout.lua b/src/resources/filters/quarto-pre/callout.lua
index b021363d1..08d0c0402 100644
--- a/src/resources/filters/quarto-pre/callout.lua
+++ b/src/resources/filters/quarto-pre/callout.lua
@@ -254,7 +254,7 @@ function calloutLatex(div)
     if caption == nil then
       caption = displayName(type)
     else
-      caption = pandoc.utils.stringify(caption)
+      caption = pandoc.write(pandoc.Pandoc(pandoc.Para(caption)), FORMAT)
     end
     callout = latexCalloutBoxDefault(caption, type, icon)
   else
````

@dragonstyle I believe you wrote the filter ? Do you think there could be some issues with these changes ? 

I believe for HTML, it is processed correctly as markdown to produce correct HTML. I'll make a PR to ease the review


