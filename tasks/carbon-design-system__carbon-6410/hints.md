CC @carbon-design-system/design 
We were noticing this is how Youtube handles their responsive tabs (the horizontal overflow like you discussed)
![scrolltabs1](https://user-images.githubusercontent.com/10426703/70357236-0806f700-183c-11ea-8579-dcadd17bc227.gif)

I think this works fairly well for our normal tabs in Cloud. However, we're trying to combine that interaction with a higher level of navigation (on-page left-nav) that also needs to collapse, which we were also responding into a dropdown. Is the dropdown model always inaccessible, or just for horizontal tabs?
@tessarodes the problem we were running into when going from tabs to the dropdown is that under the hood these are two distinct pieces of functionality that screen readers use, namely [`tabs`](https://www.w3.org/TR/wai-aria-practices/#tabpanel) and [`listbox`](https://www.w3.org/TR/wai-aria-practices/#Listbox), with different interaction models.

For tabs, we might see something announced like:

![demo](https://user-images.githubusercontent.com/3901764/70393786-a10c4e00-19b3-11ea-97f8-8f447b58eac1.gif)

For listbox (dropdown), this would look like:

![demo](https://user-images.githubusercontent.com/3901764/70393804-de70db80-19b3-11ea-98b1-788cde4686c5.gif)

---

Looking between the two, the tabs example clearly associates the content area with the tab where-as the dropdown will only inform the user of an option selected which seems like a potentially inoperable experience as the user may not know how to navigate to the part of the page that they are changing.
Related: https://github.com/carbon-design-system/carbon/issues/2551
The left/right arrows really help this interaction too. The scrolling tabs without any indicators could easily be over looked (like on google) but this youtube example seems a lot better. Plus it give you a click target if you're not on a touch screen and can't easily swipe. 

_Proposal Triage Meeting, January 21st 2020_

**Next Steps**

- [x] Need a design for scrolling tabs (inspired by YouTube above)
- Figure out dev impact of removal
  - Does it mess up designs
  - How could we introduce it safely
# Designs for responsive tabs
Status: **Ready for dev** 🤖 
Sketch file: https://ibm.box.com/s/polgkcgh8ypvi1pkttmieubulzja9jqj

## Interactions
- one click of the scroll arrow jumps/scrolls to have the next full tab show. 
- click and hold should jump to the start/end of the tab group.

## Default tabs
![Tabs - default](https://user-images.githubusercontent.com/11670886/73285906-5ee5d880-41bc-11ea-8025-a5b98c549140.png)

### In content / grid alignment 
![image](https://user-images.githubusercontent.com/11670886/73286206-cc920480-41bc-11ea-86f2-0032b28bc68d.png)
![image](https://user-images.githubusercontent.com/11670886/73286240-d61b6c80-41bc-11ea-9005-b3f30401687d.png)
![image](https://user-images.githubusercontent.com/11670886/73286323-fd723980-41bc-11ea-9633-92069597ca21.png)

## Container tabs

![Tabs - container](https://user-images.githubusercontent.com/11670886/73285904-5ee5d880-41bc-11ea-93b2-960093672eaf.png)

### In content / grid alignment 
![image](https://user-images.githubusercontent.com/11670886/73286527-4de99700-41bd-11ea-9a47-a83493882f90.png)
![image](https://user-images.githubusercontent.com/11670886/73286546-55a93b80-41bd-11ea-8b77-16252c608a0b.png)


@aagonzales is this supposed to show at a specific window size, or is it always available?
Always available, basically whenever overflow would happen. 
@aagonzales What are the Keyboard Interactions for this new design?

Some things to think about:
- do the scroll arrows take focus? (It looks as though they do in the picture?)
  - if they do, then is a keyboard user expected to type left/right arrow keys to move through the Tabs, then switch to typing space or enter when they get to the arrow button, then switch back to arrow keys to move into newly-shown Tabs? (I think that would be odd...?)
  - the keyboard interaction might feel more natural if the scroll arrows don't take focus (and if they are hidden from screen readers, i.e. use div/span with aria-hidden="true" and no role) so that users only need to use arrow keys to traverse the Tabs. I don't know for sure - just trying to think it through. 😄

- does the Tab content (i.e. tabpanel) automatically switch as the user types arrow keys to move through the Tabs? Or does the user need to type space or enter to "activate" a Tab? (or does the Tabs control handle both, and the author can choose?)

- does the `tab` key take the user directly to the currently-selected Tab's content? (probably should, because if there's going to be the possibility of many Tabs, it would be a chore for a keyboard user to have to type the `tab` key so many times to get past all of those Tabs. :)

- do the Home and End keys do the same as click and hold, i.e. jump to the start/end of the tab group?

- how about PageUp and PageDown - might be nice to have those jump to every... 10th(?) Tab, particularly if there are many tabs.

- does the Delete key delete the current Tab (if it's delete-able) ?
@carmacleod As I'm not a keyboard navigation expert I will gladly defer to your decisions on the topic. 
... but I am not a designer, so for new patterns I can only make suggestions and hope that someone from design will be able to think it through and take over. 😄 

(by "new", I mean the scroll arrows. A regular [Tabs control already has keyboard guidance](https://w3c.github.io/aria-practices/#keyboard-interaction-20).)
## Keyboard navigation:

- `tab`: traps focuses in the tab component starting at the select tab. 
   - press `tab` again and focus will move out of the tab component and not the next tab inside the component.
   - clicking `tab` at any point while inside tab component will move focus to the next focusable item on page. 
- `left arrow` and `right arrow`: navigates through the component tabs.
   - focus remains on the tab component and rotates through tab order continuously. 
   - Tab panel content does not change with `arrow` navigation  
- `enter` selects and open that tabs panel's content. 
- Scrolling arrow buttons will be excluded from screen reader and keyboard arrow selections.
- `esc` moves focus off the tab component and onto the next focusable item on page.
- `home` key takes the user to the first tab. 
- `end` key takes the user to the last tab.

### Visual aids
I made a visual to help my visual brain:

![image](https://user-images.githubusercontent.com/11670886/75391482-c53f4300-58af-11ea-90d0-9a937739a60b.png)


![image](https://user-images.githubusercontent.com/11670886/75392119-008e4180-58b1-11ea-9b3e-27241e8223e7.png)


Hi @aagonzales - that looks great!

I would only suggest a couple of changes:
- `enter` selects and open that tabs panel's content.
  - `space` or `enter`
- `esc` moves focus off the tab component and onto the next focusable item on page.
  - I would just delete this one. Users would just use the `tab` key to move the focus.
The `esc` key is usually used for "closing things", like a dialog, menu, or popup/dropdown list. :)

Thanks so much for doing this!
Any ETA on release for this update? Would like to plan ahead to prepare for any updates I need to do in my code.
Hey @gptt916! 👋 No immediate updates plan, we will try and share any changes to this in our monthly planning issues that we pin in the issues tab 👀 
just want to confirm: this [spec](https://github.com/carbon-design-system/carbon/issues/4758#issuecomment-579347916) is finalized to replace dropdown tabs and is ready for dev?
Yes, it its good to go @emyarod 