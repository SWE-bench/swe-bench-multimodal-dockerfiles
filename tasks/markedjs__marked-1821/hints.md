The [strikethrough spec ](https://github.github.com/gfm/#strikethrough-extension-) is not very specific on what counts and even github allows single `~`'s to be strikethrough

`~test~`: ~test~
`~~test~`: ~~test~
`~test~~`: ~test~~
`~~test~~`: ~~test~~

It looks like when a different amount of `~`'s are used it should not count.