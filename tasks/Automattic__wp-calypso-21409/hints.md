Here's what I was thinking for a flow:

We keep the confirmation email notice: 
<img width="760" alt="1" src="https://user-images.githubusercontent.com/5835847/34175111-84026984-e4b8-11e7-9afe-44894711c344.png">

If they ignored the previous one, we display it again at the long loading screen, hopefully encouraging them to confirm while they wait for allthemagic to happen: 
<img width="760" alt="2" src="https://user-images.githubusercontent.com/5835847/34175112-8419377c-e4b8-11e7-8b60-5e08183f194e.png">

If they ignored that one too, we display it at the address step, which now includes the currency input (which I think we should prefill based on country)
<img width="760" alt="3" src="https://user-images.githubusercontent.com/5835847/34175114-84380616-e4b8-11e7-8376-77af6117d561.png">

If they ignore this too, we allow them to press "Let's Go!" but then give them a red global notice that says they must confirm before continuing. They can then press the "Let's Go!" button again to move forward once they've confirmed.
<img width="760" alt="4" src="https://user-images.githubusercontent.com/5835847/34175115-844ddc8e-e4b8-11e7-8e05-88ee6070ccc8.png">

cc: @allendav 
Thanks @kellychoffman - i like it. So does the "Let's Go!" button act as a "retry" in this scenario? I.E. if I go and verify my email address, then come back to the page, hitting Let's Go will attempt to confirm the verification? If the verification still fails, do we just keep stacking up the notices?
That is what I was thinking. And is consistent with other error notices. Maybe if we add another one, the one above it can fade out? Might be overkill to have 12 notices all in a row. 
How about a tweak - instead of the entire address form... what if we prompt the merchant just for their store's country and then... if they select US or CA... the component updates to show the rest of the form.

Or, if they select nonUS nonCA, once they verify their email, clicking Let's Go! sends them to wp-admin WooCommerce wizard step one ("Store Setup") - so we don't have to duplicate the currency and what-are-you-selling prompts (and any other prompts that might get added there) - they can enter their complete address then and answer those other questions and then continue with the wizard.

Whatcha think?

edit: If they pick nonUS nonCA we could surface a little copy that explains that we're going to send them to the WooCommerce wizard on their site to complete their setup and manage their store, and that we will let them know when they can manage their store from WordPress.com directly.
Noodled around with this and I have a question: Can we pre-fill the wp-admin step with the address? If so, I think we should keep the full address step in Calypso and fork it from there, meaning that all non supported calypso countries get the first step of the wp-admin wizard, with the address info already filled out. This way anything that core decides to add to this step in the future will not be effected by our work; that info will have to be filled out by the user. 
@kellychoffman - yes, I think we can prefill the wizard - it draws on the usual options - the same ones we can set via the REST API - we would just need to 1) wait for them to hit the button, 2) call the API to push the values to the site, 3) redirect to the site’s wp-admin to pick things up from there
@kellychoffman - just to be 100% clear - we want a full width warning [Notice](https://wpcalypso.wordpress.com/devdocs/design/notice) until they attempt to proceed past "Let's Go" and then we want to swap that out with a [GlobalNotice](https://wpcalypso.wordpress.com/devdocs/design/global-notices) error notice?
Yep!
While finishing up the Notice and GlobalNotice implementation, I noticed we have an [EmailVerificationGate](https://github.com/Automattic/wp-calypso/search?utf8=%E2%9C%93&q=EmailVerificationGate&type=) component designed to wrap things that we want to disable until the user completes email verification. This is used presently to protect things like 1) adding google apps, 2) registering additional domains, 3) inviting people to your site, and 4) approving Jetpack Connect.

If we did it on the set-your-store-address step, it would look like this

<img width="1431" alt="screen shot 2018-01-03 at 3 13 48 pm" src="https://user-images.githubusercontent.com/1595739/34544144-5d752684-f099-11e7-9b7b-3a44fc41c6af.png">

It includes a resend button which is nice.

Alternatively, we also have a [VerifyEmailDialog](https://github.com/Automattic/wp-calypso/search?utf8=%E2%9C%93&q=VerifyEmailDialog&type=) component. It is used by the post editor and gravatar editor.  It would look like this:

<img width="1437" alt="screen shot 2018-01-03 at 3 22 07 pm" src="https://user-images.githubusercontent.com/1595739/34544225-035a3ecc-f09a-11e7-8af1-6d14e3990ae9.png">

Lastly, we also have a [EmailVerificationNotice](https://github.com/Automattic/wp-calypso/search?utf8=%E2%9C%93&q=EmailVerificationNotice&type=) but we don't seem to use it anywhere anymore.

Before we move forward with the Notice/GlobalNotice design here, it seems we should consider using the gate or dialog approach used elsewhere in calypso - cc @kellychoffman @jameskoster 
  
Great finds Allen! I like `EmailVerificationGate` between the two myself... perhaps just because when given the option of using a dialog or not, i always opt for no dialogs, but will defer to Jay and Kelly for the final call.
+1 for dialog. 
@kellychoffman - OK, just to be super clear then, I'm going to:

* Add an is-warning `Notice` on the 'Building Your Store...' view saying `You need to confirm your email address to activate your account. We've sent an email to foo@bar.com with instructions for you to follow.`
* On displaying the 'Howdy! Ready to Start Selling (Set Your Store's Address)' view, if the email address has not yet been confirmed, immediately display the `VerifyEmailDialog` on top of it
  
> On displaying the 'Howdy! Ready to Start Selling (Set Your Store's Address)' view, if the email address has not yet been confirmed, immediately display the VerifyEmailDialog on top of it

Could we display that only when they press the "Let's go" button? So it acts as an in-your-face error message if they've ignored all the other ones up til then? 