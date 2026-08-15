Gutenberg: Modal to try new Editor
Initial version implemented in #26816.

Follow-up tasks:

- [ ] remember dismissal in userprefs & default dialog to visible on load
- [ ] redirect to wp-admin for Jetpack/AT sites (TBD)
- [x] add click tracking events to both buttons in dialog
- [x] make sidebar image clickable?

Original issue:

Let's create a modal that will display on the /post and /page editor when the `gutenberg` feature flag is enabled. Clicking on  "Use the Classic Editor" Will dismiss the modal, while clicking on the primary button will redirect to `/gutenberg/{post-type}` or the wp-admin Gutenberg editor. Let's add a relevant click event for each action.

Copy is not final and may be subject to change. Please ping @shaunandrews  if we need assets.

![screen shot 2018-08-09 at 3 13 05 pm](https://user-images.githubusercontent.com/1270189/43928725-c822bd22-9be6-11e8-8d9d-1cf85bc78168.png)

Clicking on Learn More should display the modal again:

![screen shot 2018-08-09 at 3 38 53 pm](https://user-images.githubusercontent.com/1270189/43929554-6151eb64-9bea-11e8-87fd-71a910e68295.png)


Bonus Design Question: Should we add an option to not show this modal again for a while?

