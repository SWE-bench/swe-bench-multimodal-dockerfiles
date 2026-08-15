Hi, thanks for the report. I can reproduce this issue.

The `implicit-arrow-linebreak` rule has a lot of logic that deals with trying to move around comments when autofixing, whereas most other rules just skip autofixing if there's a comment in the way. It would probably be worth into whether this particular comment-moving issue can be easily fixed, but if not I think it would be better to just remove the comment-moving logic from `implicit-arrow-linebreak` and skip autofixing if there's a comment in the wrong place.
I'll look into this.