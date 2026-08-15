It looks like we're trim()'ing the string which doesn't work when the first line has meaningful indentation...
Note that this trimming is happening on the _output_ of a call. So it seems it must be happening in our .R files somewhere.
Any update with this? 
It seems not as the current status of the issue is opened.
> Note that this trimming is happening on the output of a call. So it seems it must be happening in our .R files somewhere.

The trimming is here @cscheid line 901
https://github.com/quarto-dev/quarto-cli/blob/d076ea1e07e496ef879c31c1adb645318587ab9d/src/resources/rmd/hooks.R#L891-L904

We do it for all content we put in `cell-output-display` div. I wonder if removing the trim would break stuff... 

It would probably change some current output but it seems we shouldn't trim... 

What do you think about this ? 
@cderv the current behavior is definitely a bug. I would start by replacing `trimws(x)` with `x` in a branch and running the test suite...