Bash is a very simple grammar and could probably use a champion if one wanted to step up.  We definitely could improve support for here docs and here strings (if we can detect them).

- Pretty sure we already handle sub-shell variables. (ok, no, we only handle  $() variables inside a string)
- Shell doesn't know anything about `\`.  That's possibly something we could fix that would improve `shell` substantially.

Operators is something we traditionally do not highlight (on purpose), but there is a separate discussion regarding that:

https://github.com/highlightjs/highlight.js/issues/2500
@yyyc514 Thanks for the pointers.
Also noticing numbers/integers aren't highlighted, as in: 
```sh
x=3
phoneNum=5557778888
```
etc.