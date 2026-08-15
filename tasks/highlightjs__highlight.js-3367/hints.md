> `print(1if 0==0else"b")`

First facts: This if of course broken since our number regex in Python requires word boundaries (which do not exist between `0` and `e`... making 0 not a number... and the keyword regex is `\w+` (the default), which matches `0else` which is NOT a keyword.

> As keywords and variables cannot start with a number in Python, the space between a number and a keyword can be skipped.

This is **terrible** style though and it doesn't bother me much if we don't support it (_and code golf in general_).  I also imagine it could result in potential false positives if we remove the boundary checks for numbers.  If someone wants to play around with a fix happy to review a PR.  But if the fix has ill effects for regular (non golf code) code or detrimental effects on auto-detection then that's an issue.

> (Also, also should print be a built-in here?)

_See comments in `python.js` regarding this._
It's also possible one half of this might be more easily fixed than the other... perhaps the keyword can be fixed just by declaring that keywords in Python can never start with a numeral? Is this true?
> This is terrible style though and it doesn't bother me much if we don't support it (and code golf in general).

I absolutely agree, but wanted to create the issue anyway just in case it's easier to fix than I thought.

> It's also possible one half of this might be more easily fixed than the other... perhaps the keyword can be fixed just by declaring that keywords in Python can never start with a numeral? Is this true?

I don't think there are keywords that start with a number, but not entirely sure.
https://docs.python.org/3.8/reference/lexical_analysis.html#keywords

So I think just altering `$pattern` would fix half the issues here.
https://docs.python.org/3.8/reference/lexical_analysis.html#keywords
Reaching out to the author of the PR for our Python numeric support so see if there is a reason for all those `\b` at the end of number matches.  But if this boils down to "better support average python" vs "better support code golf" (with no easy/clear solution) then I'll probably close this a #wontfix and just say that code golf is not our specialty.  We'll see.