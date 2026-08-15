We simply match patterns... can you point me (or explain) F#'s grammar rules here?  I just looked at their own spec and they clearly say `(*` begins a new multi-line comment... they don't seem to show the grammar for the whole top-level (which would be super helpful).

How would we (since we're just pattern matching) know that this is NOT a comment?  How does F#? Any links or info you could provide would be helpful.
Im pretty new to F# but a multi-line should be like

(*
My comment
*)

With a closing *). I have no idea how F# would distinguish from a
multi-line and say mutliplying twice

1
|> (*) 2
|> (*) 4

Since that does have an apparent closing *).

Idk much more about the language but github seems to highlight it properly
when i wrote it for this issue.

On Mon, Sep 21, 2020, 11:14 AM Josh Goebel <notifications@github.com> wrote:

> We simply match patterns... can you point me (or explain) F#'s grammar
> rules here? I just looked at their own spec and they clearly say (*
> beings a new multi-line comment... they don't seem to show the grammar for
> the whole top-level (which would be super helpful).
>
> How would we (since we're just pattern matching) know that this is NOT a
> comment? How does F#?
>
> —
> You are receiving this because you authored the thread.
> Reply to this email directly, view it on GitHub
> <https://github.com/highlightjs/highlight.js/issues/2697#issuecomment-696085529>,
> or unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AFC3BOLU42WK4YEGT3TFPL3SG5CDHANCNFSM4RUCLZKA>
> .
>

Is this a valid comment:

```
(*)
My comment
(*)
```

If `(*` and `*)` simple have to be their own "tokens" separated by space that shouldn't be a terrible fix.
It shouldnt be, no. (*) is a function so it should evaluate it. Then try to
evaluate the "My" symbol and throw an error because its not defined
probably.

On Mon, Sep 21, 2020, 12:36 PM Josh Goebel <notifications@github.com> wrote:

> Is this a valid comment:
>
> (*)
> My comment
> (*)
>
> —
> You are receiving this because you authored the thread.
> Reply to this email directly, view it on GitHub
> <https://github.com/highlightjs/highlight.js/issues/2697#issuecomment-696230556>,
> or unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AFC3BOI3YUYCLHRGTHI36WDSG56G7ANCNFSM4RUCLZKA>
> .
>

>  If more than one token can match a sequence of characters in the source file, lexical processing always forms the longest possible lexical element.

Ah I think that explains it... So the trick is indeed it needs to be "isolated" so the lexer sees it as it as a comment start/end instead of something **longer** (like a function).