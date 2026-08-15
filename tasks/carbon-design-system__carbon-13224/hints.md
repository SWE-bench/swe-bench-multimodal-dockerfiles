@kaylarakower is the button beside the menu also a part of the component? What the relationship of the button and menu? How is this different than an [overflow menu](https://www.carbondesignsystem.com/components/overflow-menu/code) or a [dropdown](https://www.carbondesignsystem.com/components/dropdown/code)? 
![image](https://user-images.githubusercontent.com/11670886/59860926-76ff9a80-9345-11e9-8075-c118fc1932ae.png)


Or is the component the whole piece? What do the pieces on the far left do?
![image](https://user-images.githubusercontent.com/11670886/59861209-fb521d80-9345-11e9-8b10-09bf93239764.png)

![spec](https://user-images.githubusercontent.com/48567372/62240595-50516c80-b3a5-11e9-9f42-fd41f4a95b51.jpg)

Sketch file: https://ibm.box.com/s/txyppivhxkx1cptc2lhfyr8afysujimy
## ✅ Experimental status approved 
Moving forward this component will go into `experimental` to start with. I have approved @kaylarakower latest designs. Her developers will be building and contributing this component.
Update: My team will not be able to contribute the development of this feature, @aagonzales please add to dev backlog
Hey 👋 - this doesn't change anything you have here I believe, but I do recommend as some related reading.

I've begun a deep dive into the conceptual approaches to a combo/split and menu buttons etc for my team, including research into existing approaches by other products etc as well as some Nielsen looks into the topic.

Resulting in a recommendation, and beginnings of a pattern:
https://ibm.invisionapp.com/share/9YNZT26NFRW#/319466322_Introduction
After some more recent activity on this topic from a few others across different teams, I figure it may also be valuable to share a link to an extract of the IoT PAL sketch library that houses the symbols that came out of my exploration of competitors & best practice linked in my comment above.

Note, this link is shared under 'people in your company' so will require an IBM login to view.
https://ibm.box.com/s/f4qn7rdlweutdtiwdfjh4m48rptwgv98
@lukefirth That's awesome! Thanks for always keeping us in the loop on the progress of your work! 
Hi 👋 

We're starting to build out some specs and guidance for two different type of buttons, [menu buttons and split buttons](https://pages.github.ibm.com/ai-applications/design/components/buttons/usage), that stems from what Luke initially shared. 

Would love to work with the Carbon team to get this in as a contribution as several other teams seem to have similar needs for it as well!
If you haven't already done so, please be sure to think about keyboard interaction and focus styles.

I think the focus style for the menu button should be the same as the Carbon Primary Button focus style.
Probably the split button should be the same or similar.

For the menu button, drop down the menu on space, enter or down arrow. Then up/down arrows move through the menu items.

For the split button, I'm not exactly sure what the usual keyboard interaction is, but I am guessing that space or enter would activate the main action, and down arrow would drop down the menu?

Do you have focus/keyboard design done yet? Thanks!
Our team has something similar to your menu button. Ours is a hacked up combination of overflow menu and primary button. It works "ok", but it does not have focus styling consistent with other Carbon primary buttons. Yours looks good so far! Our team could definitely use something like your menu button! (Of course, we would want to keep our plus sign icon. :) )
![image](https://user-images.githubusercontent.com/3331913/97933129-de05cf80-1d3f-11eb-89ea-be7e070c5c5d.png)

Also I'd like to make sure that you consider the ARIA markup needed to make a menu button accessible to screen reader users. Here's the ["Menu Button" pattern in the APG](https://w3c.github.io/aria-practices/#menubutton). Please read through the "Keyboard Interaction" section and the "WAI-ARIA Roles, States, and Properties" section in the Pattern description. There are 3 examples - I think your menu button would be closest to the [2nd example](https://w3c.github.io/aria-practices/examples/menu-button/menu-button-actions.html) (although I am not a fan of opening the menu on hover!). Note that the Pattern description is more important than the examples, because each example just shows one way to implement the pattern, but there are certainly other valid ways to do it.
@carmacleod is there a chance your work around is documented online? We have a similar need and wanted a work around as we wait for this to be added to carbon. Can u please kindly respond to this discussion https://github.com/carbon-design-system/carbon/discussions/9905 