Yes, we only know it's a function if it uses the `function name` syntax... in these cases (inside a class) it's hard to tell those apart from simple function calls, which look identical (and we don't highlight).

If we highlighted `[identifier]([params]) {` I wonder if that would work or if there are other places you might find that in JS?  Yeah that's no good because this is valid JS:

```
functionCall()
{} // a block of some sort
```


Not sure there is any great way to do this, but flagging it as feature and needs help if someone motivated comes along.
@joshgoebel @allejo 

I just looked to see how Prism solves this (if they do) and they solve it just by coloring both invocations and definitions the same... ie, making no distinction... once you stop worrying about that it's easy to just match the `something(...)` pattern as a function definition OR dispatch.

Of could we could add some distinction, but I still think these would be "title"s... perhaps `.invoke.title` (in cases where we could detect the difference)?  Defaulting to picking up the same styles as `.title` but easy for themes to override... or perhaps it's better to not be so specific... Prism sure seems to be benefiting from the "broadness" of their definition on this one.

Thoughts?

I think we should perhaps consider the same or else I'm considering closing this as a "cant fix".
Closing as "cantfix".  We simply can't distinguish these from function dispatch (which we do not highlight), so there is no way for us to know these are function definitions.  I may go ahead and remove the special hard-coded `constructor` case also just to remove the inconsistency of highlighting constructor but not the others.

If we did decide to highlight function invocation in the future then these would pick up some color from that, but that is really a separate concern unrelated to this issue directly.