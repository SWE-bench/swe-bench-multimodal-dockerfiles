It looks like there are three cells being emitted by bokeh if we run the corresponding .ipynb file:

```json
{
 "cells": [
  {
   "cell_type": "raw",
   "id": "ff951fb8",
   "metadata": {},
   "source": [
    "---\n",
    "title: test webpage\n",
    "format:\n",
    "  html:\n",
    "    code-fold: true\n",
    "keep-md: true\n",
    "keep-ipynb: true\n",
    "---"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "fig-demo",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "(function(root) {\n",
        "...",
       "}(window));"
      ],
      "application/vnd.bokehjs_load.v0+json": "(function(root) {...",
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "\n",
       "  <div class=\"bk-root\" id=\"9107e47f-bdc3-4fc2-9fc5-fc860b2b3abe\" data-root-id=\"1003\"></div>\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/javascript": [
       "(function(root) {\n",
        "...",
       "})(window);"
      ],
      "application/vnd.bokehjs_exec.v0+json": ""
     },
     "metadata": {
      "application/vnd.bokehjs_exec.v0+json": {
       "id": "1003"
      }
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "#| label: fig-demo\n",
    "#| fig-cap: This is a demo figure for debug\n",
    "\n",
    "from bokeh.io import output_notebook\n",
    "output_notebook(hide_banner=True)\n",
    "\n",
    "from bokeh.palettes import Spectral5\n",
    "from bokeh.plotting import figure, show\n",
    "from bokeh.sampledata.autompg import autompg as df\n",
    "from bokeh.transform import factor_cmap\n",
    "\n",
    "df.cyl = df.cyl.astype(str)\n",
    "group = df.groupby('cyl')\n",
    "cyl_cmap = factor_cmap('cyl', palette=Spectral5, factors=sorted(df.cyl.unique()))\n",
    "p = figure(height=350, x_range=group, title=\"MPG by # Cylinders\", toolbar_location=None, tools=\"\")\n",
    "p.vbar(x='cyl', top='mpg_mean', width=1, source=group, line_color=cyl_cmap, fill_color=cyl_cmap)\n",
    "show(p)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "36ad8b05",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

I think what's happening is that `bokeh` or `jupyter` is using the `"output_type": "display_data"` entry in the output to denote that this is "not really" an output cell, and so we should treat these differently in our output.

Yes. The example in another issue will have the same problem when you set the figure label as `fig-xxx`.

https://github.com/quarto-dev/quarto-cli/issues/1867
https://jja.quarto.pub/quarto-basics/
Hi @cscheid , can I set `fig-subcap: false`? I try this option but it is not working.
No, it doesn't work like that; that option is for you to provide the different subcaptions, instead of enabling or disabling it
Thank @cscheid . I found `fig-subcap: true` in the document (https://quarto.org/docs/authoring/cross-references.html). So I though there is a `fig-subcap: false` option.
@y9c the documentation you linked says: "If you’d like subfigure captions that include only an identifier, e.g. “(a)”, and not a text caption, then specify `fig-subcap: true` rather than providing explicit subcaption text:"

Thank you @cscheid . 

I would like to know if there is a quick solution to fix this on the user side. Or I need to wait for a patch commit for this. 
Hi @cscheid, 

Is there a solution to remove subfigure caption?

Thanks.
You will see an update here when this issue is addressed.