Support Contact Form: breaks when no primary site exists
#### Steps to reproduce
1. Starting at URL: wordpress.com/me/account
2. set a primary site to a free, test site that you don't mind deleting
3. go into site settings and delete it
4. now you have a site with no primary site and no site selected
5. Click the help button in wordpress.com/me
6. Click contact us

#### What I expected
Something to happen - like an error (better but not ideal) or a site picker (since the issue is that we don't have site selected yet to load the form with).


#### What happened instead
Nothing, but a slew of console errors:
```
help.1f7980126b15040106c3.min.js:5 Uncaught TypeError: Cannot read property 'ID' of null
    at t.value (help.1f7980126b15040106c3.min.js:5)
    at d._renderValidatedComponentWithoutOwnerOrContext (vendor.5147b04b7f0d25caa892.min.js:18)
    at d._renderValidatedComponent (vendor.5147b04b7f0d25caa892.min.js:18)
    at d.performInitialMount (vendor.5147b04b7f0d25caa892.min.js:17)
    at d.mountComponent (vendor.5147b04b7f0d25caa892.min.js:17)
    at Object.mountComponent (vendor.5147b04b7f0d25caa892.min.js:19)
    at d.performInitialMount (vendor.5147b04b7f0d25caa892.min.js:17)
    at d.mountComponent (vendor.5147b04b7f0d25caa892.min.js:17)
    at Object.mountComponent (vendor.5147b04b7f0d25caa892.min.js:19)
    at d.performInitialMount (vendor.5147b04b7f0d25caa892.min.js:17)
```

#### Browser / OS version
Chrome

#### Screenshot / Video
This is what the user experienced in their console:
![screen shot 2017-10-24 at 3 42 15 pm](https://user-images.githubusercontent.com/8921630/31966870-f74a7ab8-b8c0-11e7-9410-2dff77f72719.png)

This is what it looked like in their browser:
![screen shot 2017-10-24 at 3 25 25 pm](https://user-images.githubusercontent.com/8921630/31966937-2731b908-b8c1-11e7-9781-d2aa943e30d1.png)


#### Context / Source
#user-reported this over email - they have paid sites like http://ncch.org/ on their account so should have smooth access to our contact form
