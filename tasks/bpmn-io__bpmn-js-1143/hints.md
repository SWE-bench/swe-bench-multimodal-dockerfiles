Could you provide us with your logs, starting from the first error?
On my machine (Arch Linux, your Chrome version) I cannot reproduce the issue given the steps you procided:

![capture 79d5GQ_optimized](https://user-images.githubusercontent.com/58601/61867350-47f5bf00-aed7-11e9-87db-d80fe5c9a459.gif)

Sure! This is what I get from the brwoser console:
Topmost errors in trace:
![error_1](https://user-images.githubusercontent.com/51420727/61867609-e7b34d00-aed7-11e9-829f-31bc7d4c7e93.PNG)

Next Error: 
![error_2](https://user-images.githubusercontent.com/51420727/61867629-ee41c480-aed7-11e9-98d0-a809549ada11.PNG)

After this, the exactly same three errors are thrown multiple times. 
I am able to reproduce this every time I do the steps describe above..

I did some more testing: the error occurs _only_ if you add a pool !
Thanks for the additional clarification. I can reproduce it now. We will have a look. :+1: 
Root-Cause: In [`CreateParticipantBehavior`](https://github.com/bpmn-io/bpmn-js/blob/develop/lib/features/modeling/behavior/CreateParticipantBehavior.js#L51) the childrenBBox has malformed (NaN) height and width properties, because `bpmn:Group` elements are ignored. If no other elements are there, of course, no children are still available to create the correct participant bounds.

I'll have a look at this next week 🎸