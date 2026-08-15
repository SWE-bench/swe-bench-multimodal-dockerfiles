Yes, we currently show this for anything under the stats root. Is there any reason why activity log was added to the stats path if we don't consider it a stat?
cc @kwonye @catehstn what are your preferences for behavior here?
@gwwar there's a good reasoning about why it's under Stats in p7pQDF-2Me-p2, in the #comment-10161 
For folks reading, the TLDR of the thread was we couldn't make another top level item in the sidebar (too crowded), and that activity "fit well together conceptually". There are open questions on if folks would have trouble finding it / or are using it that often.
A quick technical fix would be to expand the check while in the stats section to see if the current window location contains your sub-sections. eg

```jsx
if ( ! includes( ALLOWED_SECTIONS, currentSection ) ) {
	return null;
}

if ( currentSection === STATS && isInActivityLog ) {
	return null;
}
// ...
```

I don't think we have enough of a use case to dispatch additional information about the path for a general framework update though we can certainly revisit if folks see this happening often.

We're happy to help review if folks start a PR. I'm still interested to hear what @kwonye and @catehstn would prefer behavior wise here.
> A quick technical fix would be to expand the check while in the stats section to see if the current window location contains your sub-sections. eg

I agree with this approach, @gwwar. That stats is pretty focus on the general stats screen so it's out of place here in the activity log.
Agree with Will, we will want to revisit it when we have AL in the apps though (ETA: May).
Could the banner copy be upgraded to cover both the Stats and the Activity log? /cc @keoshi @MichaelArestad 
This is a symptom of a bigger problem, one that we caused ourselves for adding the Activity under Stats. Not saying it doesn't belong there, just saying the current placement was a consequence of us needing a physical place to add it, so we could focus on bigger things.

According to the user interviews we did ( p9rlnk-jD-p2 ), the current placement allows for an organic discovery of the AL:

> A lot of the discovery and traffic we’re getting on the AL seems to come from the fact that people use Stats very often.

But it also leads to unmatched expectations:

> A considerable number of people didn’t know what to expect or thought Activity would be an Analytics kind of product, i.e.: a different take on external impressions to their site.

Until we discuss the final naming/place in Calypso, and for the sake of this particular issue, I'd suggest removing the banner from Activity.