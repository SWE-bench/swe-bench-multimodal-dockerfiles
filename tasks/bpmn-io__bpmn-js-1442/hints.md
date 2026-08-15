Root-Cause:

The elements are added in order from left to right, but on the same Sequenz flow. Because of that, the second element comes first, see the gif below:
![recording](https://user-images.githubusercontent.com/21984219/116685777-2f231300-a9b3-11eb-8002-e6320582cf2c.gif)

__Solution Ideas__
I see two options:
1. Add the Elements back-to-front.
2. Determine the target-Flow again after each element is created

However, both have Problems:
1. I have made a draft implementation in the linked diagram-js PR. However, reversing the order in which the elements are added in the `CreateElementsHandler` makes assumptions about the structure of the arguments hand feels like a hack.
__EDIT__: This will actually break the Nested elements, such as Participants/Sub-Processes. We would probably have to change the Tree-destructuring from https://github.com/bpmn-io/diagram-js/blob/master/lib/features/copy-paste/CopyPaste.js#L296
2. The mouse event targets only one flow, so we do not have references to the next target flow. I'm not 100% sure if this approach can be achieve this without a bigger refactoring.

@philippfromme , I'd be interested in your opinion on this. Would changing the order when copying the shapes (opposed to when creating the new ones) make this less hacky?
Honestly, I think we should disable this behavior when more than one shape is created. We simply cannot know what connections to create if we are creating multiple shapes at the same time. The behavior can also easily blow up completely:

![yX9DFnWuCq](https://user-images.githubusercontent.com/7633572/116692795-38b17880-a9bd-11eb-9844-4f6f2a957e50.gif)

The behavior was created at a time when only single elements could be created.
Moving the elements is rejected so pasting should be rejected, too:

![O0Lj6CJnIq](https://user-images.githubusercontent.com/7633572/116693204-db69f700-a9bd-11eb-8ceb-559b793d1d18.gif)

That sounds reasonable, I'll see if we can reuse logic from movement for pasting as well