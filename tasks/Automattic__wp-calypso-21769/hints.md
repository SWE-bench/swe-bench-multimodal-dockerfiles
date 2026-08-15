I dug into this a little bit. On a surface level, it's happening because we check for `ID` without checking that `selectedSite` exists here:

https://github.com/Automattic/wp-calypso/blob/master/client/me/help/help-contact-form/index.jsx#L321

A simple fix would be to add in a check and pass in `null` if the primary site is empty at the moment. But, you would get a broken-ish form if you pass in `null` for selected site on the sites dropdown initially.

<img width="563" alt="screen shot 2017-10-25 at 10 02 39 am" src="https://user-images.githubusercontent.com/7240478/32009209-a78ebcfe-b96b-11e7-9cfe-a3a2ef05731f.png">

Seems like a better approach overall would be to update the primary site setting on the account when the primary site is deleted. That way, we avoid problems like this without having to put individual fixes in place.
I was helping @sanjeev00733 accessing the form today for the same reason. Not sure what triggered his error, but we've found a workaround: 

* go to "my sites".
* choose one site (not the "all sites" option).
* visit the contact form.


Some more info from the debugging session: something like this has happened [before](https://github.com/Automattic/wp-calypso/issues/15819), and we've got it [fixed](https://github.com/Automattic/wp-calypso/pull/15845). As per [this request](https://github.com/Automattic/wp-calypso/issues/15915), the `selectedSite` logic was [reorganized](https://github.com/Automattic/wp-calypso/pull/15013). cc @unDemian @mattwondra 
I was getting this issue and was able to make it work with the help of @nosolosw 
I will add some information in case it helps.

I was getting this error in Firefox and Chrome on Mac OS Seira 10.2.
Irrespective of browser and OS I think the issue is I didn't have a site selected and so I had to 

- Switch to a site  
- click on help icon at the bottom on the left sidebar to get to the contact form.

As an user, it would have helped if the page said "You need to select a site first, please select a site you need help with" instead of **Loading contact form message**