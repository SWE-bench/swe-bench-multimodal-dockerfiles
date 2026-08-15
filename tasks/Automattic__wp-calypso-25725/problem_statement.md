Plans: Allow changing owner of a plan
Currently, only an Administrator of a site (WordPress.com or Jetpack) can purchase a plan, and once they have purchased it, they are the owner and no one else can control that plan.

We should make it so that customers can transfer ownership of a purchased plan to any other Administrator on their site. 

I propose that on this view (under Me > Manage Purchases > Purchases), we make the Owner box clickable, and have it go into a simple flow for transferring ownership.

![purchases_ _manage_purchase_ _wordpress_com](https://user-images.githubusercontent.com/108942/38649487-26ec03f4-3db4-11e8-973c-8e16a078bcec.png)

We would _only_ make it clickable if there were other Administrators on this site. If there were, and you clicked, you'd be given a big warning about how once you transfer ownership you won't be able to cancel/manage the plan, and that your billing details will be transferred along with it, etc. You'd be shown a list of Administrators on the site, click one, and then we'd transfer ownership of the plan over to that person. Ideally we'd also send an email to both you and the new owner telling them what happened (and add an entry to the Activity Log as well).

cc @rralian in case this is a complete no-go in our billing system, although I believe we can/do currently have this functionality in our admin tools on the backend.
