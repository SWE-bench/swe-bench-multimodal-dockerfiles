This is stemming from changes made in https://github.com/carbon-design-system/carbon/pull/12974

> NOTE: I still think it might worthwhile to consider simplifying things and simply make `hideLabel` work without being tied to `aria-labelledby`. The reason being is that the `for` attribute on the label can also be used to tie a label to a `Toggle` component and that should be A11Y compliant as well. So by requiring `aria-labelledby` be used in conjunction with `hideLabel` it seems to not be supporting the alternate `for` attribute with the label. (see below for an illustration)

@janhassel What do you think here? Updating the storybook props description to clarify the relationship between these two props makes sense, but curious if you feel they should be explicitly linked even when `for` is an option?
I agree, the documentation could be improved to describe the behavior better.

@fbarroso24 I'd be interested in your specific use case that leverages `<label for="id">` but shouldn't be in `props.labelText`. Could you share more details to help me understand?

If you're an IBMer, feel free to reach out via slack (`@jan.hassel`) as well.
> I agree, the documentation could be improved to describe the behavior better.
> 
> @fbarroso24 I'd be interested in your specific use case that leverages `<label for="id">` but shouldn't be in `props.labelText`. Could you share more details to help me understand?
> 
> If you're an IBMer, feel free to reach out via slack (`@jan.hassel`) as well.

@janhassel it depends on the use case really.   The following link describes various ways to apply labels that are A11Y compliant: https://www.w3.org/WAI/tutorials/forms/labels/.
NOTE: The example isn't for a `Toggle` but it simply describes the various ways to tie labels to inputs.
![image](https://user-images.githubusercontent.com/8657768/214324605-959b06bc-7339-4fe0-8409-3eeeff28f652.png)

The key difference is where the label resides.
`labelText`: It's set directly on the `Toggle` component
`aria-labelledBy`: Label comes from another component but this Toggle is aware of the other element's id
`for`:  Label comes from another component.  However, this toggle doesn't need to know where the label comes from.  The element using the `for` attribute will need to know this `Toggle`'s id however.

For this `Toggle` component, the `aria-labelledby`, `labelText` can be used to supply a label and would be set via the code that initializes the `Toggle` component.  However, if the label to use on this toggle is generated via another component than that would be a use case where the `for` attribute would be used in the other component to tie that label to the `Toggle` component.

Specifying a label on the Toggle and a label via the `for` attribute would actually result in a `A11Y` violation because you'd have 2 labels pointing to 1 input.
I see your point, @fbarroso24

@tay1orjones I'm unsure how this would best work in a component library while trying to ensure accessibility requirements are met. If we wouldn't wanna verify there is an actual `<label>` referring to the toggle's id via `document.querySelector` or alike, I don't think there is much we can do except making `props.labelText` optional and just hope that users would populate it when they need to...

Long term, it may be worth exploring if the current `props.hideLabel` behavior should be made more explicit with sth like `props.renderLabelOnSide` (bad naming, I know, just for illustrative purposes.). This would be a breaking change imo so couldn't happen before v12 (except under feature flag).
The a11y issue with the double label would still remain though if we would follow how other components (e.g. `TextInput`) are handling `props.hideLabel` as they just make the `<label>` element visually hidden but still keep the relationship.
> I don't think there is much we can do except making` props.labelText` optional and just hope that users would populate it when they need to...

@janhassel Yeah, this is probably the best course of action. Also ensure that it is well documented. This could include

1. A sentence/paragraph explaining this relationship in the `toggle.mdx` storybook docs
2. Mirror this content from `toggle.mdx` into the "Development considerations" on the website [here](https://carbondesignsystem.com/components/toggle/accessibility#development-considerations)
3. [Optional] Add a new story titled "with accessible labels" showing proper usage of all three scenarios
    * `labelText`
    * `aria-labelledBy`
    * `for`

