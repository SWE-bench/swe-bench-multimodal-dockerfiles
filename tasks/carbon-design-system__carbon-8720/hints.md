CC @carbon-design-system/design to see if there is an interest in the team. I thought we had some discussions around it, but completely slipped off my mind wrt where.
There is interest in this. We would need to take the component through a review process.
We've marked this issue as stale because there hasn't been any activity for a couple of weeks. If there's no further activity on this issue in the next three days then we'll close it. You can keep the conversation going with just a short comment. Thanks for your contributions.

Still necessary, it's just on the backburner for now
My team is interested in this component too. Meanwhile we came with a slightly different style.
https://ibm.invisionapp.com/share/GRNZ3Q843A2#/319182290_list

I would be happy to update to the thicker version presented above if this becomes the standard. I think it is worth checking is the text supporting the progress bar should be part of it or not or how to deal with text positioning for different contexts etc. It would be great if the color of the progress bar in the component wasn't locked to one color -  for example we need to differentiate between upload and processing phase.

Thank you,
Mariusz   


I need this type of component currently as well. For now Im using something very similar to the screenshot attached in this issue 
We can definitely prioritize this as one of the next components to build out. Meanwhile, we are short on resources so if anyone is willing to contribute design & code, we would really appreciate it! 


We've marked this issue as stale because there hasn't been any activity for a couple of weeks. If there's no further activity on this issue in the next three days then we'll close it. You can keep the conversation going with just a short comment. Thanks for your contributions.

KeepAliveBot
We've marked this issue as stale because there hasn't been any activity for a couple of weeks. If there's no further activity on this issue in the next three days then we'll close it. You can keep the conversation going with just a short comment. Thanks for your contributions.

not stale
We've marked this issue as stale because there hasn't been any activity for a couple of weeks. If there's no further activity on this issue in the next three days then we'll close it. You can keep the conversation going with just a short comment. Thanks for your contributions.

Hi all. Is there any progress on the progress bar component?
I am also interested in this progress bar component.  I would like to use it in a situation where something is happening in the background, and the user needs to know the status while continuing to work in the foreground. 
Since this is quite a common component and I think many teams (including ours) would need it, could this be a candidate to bring over from Cloud PAL and add to the external core library?
Hey, Any progress on this component? I am also interested in this progress bar component. Our product needs to use it for system updates. It usually takes a long time and will happen in the background, so it will be very helpful for them to come back and able to see the progress is moving forward and still working. Thanks! 
Extremely interested in this component. What's the status please?
[edit] 
I saw it's mentioned in projects. https://github.com/orgs/carbon-design-system/projects/8 
Good to see it being progressed! 
[/edit]
Just did some research on this, and it seems like there are two native HTML elements that could be used. See here for a working example: https://codesandbox.io/s/stoic-cloud-3t5fz?file=/src/index.js

A) `meter` which is defined by the w3c as 
> The meter element represents a scalar measurement within a known range, or a fractional value; for example disk usage, the relevance of a query result, or the fraction of a voting population to have selected a particular candidate. This is also known as a gauge.
[w3c docs](https://html.spec.whatwg.org/multipage/form-elements.html#the-meter-element)

or

B) `progress` which is defined by the w3c as 
> The progress element represents the completion progress of a task.
[w3c docs](https://html.spec.whatwg.org/multipage/form-elements.html#the-progress-element)

The biggest issue is `meter` is fully unsupported in IE11 (https://caniuse.com/meter)
However, `progress` is fully supported with the caveat that `indeterminate` is not supported in Safari (https://caniuse.com/progress)

There are some styling tweaks that could be made to each of these components to align with the Carbon standard
- [Meter](https://css-tricks.com/html5-meter-element/#styling-the-meter-element)
- [Progress](https://css-tricks.com/html5-progress-element/#styling-progress-bars)


@tw15egan It seems that only Safari on iOS 7 doesn't support the`indeterminate` variant, while Safari on macOS and iOS 8 and higher fully support it. That would make `progress` the better candidate imo, what do you think?

Is there design guidance on this? I could probably find some time to work on the implementation.
@janhassel I agree 👍🏻 

@carbon-design-system/design do we have any guidance for this?