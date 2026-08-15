Personally prefer a control to a story, a disabled story would be odd.

Perhaps also read only specific color tokens e.g. $border-readonly
- MDX file update?
Q: A little concerned elsewhere we are using `readOnly` as opposed to the standard attribute `readonly`. Will this not cause confusion?
@lee-chase I'll jump in and try to answer some of these questions.

> Personally prefer a control to a story, a disabled story would be odd.

We apply VRT to each story in the storybook. By having a dedicated story titled "readonly" we can ensure there are no visual regressions over time. I'm really either/or on this one though - we don't usually have specific stories for other states like `invalid`. This could be a follow-on item later. For now it can be a control on the "playground" story imo

> Perhaps also read only specific color tokens e.g. $border-readonly

My guess is no, we won't add these as tokens. Adding tokens has lots of implications across the system. Ultimately this is a question for design though, @aagonzales what are your thoughts?

> MDX file update?

Story files should import an .mdx file that corresponds to the "docs" tab in storybook. This .mdx file will need updated to include the readonly story as well as light docs on how/when to use the readonly prop/variant.

> Q: A little concerned elsewhere we are using readOnly as opposed to the standard attribute readonly. Will this not cause confusion?

Yeah I think the standard attribute should be used here where possible, following convention of how we use other standard attributes like `title`. I think it should be listed as a prop and probably just have a proptype of `bool`.