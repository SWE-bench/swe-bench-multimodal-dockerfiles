> Somehow, the behavior is not totally consistent here as some things in the braces are highlighted.

Because we don't support "nesting" of any type... so sometimes the nested `}` will cause the rule to terminate early allowing it to match again... it's not matching "inside" though... it's just the pattern terminating early because we don't handle nesting.  Of course we definitely could... that's what we have "self" for.

At best I'd consider our Latex support to be more of a "placeholder" than a real grammar...  If someone would like to pitch in here to help I'd be more than happy to answer any HLJS specific questions about our grammars, etc.

Ok, I will give it a shot.
Check out `tools/developer.html`... can be a real help. (you'll need to first build a browser build)