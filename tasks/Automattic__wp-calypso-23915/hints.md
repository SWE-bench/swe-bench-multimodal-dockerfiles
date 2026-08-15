Thank you for the report! I tried testing using the steps provided just now and was unable to reproduce the problem. I tested while logged in as a regular user and an Automattic user. I tested starting from a list (as in your example) in the Reader. I tested using Firefox 59.0.1 and Chrome 65.0.3325.162 on macOS 10.13.3.

Video: [29s](https://cloudup.com/cURlDDmQwdp)

Could this have been a temporary glitch or possibly something related to the staging server? Would you mind checking to see if the problem is still happening for you, and if it is could you check to see if there are any errors showing in the browser console at the time you click the "Edit" link?
I tested again and was unable to reproduce. @gravityrail is this problem still happening for you? Do you think I need to adjust my testing steps? I noticed the list you are testing is named "amptest"—is there a way I can test the same type of content you are testing? Do I need to do anything special to test AMP content in the Reader?
I noticed that the URL for that Edit link in your video is this format: `https://wordpress.com/edit/{SITE_ADDRESS}/{POST_ID}`

However, it should be `https://wordpress.com/post/{SITE_ADDRESS}/{POST_ID}` (with `post` instead of `edit` in the URL).

I reproduced the issue by trying to edit a post I authored on a Jetpack site I own, clicking the Edit link on the post from my main Followed Sites feed. It looks like this is a bug with Jetpack sites in the Reader rather than something specific to Reader lists.