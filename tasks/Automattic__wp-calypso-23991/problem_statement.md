Editor: Adding and removing Featured image mark new post as dirty


#### Steps to reproduce
1. Starting at URL: https://wordpress.com/post
2. Set Featured Image 
3. Remove it
4. Press back button (on Calypso navbar)

#### What I expected
Redirect back without AYS ("Are You Sure?" dialog)

#### What happened instead
I got AYS dialog, though there nothing to save in post.

#### Browser / OS version
Chrome 60 / Mac OS Sierra

#### Screenshot / Video

![AYS dialog](https://user-images.githubusercontent.com/5654161/29975637-c3d4073a-8f3f-11e7-8108-400114d4adbf.gif)

#### Context / Source


That issue was discovered after PR review on [wp-e2e-tests/pull/694](https://github.com/Automattic/wp-e2e-tests/pull/694). The interesting part that this issue is reproducible only for new posts. When editing saved post - no AYS dialog would be shown. 

Should be related to #9833
