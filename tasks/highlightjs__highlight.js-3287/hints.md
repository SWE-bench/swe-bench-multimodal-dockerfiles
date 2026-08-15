- Are block comments allowed in this context as well as line comments (I'd assume so?)
- Must the backtick start the line or just be the first non-whitespace for it to be special/meta?
- Does <code>`BLAHBLAH</code> always denote a constant?  Are constants typically (or required) to be uppercase in Verilog?
Thanks for the reply!

> * Are block comments allowed in this context as well as line comments (I'd assume so?)

Yes, both line comments and block comments are allowed in this context.

> * Must the backtick start the line or just be the first non-whitespace for it to be special/meta?

In Verilog, it seems that compiler directives (meta) can be placed anywhere in the code.
(But generally at the beginning of the line).
You can also include line breaks in meta by backslash (`\`), just like in C.

In order to identify `meta` scope, I think you need to make sure that the backtick is followed by specific keywords.
The Verilog meta definition seems to list all the keywords for compiler directives, so I think it can be used.
https://github.com/highlightjs/highlight.js/blob/ba8735ff6645dcffd13544d5434a8bef184ea7c0/src/languages/verilog.js#L118-L123

> * Does `` `BLAHBLAH `` always denote a constant?  Are constants typically (or required) to be uppercase in Verilog?

`` `BLAHBLAH `` indicates that BLAHBLAH is the identifier defined by `` `define ``, which is normally a constant.
Constants are typically in uppercase, but are not required.
