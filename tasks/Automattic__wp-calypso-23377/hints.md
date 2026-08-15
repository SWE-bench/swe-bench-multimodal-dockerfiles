See also notes and history in https://github.com/Automattic/wp-calypso/issues/4795
Tangentially-related: https://github.com/Automattic/wp-calypso/issues/8911
Flow note shared with me by @catehstn today:

> Deleting a post I'm writing, like abandoning a draft I don't want to save, deletes the post — then tells me I can restore it to keep editing. Weird. I expect it to close the editor.
What are your thoughts on showing a success message and undo button instead of the current Deleted Post modal? 
Yes, "Restore" being the primary action button with blue shade causes major confusion in my opinion too. 

Two other readings from my end. 

1. Clicking on **Esc** button or clicking anywhere outside the popup box does not help discard this popup box either.
2. This popup box appears only when trashing a post from the post editor screen. Trashing a post using the menu options the https://wordpress.com/posts screen does not show this - trashes the post immediately.

#painpoints #manual-testing 
@Automattic/tanooki will look into this.
I wouldn't call this a bug because the restore dialog is working as originally intended.  However it has come up several times that the design/flow needs improvement.

Previously discussed a bit at https://github.com/Automattic/wp-calypso/pull/18785, it sounds like we want to do this now:

> 1. Don't show the restore dialog at all.

This is the confirmation dialog that appears when trashing the currently-edited post.  It should indicate that the user will be redirected to the posts list if the post is trashed:

> <img src="https://user-images.githubusercontent.com/227022/36705456-d6d9df7c-1b2a-11e8-8b88-fc411d98cd4f.png" width="300">

Upon clicking "Move to trash", the user should be returned to the posts list.  Clicking "Don't restore" currently does this, but it may make more sense to go directly to the "Trashed" section of the posts list instead.

Then, a notice should appear when the post is successfully moved to the trash.  Here is the existing notice when a post is trashed from the posts list.  We could also add an action to restore the post there:

> ![2018-02-26t19 28 42-0600](https://user-images.githubusercontent.com/227022/36705571-86f9a9c8-1b2b-11e8-9352-e30a5ed64978.png)

We should also be sure to remove all code related to the existing "Don't Restore / Restore" dialog.