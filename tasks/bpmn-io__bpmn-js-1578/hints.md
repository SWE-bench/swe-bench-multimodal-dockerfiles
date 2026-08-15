I cannot reproduce this using 
https://demo.bpmn.io/new

See recording:
![duplicatePoolAndSave](https://user-images.githubusercontent.com/42800119/147917961-2604acc2-17b4-4af4-8080-a9016dacf20c.gif)

Can you please give more detailled steps to reproduce this?


> I cannot reproduce this using https://demo.bpmn.io/new
> 
> See recording: ![duplicatePoolAndSave](https://user-images.githubusercontent.com/42800119/147917961-2604acc2-17b4-4af4-8080-a9016dacf20c.gif)
> 
> Can you please give more detailled steps to reproduce this?

After export. You need import file was exported.
Ah got it - thanks. I can reproduce this. We will have a look.
**Root Cause**

When morphing the Process into a Collaboration, the ID get's unclaimed.
https://github.com/bpmn-io/bpmn-js/blob/fe11c2ee78000449ba20412c99be30be95bf776d/lib/features/modeling/behavior/UnclaimIdBehavior.js#L50

With https://github.com/camunda/camunda-modeler/issues/1410, we keep the IDs when copying Elements, so we create the process with the same ID again.

**Solution Sketch**
Determine if it makes sense to unclaim IDs when the root changes but nothing is deleted and either:
- Remove the code that unclaims the ID
- Ensure the ID is re-claimed once the new participant with a `processRef`is created