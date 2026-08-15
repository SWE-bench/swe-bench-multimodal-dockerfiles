Hey @janhassel!

We took a look at this during our proposal grooming session this sprint and love the component 🔥 

I think the only feedback from the session was around visuals, @laurenmrice do you have a second to list out any changes that you would hope to see for it? Then either your team @janhassel could put something together or we could try and get this added to a sprint (which might take a bit)
@joshblack Good to hear! If we get a list of visual changes and feedback I'll try to secure some time for this and come back to you once I know more about if, how and when we can support this effort.
Hey Jan 👋 

Here are the design specs for the context menu! Basically the same thing as you have above but just detailing out the increments, etc. We can have you pair up with a dev on our team while you are contributing the code in case you have any questions.

Would you also be able to provide dev/design documentation guidance for the context menu? We can help revise any content that is written.


### Styles spec
---------
![Context menu - 32px row and 16px padding](https://user-images.githubusercontent.com/43969356/97744611-ed75e600-1abd-11eb-84b7-1fd75f1f04e4.png)

### Structure spec
---------
![Context menu - 32px row and 16px padding - spec](https://user-images.githubusercontent.com/43969356/97743530-3167eb80-1abc-11eb-9ed5-f093c141b90e.png)

### UI example
---------
![body-short-01 (no icon)](https://user-images.githubusercontent.com/43969356/97745511-5ca00a00-1abf-11eb-8809-0016eec3b158.png)




@laurenmrice Thanks a lot for the detailed visual specs, looks great!
Before I start working on this, what would be the preferred strategy here? Should this be a separate component called `ContextMenu` or should this be an update and extension to the existing `OverflowMenu`? I see use cases where a nested overflow menu would make a lot of sense for teams and visually they're relatively close. What do you think?
This should be a separate component called `Context Menu`. Just curious, is this the typical standard name for this kind of component (Context menu, contextual menu, control menu)?  @janhassel 