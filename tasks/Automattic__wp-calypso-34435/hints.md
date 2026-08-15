I can reproduce the bug even when logging in:

![Jul-03-2019 10-46-10](https://user-images.githubusercontent.com/6458278/60556494-f4cf9700-9d84-11e9-81f0-7a99d46f8b37.gif)

I think it was introduced here: 

https://github.com/Automattic/wp-calypso/pull/34356/files#diff-515b9f6b5e27cdcebb984cf5d42edd35L191

@andrewserong 

Did some ugly hacking around, ~but checking for the existence of `lastKnownFlow` seems to fix it, but it doesn't get to the core of what's going on~. (Doesn't fix it. See: https://github.com/Automattic/wp-calypso/issues/34403#issuecomment-507902190) 

```
			if ( step.lastKnownFlow ) {
				return includes( flow.steps, step.stepName ) && step.lastKnownFlow === flowName
			}
			return includes( flow.steps, step.stepName );
```

Any ideas?

_edit_: At the domains steps, after having selected a blog site, I noticed that the last known flow flips to `onboarding`. It doesn't happen all the time though.

```
console.log( flowName, step.lastKnownFlow ) // -> onboarding-blog, onboarding
```
> At the domains steps, after having selected a blog site, I noticed that the last known flow flips to onboarding. It doesn't happen all the time though.

Ah, it's only when you sign/log in for the first time. It's [filtering the flow steps](https://github.com/Automattic/wp-calypso/blob/master/client/signup/utils.js#L202) in `getCompletedSteps()` and checking the last known flow, but because we only fork at site type, the user step's last known flow is still `onboarding`

<img width="1014" alt="Screen Shot 2019-07-03 at 11 25 57 am" src="https://user-images.githubusercontent.com/6458278/60556604-85a67280-9d85-11e9-8244-7e783054b0d9.png">



Maybe we can tell the filtered steps method that we're performing a resume? https://github.com/Automattic/wp-calypso/pull/34426/files
Thanks for reporting this @rachelmcr, much appreciated! — we've deployed a fix to revert the change that caused this issue. I'll work on a more permanent fix this afternoon, so will leave this issue open until it's resolved.