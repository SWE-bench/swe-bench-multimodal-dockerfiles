@wkeese I can't recreate this on Windows in either Chrome or Firefox using our Storybook. Do you still see this error? 
Yes, I do. Just retested on Chrome on Windows 10.   Probably, you forgot to select some options in the dropdown first?  Try using TAB and SHIFT-TAB to go back and forth between the (2x) button and the `<input>`.

<img width="628" alt="Screen Shot 2021-01-16 at 13 42 16" src="https://user-images.githubusercontent.com/69599/104797356-c7c8c500-5800-11eb-85b5-956e9975b0dd.png">

Also, note that this is about the *filterable* multiselect.
@wkeese thanks I see it now, thanks for your patience. 

@carbon-design-system/design while it might look a little questionable I don't actually have a problem with this behavior from an accessibility stand point. The text input is receiving focus correctly. In fact an argument could be made that this behavior _helps_ magnification users better determine the actual input on the form as distinct from the button to clear the selections since visually we combine a listbox and a button here.
I agree you can debate which focus outline is better from an accessibility standpoint, but I think you need to pick one way or the other.  Right now tabbing into or clicking on the `<input>` puts the focus outline on the `<input>`:

<img width="344" alt="Screen Shot 2021-01-22 at 8 13 37" src="https://user-images.githubusercontent.com/69599/105424016-dc3a1100-5c89-11eb-8e33-2758774fcdc3.png">

But clicking on the upper left (when options are selected) puts the focus outline on the whole control:

<img width="341" alt="Screen Shot 2021-01-22 at 8 09 20" src="https://user-images.githubusercontent.com/69599/105423824-967d4880-5c89-11eb-8181-1bad4edc25b8.png">

The other (very related) issue is that there's actually an extra tab stop on the whole control: clicking on the upper left and then pressing the tab key goes to the (2 x) button, and then another tab goes to the `<input>`... i.e. there are 3 tab stops where there should be 2.

(Both these screenshots are from React on Chrome/mac but I assume it's a universal behavior.)

PPS: I would also question the slightly different background colors for the left side vs. the input.