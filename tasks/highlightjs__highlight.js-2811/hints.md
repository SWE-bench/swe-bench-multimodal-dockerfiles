Looking at the current implementation, it's assumed that any line starting `@` will be _meta_ throughout:

https://github.com/highlightjs/highlight.js/blob/deea7b7ed8f8e62b38b2eb07c935af5592850c9c/src/languages/python.js#L276-L279

Yep, should be a pretty easy fix (allow comments inside that rule)... want to try a PR?
Actually what we really may want is the ending to just end if it sees a comment upcoming:

```
 { 
   className: 'meta', 
   begin: /^[\t ]*@/, end: /$|(?=#)/ 
 }, 
```

Or some such... Though a proper regex to match just the decorator would be good if that's a known thing.
> a proper regex to match just the decorator

Decorators can be complicated, it's basically `@` followed by any expression! You can have decorator _factory_ functions with  parameters, for example:

```python
@surround_with("#", repeat=3)
              # ^ not a comment!
def text():
    return "hi!"

text()  # => ###hi!###
```
I'll have a play with it this weekend and see if I can get a PR together.
Can it be like:

```
@1 + 2 * 6
```

Then?  Or it's gotta be a name or function type expression?
It used to need to be _"a dotted name, optionally followed by a single call"_ per [the grammar][2]:

```
decorator: '@' dotted_name [ '(' [arglist] ')' ] NEWLINE
decorators: decorator+
```

From Python 3.9, though, as [PEP 614][1] relaxed the rules, it can be any expression per [the new grammar][3]:

```
decorators: ('@' named_expression NEWLINE )+ 
```

  [1]: https://www.python.org/dev/peps/pep-0614/
  [2]: https://docs.python.org/3.8/reference/grammar.html
  [3]: https://docs.python.org/3.9/reference/grammar.html
If you have a grasp on this I'll just wait to see the PR and markup tests (of which I hope there will be quite a few variants)... but if it truly can be any old expression I'm worried it could be a bit complex...  although perhaps all we really need is a simple mode that allows for strings, comments, and then this simply solves itself.

Although I'm curious about the meta styling fighting with the other styles, but we can talk about that once we have a PR I suppose. :)