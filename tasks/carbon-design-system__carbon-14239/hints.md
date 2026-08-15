@kglickman Thanks for reporting these. 

> the StructuredList elements have roles and buttons can't have children with roles

Could you share the specific rule you're referring to here? I'm not sure how we should tackle this issue. Right now the check for interactive elements relies on if the elements can receive focus. We could consider expanding the check to assert if child elements have certain roles that would require the ExpandableTile to not be a button. I'd prefer to avoid providing a way to manually toggle the ExpandableTile behavior for interactive vs. not. It would be a huge footgun.


For the second issue when expandable tile has interactive elements, I think the `aria-expands` should be removed from the containing div that has the error. The expando icon `button` should get `aria-controls` with a value of the id of the container (`expandable-tile-1` in the storybook).


The exact error message is "The element with role "button" contains descendants with roles "table" which are ignored by browsers" There is a "Learn more" which says:

This rule is triggered when one of the following elements contain more than presentational descendants: button, checkbox, img, math, menuitemcheckbox, menuitemradio, option, progressbar, radio, scrollbar, separator, slider, switch, and tab. Refer to the table in [ARIA in HTML - Allowed descendants of ARIA roles](https://www.w3.org/TR/html-aria/#allowed-descendants-of-aria-roles) for the normative definition for each ARIA role, the kinds of content categories for each role, and what [kinds of elements](https://html.spec.whatwg.org/multipage/dom.html#kinds-of-content) can be descendants.

For example, a <button> allows text and images, but does not allow [interactive content](https://html.spec.whatwg.org/multipage/dom.html#interactive-content-2) or descendants with a tabindex attribute because that would confuse assistive technology users as to the expected content or behavior of the button.