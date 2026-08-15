Note for when we fix this: Fix the i18n of `Error` for the metrics, and maybe pull the same string?
![image](https://user-images.githubusercontent.com/6392995/66617616-b4a16100-eb8a-11e9-9154-60c8a1460af9.png)

thicc bang
<img width="1280" alt="76" src="https://user-images.githubusercontent.com/406636/66769158-45b55800-ee69-11e9-9cdd-bedfa50c5f40.png">

Here is a zip for the error icons in svg: [ic_errors.zip](https://github.com/GoogleChrome/lighthouse/files/3725544/ic_errors.zip)

@yuinchien I'd like to work on this issue. Just to confirm, its simply to update all current error icons with new design in lighthouse performance report, Right? 
Not sure about second error with i18n error, but might just get started first.. 😄 
Thanks @rahulpatel596! Basically.

We want to replace the red triangle with the new red exclamation icon for all audits that *error*. 

Sidenote for Lighthouse team, what do you think about changing the text from "Error" to "Exception Thrown"? I feel like that might clear up most of the confusion around whether this is their failure or ours.
Hey @patrickhulce 
I am working on this and I just wanted to confirm that I am making changes in correct place because current production version has a quite different UI. 
Thanks for your help :)

<img width="1439" alt="Screen Shot 2020-11-07 at 9 26 12 PM" src="https://user-images.githubusercontent.com/33618437/98456215-7afda980-2140-11eb-8a2e-a228a3d69a32.png">

We *don't* want to replace the legend one, other than that yes those 3 places would have the exclamation instead of the question mark/triangle *and* the regular audits below this as well. Keep in mind that this exclamation design should only apply when there has been an error and the score is `null`.
Hey @patrickhulce Is there a specific method or way to follow which can generate report with an error and/or with null score?
Yes @rahulpatel596, every PR has a [sample error report deployed](https://lighthouse-638sz3brb.vercel.app/error/) and you can replicate it on your local machine with `yarn now-build`
Some good progress was made in https://github.com/GoogleChrome/lighthouse/pull/11670 but this is available again if anyone would like to pick it up.
I'm happy to work on this, but it seems there is already a PR (https://github.com/GoogleChrome/lighthouse/pull/9272) that handles updating the error icons.


@tannerdolby that PR is very old, you are welcome to submit your own :)
@adamraine sounds good, I will start working on this and submit a PR soon :)