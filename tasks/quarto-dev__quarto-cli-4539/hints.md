(See the comments on #4272 after the original issue was closed).
Thanks for letting me know about this. Will test and figure out the problem.
Upstream Pandoc issue that is causing the problem: https://github.com/jgm/pandoc/issues/8647

Update:

Their parser is not actually fully generic of the possible HTML tables, and some of these issues are triggered by tables emitted by gt.  Specifically, Pandoc is fairly opinionated in where it expects to read and emit th vs td elements, and mixes them up in an HTML->Native->HTML round trip for a number of scenarios.
Unfortunately, I think quarto should support a pretty faithful preservation of th vs td, in particular because this has accessibility impacts. This change is unlikely to appear in Pandoc (see discussion in the link above), so we'll have to work around it on our side.
If I understand correctly, this should be fixed as of 1.3.222. I just updated to 1.3.224 and is still experiencing the issue with the example code above.
I can repro it here, thanks for flagging.