[This line](https://github.com/bpmn-io/bpmn-js/blob/014359523071b86f885e87e4204f92686b55b3d6/lib/features/modeling/behavior/DetachEventBehavior.js#L34) causes the problem, since the array length is more than 1 in this case DetachEventBehavior just does an early return instead of replacing elements.
Replacing elements.move preExecute in DetachEventBehaviour fixes the problem:

```
  this.preExecute('elements.move', function(context) {
    var shapes = context.shapes;

    shapes.filter(function(shape) {
      var hasHost = (shape.host && (context.shapes.indexOf(shape.host) > -1)) ? true : !!context.newHost;
      return shouldReplace(shape, hasHost);
    }).map(function(shape) {
      return shapes.indexOf(shape);
    }).forEach(function(index) {
      shapes[ index ] = replaceShape(shapes[ index ], bpmnReplace);
    });
  }, true);
```

This is the tricky part:

`      var hasHost = (shape.host && (context.shapes.indexOf(shape.host) > -1)) ? true : !!context.newHost;`

For edge cases where a boundary event is attached to a task and we move them all together, context.newHost is null however the Detach behaviour in that case should not apply to the Boundary Event (since it is being carried with its host), therefore we check if a shape has a host **and** this host is inside the moved shapes within the context to decide if it has a host or not, for other cases checking if context.newHost exists is enough. Since this is preExecute shape.host refers to the host before the replace.