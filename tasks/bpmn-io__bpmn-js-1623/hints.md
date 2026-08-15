Hi, thanks for creating this issue. 

I am not sure if it belongs to the examples repository. This looks more like an issue with the plugin or bpmn-js. Do you think this is a bug on our side or rather a problem within your plugin?

Hi @barmac! Well, I am sincerely not sure. When I change diagram on canvas I call `bpmnjs.open(#diagramId)`. I saw the deep linking example with the `canvas.setRootElement` function, but it doesn't work like that. Maybe it's a problem on my plugin 
_I should not use the `open` function but something else?_ or maybe _I should call something else after the `open`?_ 
That's why I'm here. Maybe I am missing something to do, to open the diagram correctly.
@marstamm I think we need your help here. 

Perhaps the missing overlay is a bug on our side. I am moving this issue to `bpmn-js` repo.
I'll take a look :eyes: 
I can confirm that his is a problem with our implementation:

https://github.com/bpmn-io/bpmn-js/blob/fb6c6495701e693e76c89d97cf05d96a0c7e5c35/lib/features/drilldown/DrilldownOverlayBehavior.js#L83

We add the initial overlays on `import.done`. However, this event is only fired when `viewer.importXML` is called and not for `viewer.open`. The fix is to listen to `import.render.complete` instead or fire `import.done` every time
OK so then we can confirm that this is a bug in bpmn-js. Thanks for looking into this @marstamm 
Hello @marstamm, thank you for your reply! So, if I am right, the first solution competes to bpmn-js, the second is on my plugin, right?
If you confirm that `import.render.complete` will be the solution, I'll wait for the next release :) thank you!
Hi @Ichigo85 ,

This is a bug in bpmn-js, so we should take care of firing the correct events in the core. I will fix it before the modeler stable release.

You could fire the `import.done` event yourself as a quick fix, but I do not recommend it. It could lead to unexpected side-effects if we decide to implement it in the core.