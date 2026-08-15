Thanks for the detailed explanation, I can reproduce this 👍 Moving this to backlog
# Root Cause Analysis 🔍 

This was assumed to have been fixed (cf. https://github.com/bpmn-io/bpmn-js/issues/1617). However, the fix only works if you don't move the label, so effectively, it's still broken.

Here's what's happening:

* during move the hovered element is 🐒 patched to be the root element when moving a label (cf. https://github.com/bpmn-io/bpmn-js/blob/v9.3.2/lib/features/modeling/behavior/FixHoverBehavior.js#L45) so the label always ends up becoming a child of the root element
* when collapsing the sub process the label stays visible as it's not a child of the sub process diagram shape (cf. https://github.com/bpmn-io/diagram-js/blob/v8.8.0/lib/features/modeling/cmd/ToggleShapeCollapseHandler.js#L31)

However, not 🐒 patching still doesn't fix the issue since the parent will still end up being the root element (cf. https://github.com/bpmn-io/bpmn-js/blob/v9.3.2/lib/features/ordering/BpmnOrderingProvider.js#L134). So we're basically trying to fix the parent of the label in 2️⃣ places. 🤡 

I see two possible approaches:

### 1. Labels are always children of the parents of their label target
  * this would require us to _not_ 🐒 patch the hovered element anymore and to default to the label targets parent when computing the order 

### 2. Move labels to appropriate root element when collapsing a shape
  * this would require us to add a behavior
I will go for the second approach as it is less intrusive.