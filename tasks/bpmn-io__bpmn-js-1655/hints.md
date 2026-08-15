This happens in [SetColorHandler](https://github.com/bpmn-io/bpmn-js/blob/develop/lib/features/modeling/cmd/SetColorHandler.js). This is because when setting the color of a multi element selection, the external label is considered as a standalone element. For a single element, only the shape is selected and the label color is derived from it.
> warning This only happens if color is applied to selection of element + element label.

From what I found this also happens when you apply on the label itself.
Yes, I will update correctly @nikku 