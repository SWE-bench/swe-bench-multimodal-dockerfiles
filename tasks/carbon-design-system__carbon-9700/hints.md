@aagonzales we have a `hasForm` prop that allows things to span the full-width of the `Modal`, but it will also let the paragraph above go full width. 

The problem I think we're running into is that we are allowing consumers to render whatever they want inside of a modal, and the modal body has a varying padding-right based on the size of the screen. Since the inputs are also put inside the Modal body, they are affected by this as well (unless the `hasForm` prop has been provided). But like I pointed out, that will allow everything to go full width. 

Is the main reason for the right padding to constrain full-width paragraphs? If so, I wonder if we can just set the padding on all paragraph elements inside of the `Modal`. [We already set the font styles for all paragraphs](https://github.com/carbon-design-system/carbon/blob/main/packages/components/src/components/modal/_modal.scss#L269), so we would just be moving the padding from the modal body container to just the paragraphs. 
Yeah it would just be for paragraphs text that would be at the 20% padding. Everything else is full width. The storybook example was correct at some point in the past. 

The exception is the xs modal. https://www.carbondesignsystem.com/components/modal/style#margin-right