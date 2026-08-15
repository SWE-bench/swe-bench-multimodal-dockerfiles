The properties are lost because they aren't copied when changing multi-instance:

```javascript
var loopCharacteristics;

if (entry.active) {
  loopCharacteristics = undefined;
} else {

  // existing loop characteristics is simply thrown away 🤡 
  loopCharacteristics = self._moddle.create(entry.options.loopCharacteristics);

  if (entry.options.isSequential) {
    loopCharacteristics.isSequential = entry.options.isSequential;
  }
}
self._modeling.updateProperties(element, { loopCharacteristics: loopCharacteristics });
```

See https://github.com/bpmn-io/bpmn-js/blob/v8.9.0/lib/features/popup-menu/ReplaceMenuProvider.js#L434.