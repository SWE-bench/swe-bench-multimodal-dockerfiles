Reader: failed comment loading produces a plague of error notices
When opening a Jetpack post for a site that has the JSON API turned off, the replies endpoint returns a 403 and this happens:

![image](https://user-images.githubusercontent.com/17325/40953053-23bd94ba-68d2-11e8-854c-eef25826e32f.png)

In this situation, we should limit the retries and preferably show the error message in the comments section rather than firing a ton of error notices. Even better, we could set comments to 'off' in the API response if the Jetpack JSON API is turned off for their site.
