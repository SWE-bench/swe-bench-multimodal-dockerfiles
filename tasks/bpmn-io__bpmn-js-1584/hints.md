I have noticed that my library version is outdated, however the bug is still present in the newest version (8.3.1)
Hi,

Thank you for reporting this. I was able to reproduce the issue. Indeed, it seems unreasonable that we re-generate the Process id. I suspect that the bug may have something to do with the [CreateParticipantBehavior](https://github.com/bpmn-io/bpmn-js/blob/develop/lib/features/modeling/behavior/CreateParticipantBehavior.js).

We will happily accept a pull request with a fix. If you want to implement that, I will support you if you get stuck.
Hi,

Thank you for the reply and confirmation. Unfortunately, I am still quite a javascript newbie, and even more so a newbie to the bpmn-js library, so I am worried that I would do more harm than good by trying to fix it (I have taken a look around the file and I am not quite sure what might be causing the behaviour, unfortunately). If this issue will still be open in the future when I gradually gain more insight, I might gladly give it a go :). 
That's OK :) Reporting a valid issue is already a great contribution.
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