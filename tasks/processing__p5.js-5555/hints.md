Thanks for the clear research and write-up!

This is a bit of a point of flip-flopping on my part historically. 'alpha' was false by default until [this PR](https://github.com/processing/p5.js/pull/3835) which was in response to [this issue](https://github.com/processing/p5.js/issues/3816).

The goal was to make the default behavior feel as close to the 2D renderer as possible, in that specific instance I was most concerned with what was expected from graphics objects. That said, I think I agree that alpha defaulting to false may prevent more unexpected behavior for more people. 