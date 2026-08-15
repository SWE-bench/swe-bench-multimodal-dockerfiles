Thanks for reporting this. Can you create a PR to fix this?
It looks like we just need to check for `this.options.gfm` around this code

https://github.com/markedjs/marked/blob/da071c9e408faceec944c0df4b8d4fac43c47d3d/src/Tokenizer.js#L280-L286
Thanks for reporting this. Can you create a PR to fix this?
It looks like we just need to check for `this.options.gfm` around this code

https://github.com/markedjs/marked/blob/da071c9e408faceec944c0df4b8d4fac43c47d3d/src/Tokenizer.js#L280-L286