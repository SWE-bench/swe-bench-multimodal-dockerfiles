Could that be related with the latest JPC refactors? cc @sirreal @seear @johnHackworth 
This one seems to be related: #19462
Nice testing @tyxla, you have a real talent for finding bugs like this 🙂 

## TL;DR
I believe this is an old issue in a flow that's not used often

## Here's the breakdown:

### 1

The Authorization at `/jetpack/connect/authorize` redirects at the end of the authorization step:

https://github.com/Automattic/wp-calypso/blob/7bf6dddec0ecdfa624cb54237f0d640b0581c830/client/jetpack-connect/auth-logged-in-form.jsx#L114-L115

### 2

This is a url of the form `/jetpack/connect/plans/:SITE_SLUG`, which is routed through `siteSelection` and `plansSelection` (which is never reached):

https://github.com/Automattic/wp-calypso/blob/7bf6dddec0ecdfa624cb54237f0d640b0581c830/client/jetpack-connect/index.js#L64-L70

The plans route is never reached, because at this point in the flow we'd expect the site to be in the site list, however for subscribers, that's not the case. `state.sites.items` does not include the newly connected site for a subscriber.

### 3

`siteSelection` attempts to find the site which matches the slug. This fails. The user is redirected to the path with the slug removed:

https://github.com/Automattic/wp-calypso/blob/7bf6dddec0ecdfa624cb54237f0d640b0581c830/client/my-sites/controller.js#L390-L394

### 4

We've now arrived at `/jetpack/connect/plans`. This _does not match_ the plans route `/jetpack/connect/plans/:site` (note the required `:site`), and instead matches the connect route `/jetpack/connect/:locale?`:

https://github.com/Automattic/wp-calypso/blob/e468e3c0fc37abbb1e7ee31d912fa13f029b995e/client/jetpack-connect/index.js#L58-L62

### 5

Congrats, you're a new connected subscriber… who was unceremoniously dropped onto the connect site url input page with a plans url 🤦‍♂️ 

----

## Moving forward

It's hard to say what would be a good fix for this. The fundamental cause is that the entire flow expects a site you connect to appear in your sites. 

It might make sense to look at a robust fix for this as part of [Jetpack Connect Services](https://github.com/orgs/Automattic/projects/8). I've added it to the project board.
Thanks for the thorough writeup @sirreal ❤️ 
I wanted to see if this had improved as we've worked on [Jetpack Connect Services](https://github.com/orgs/Automattic/projects/8).

At the moment, rather than returning to the site input page, a subscriber is returned to `/jetpack/connect/store`.