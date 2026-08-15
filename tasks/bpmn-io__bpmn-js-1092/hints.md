I was indeed able to create a centric connection between two tasks (but not in any case):

![Jun-18-2019 11-26-47](https://user-images.githubusercontent.com/9433996/59670372-227ce380-91bc-11e9-9312-34da4f49d2f7.gif)

However, it makes sense to have it this per default, since as the screencast reveals, it does not snap on center in the first place.

Furthermore, there seems to be a bug with the connection adjustment when moving the centered connected tasks:

![Jun-18-2019 11-27-33](https://user-images.githubusercontent.com/9433996/59670520-607a0780-91bc-11e9-8f45-aca35afeec14.gif)

This might come from the same problem described here (and might be fixed with #1079), but I'll create another issue for this.

@pinussilvestrus Please use the provided example diagram, too. It contains a not-yet-snapped process, the thing that is common, as diagrams are not generally snapped yet.
Thanks for the hint! Yes, in this case, it is not possible to connect them center to center in any case.
After a further discussion we will try out following way: When connecting Element -> Task

* Snap to target center if the cursor is in `center` of target
* Snap to grid position if otherwise (as it is right now) 

![taskSnapping](https://user-images.githubusercontent.com/9433996/59683010-a2647700-91d7-11e9-832f-74ade9fe18ae.png)
