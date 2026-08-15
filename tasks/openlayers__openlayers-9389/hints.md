Reopening for the two tasks that were not completed in #9333. Here is a copy of the open questions from there:

@KaiVolland:
> STATUS
> 
> I transfomed the majority of the tests but now im stuck with some tests for different reasons:
> 
> * clip.test.js tile.test.js (render listener)
>   I couldn't manage to transform these tests as they rely on OL events/listeners which don't work as aspected for me in the test environment.
> * vectorimage.test.js (test with TextStyle)
>   Al tests with TextStyle are hard to compare with current setup as the CI seems to have different fonts installed which leads to high pixel mismatch numbers. Found a workaround for the TextStyle tests themselves but nut for the declutter tests in the vectorimage.test.js
> * ReprojImage
>   Every current test of the new test approach is based on a rendered map. But the ReprojIamge tests don't. I didn't dove to deep into these so i might miss the simple solution.
> Nevertheless i could need some help / hints for the last missing tests.
@KaiVolland Thanks for your work!

For the TextStyle issues, locally providing and using a web font could be a solution. For the event/listener issues you mentioned, I'd need more detail (maybe a WIP branch that shows the problems?). For the reprojection tests, it should be possible to test those in the context of a complete map setup instead. Would also be easier to help if you have a WIP branch that shows where you're stuck.
I created a WIP-PR for the TextStyle and added a local font #9362. Even if the font is the same it appears differently on the CI then on my machine.

Another WIP-PR to demonstrate my issues/confusion with listeners: #9364 
Last missing tests are the reproj tests. I opened another WIP-PR #9375.
As there is no API-Doc nor example for the Reproj classes im struggling to transform the test.

BTW: I'm wondering why there is no options object used for the constructors, as it is very hard to call a constructor function with 6 / 11(!) parameters in the right order. Reading the code is even harder.
@KaiVolland The reproj code is only used internally, and the reason why no constructor options are used are historical - with Google Closure Compiler, creating options objects was a very annoying procedure. I'd recommend a good JavaScript IDE like VS Code, which will always give you hints on the required arguments as you type. 