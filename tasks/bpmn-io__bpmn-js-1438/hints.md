Related to https://github.com/bpmn-io/bpmn-js/issues/447
Hint: the message got rendered [at this place](https://github.com/bpmn-io/bpmn-js/blob/develop/lib/draw/BpmnRenderer.js#L1457).
Hi, Can i take this up ? 
Yes, feel free to open a PR and ask for help if you stuck 👍 
@pinussilvestrus Can you share some tips to navigate the folder structure of the repo? I'm trying to identify where I can narrow the issue down to 
I already gave a first hint of where to start: https://github.com/bpmn-io/bpmn-js/issues/777#issuecomment-697279882

Basically, the project is divided into features and core modules. Every module will then be put together inside the overall Modeler/Viewer class. This is a task of rendering, I guess a good start would be to look inside the `draw`, furthermore the BpmnRenderer.
Thanks a lot @pinussilvestrus  that helps
I have gone through the setup process here (https://github.com/bpmn-io/bpmn-js/blob/develop/.github/CONTRIBUTING.md) and have set up the repo successfully.

Where can i find the steps to build the code with my code changes and see it in action in a browser ? 
Thanks 
Executing `npm run dev` will execute test suites which also renders Modelers into the browser. What we mostly do is to make this [test case](https://github.com/bpmn-io/bpmn-js/blob/develop/test/spec/ModelerSpec.js#L48) unique and then run it to see a modeler and manually test new behavior.

```js
it.only('....')
```
Ahh I see.. So you use a test case to build everything and fire up the browser and once everything is loaded you manually test it.. 

But wouldn't running `npm run dev` run all the ~1500 test cases? 
Not if you use the `only` keyword

```js
it.only('should import simple process', function() {
    var xml = require('../fixtures/bpmn/simple.bpmn');
    return createModeler(xml).then(function(result) {

      expect(result.error).not.to.exist;

      result.modeler.get('editorActions').trigger('selectElements');
    });
});
```
Okay thank you . Let me try that 👍 
Okay everything is working now.. 
But how do I play around with the UI? everything happens so fast with the test cases. 

![ezgif com-gif-maker](https://user-images.githubusercontent.com/20852629/94674136-5cccae80-0335-11eb-99ad-a72efde4e872.gif)

Did you try to click on "Debug"?
@pinussilvestrus  Yeap!! It works now 😊
![Screenshot 2020-10-01 at 10 07 37 AM](https://user-images.githubusercontent.com/20852629/94768769-f0ea5480-03cd-11eb-9012-884ea8dbb762.png)

~I have the UI rendered and I'm trying to create a scenario as depicted in the issue. How do I add a message b/w two components?~

I used 
```js
it.only(...)
```  
[here](https://github.com/bpmn-io/bpmn-js/blob/develop/test/spec/features/modeling/behavior/ReplaceConnectionBehaviorSpec.js#L72) to generate the messages as shown 

![Screenshot 2020-10-01 at 10 52 24 AM](https://user-images.githubusercontent.com/20852629/94771160-34e05800-03d4-11eb-96b8-7db65a1d7c73.png)

For time being, I have hard-coded the attributes to display the message name here 

```js
semantic.messageRef = true
      semantic.name = "Hi there"
      if (semantic.messageRef) {
        var midPoint = path.getPointAtLength(path.getTotalLength() / 2);
        var markerPathData = pathMap.getScaledPath('MESSAGE_FLOW_MARKER', {
          abspos: {
            x: midPoint.x,
            y: midPoint.y
          }
        });

        var messageAttrs = { strokeWidth: 1 };

        if (di.messageVisibleKind === 'initiating') {
          messageAttrs.fill = 'white';
          messageAttrs.stroke = 'black';
        } else {
          messageAttrs.fill = '#888';
          messageAttrs.stroke = 'white';
        }

        drawPath(parentGfx, markerPathData, messageAttrs);
      }
```
@pinussilvestrus  

I noticed that setting the `semantic.name` attribute automatically renders a label as you can see in the attached image. 
1. How is that label getting rendered? 
2. Is that the correct label to be displayed as part of this issue? If yes where can i find the code to adjust its x and y coordinates? 
3. If No, should I be using the `renderEmbeddedLabel()` function to render the label
Short answer: Yes Message can have labels (= names) and it's part of this issue to render them. Inside the Renderer, you'll find a method to render external labels. The [LabelUtil](https://github.com/bpmn-io/bpmn-js/blob/2dd1e1330509d3f6db7939ad8ae22b75144396bd/lib/util/LabelUtil.js) has some interesting methods which generate information about labels related to different element types.

You also have to consider that messages also belong to message flows, which can also have a label. Two labels (one for the message and one for the flow) in that case might not be necessary.
Can you help me understand how the label is printed in the image i shared above just by setting the `semantic.name` property ? because I couldn't find a renderLabel function within `'bpmn:MessageFlow'` function 
What I find confusing is that the code already supports rendering message labels as long as it has attributes `messageRef`  and `name` . So that makes me ask , where do I need to add these attributes to the Messages?
> the code already supports rendering message labels

Can you post a screenshot that shows a message object with a label in the Modeler?
![Screenshot 2020-10-01 at 4 39 20 PM](https://user-images.githubusercontent.com/20852629/94802095-a932ef80-0404-11eb-9ff6-e1d79d75673b.png)

is this what you meant @pinussilvestrus 
Does this label come from a `bpmn:MessageFlow` or a `bpmn:Message` element? The task of this issue is to render labels from `bpmn:Message` elements.
This label comes from a `bpmn:MessageFlow` element 

by `bpmn:Message` are you referring to https://github.com/bpmn-io/bpmn-js/blob/2dd1e1330509d3f6db7939ad8ae22b75144396bd/lib/draw/BpmnRenderer.js#L560
No, I mean `bpmn:Message` elements. Please make sure you are familiar with the BPMN 2.0 specification and also checked out the example diagram in the issue description.
To give you kind of a hint. The message element is rendered in [the handler of the `bpmn:MessageFlow`](https://github.com/bpmn-io/bpmn-js/blob/2dd1e1330509d3f6db7939ad8ae22b75144396bd/lib/draw/BpmnRenderer.js#L1457). The issue here is that currently the label is only rendered if a `bpmn:MessageFlow` has a name, but the name of a referenced `bpmn:Message` element not got considered.

As you already figured out, the renderer might not be the only place you have to look at. Labels sometimes (and also in this case) got rendered as external label. You may have to find out where to get the information from, what should be rendered as the label for the message flow if a message element does exist. Cf. https://github.com/bpmn-io/bpmn-js/issues/777#issuecomment-701921977
Im referring this to get a better understanding of bpmn specs https://camunda.com/bpmn/reference/

![Screenshot 2020-10-01 at 5 09 49 PM](https://user-images.githubusercontent.com/20852629/94804810-121c6680-0409-11eb-92d6-34b37a2ab9cd.png)
Okay so if `bpmn:MessageFlow` does not have a name, I need to check if either of the `bpmn:Message` elements (highlighted in red in the image) that it connects, has a name ("Message1 in this case") and somehow pass that information to `bpmn:MessageFlow` so that it gets rendered [here](https://github.com/bpmn-io/bpmn-js/blob/2dd1e1330509d3f6db7939ad8ae22b75144396bd/lib/draw/BpmnRenderer.js#L1457)?  

Also if there are other channels we can connect it would be better 
@pinussilvestrus Can you let me know if my understanding is correct?
Looking to connected message elements is a good idea. The place you linked might not be the correct place, since labels are not rendered exactly there.

I gave you some hints where label information got handled. My proposal: try to create a first solution, create a PR and then let's discuss around it.