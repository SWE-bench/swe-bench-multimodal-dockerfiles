Here is the HTML diff between two options. 
````diff
-<section class="quarto-title-block">
+<section id="title-slide" class="quarto-title-block center">
   <h1 class="title">Test</h1>
   <p class="subtitle">Test</p>
````

Somehow the id is removed (not set) and we use that for styling

https://github.com/quarto-dev/quarto-cli/blob/f00d8fd7fee31e2bf5d4e30ec81d87bb2e43479d/src/resources/formats/revealjs/quarto.scss#L201-L207

Either an issue with hash value effect, or just some CSS adjustment for when this hash is used.


We are removing the id explicitly , which mess up the CSS has it is based on it.
https://github.com/quarto-dev/quarto-cli/blob/1366f078a03d14af2f5ee532eb03214a74b209a6/src/format/reveal/format-reveal.ts#L388-L395

We're removing the id otherwise, the title slide won't have a number as `hash-type` is defining. 

One solution could be to adapt the CSS to target without the id