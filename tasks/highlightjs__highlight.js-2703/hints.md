Can you please confirm this issue on latest and if possible provider a jsfiddle reproducing?

You can borrow my template:
https://jsfiddle.net/ajoshguy/nagkqytv/18/
Yes, it's still present for Scala highlighting with version `9.15.10`. One thing to note is that I see it's not just Scala related. I see same happening for Kotlin as well. Maybe it affects all languages with similar syntax (reusing same parsers).

Fiddle with Scala: https://jsfiddle.net/y58dnucs/3/
Fiddle with Kotlin: https://jsfiddle.net/9j6uwdnr/
I imagine the "class" rule is looking for { to end the match and not expecting comments... so we'd need to teach both grammars that comments could pop up in the middle of "starting a class". That's off the top of my head without looking.
If you'd like to take a pass at making a PR it'd be welcomed.
