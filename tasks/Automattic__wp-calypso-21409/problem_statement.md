Store: Signup Flow needs to require email verification
Background p90Yrv-sE-p2

In order to allow for countries that are not supported by Store on wpcom to flow properly through the signup -> AT site/wp-admin, new user's email addresses must be verified for their WPCOM session to be valid to auth against their `wp-admin`.

There is one notice shown during the signup flow that prompts the user to verify their email address, but it does not prevent them from proceeding prior to doing so:

![notice-verify](https://user-images.githubusercontent.com/22080/34058152-cf2dccfa-e18e-11e7-99f6-8a6f1f7a2dc4.png)

__Current Thinking__
The idea right now is to create a new verification step after the user completes the Address Page form:

![address-page](https://user-images.githubusercontent.com/22080/34058228-0f78b5f4-e18f-11e7-8133-e57bceea7374.png)

Based on the user input here, we will have a fork in the flow:

_Supported Countries ( US, CA )_
If the store address entered is a supported country, the next step will be the current flow - showing the dashboard setup checklist.

_Non-Supported Countries_
These users will need to have a verified email address before proceeding/being directed to the WC setup page in `wp-admin`. Looks like we should be able to leverage [`isCurrentUserEmailVerified`](https://github.com/Automattic/wp-calypso/blob/master/client/state/current-user/selectors.js#L157) to quickly sniff this out - but we might have to do some polling, or add a button for the user to say "Yes I have verified my email".

Maybe we could even use that cool fake browser frame to show them what the email subject line looks like @allendav!

TODO: Need a design for this portion of the signup flow.
