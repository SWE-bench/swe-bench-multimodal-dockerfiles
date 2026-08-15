Signup: Blog signup flow shows a flash of account screen at the end of the flow


#### Steps to reproduce
1. Starting logged out at URL: https://wordpress.com/
2. Click "Get started" to start the signup flow.
3. Enter the details for your new account.
4. When prompted for your site type, choose "Blog."
5. Finish the signup flow, choosing a site topic, address, and plan.

#### What I expected

After choosing the free plan, I expect to finish signup and be taken to a logged-in screen.
After choosing a paid plan, I expect to finish signup and be taken to checkout.

#### What happened instead

After choosing a plan, I see an account details screen with this notice:

> Your account has already been created. You can change your email, username, and password later.

The flow then automatically progresses to the next screen (the logged in checklist view for the free plan, or to checkout if I selected a paid plan).

#### Browser / OS version

Chrome 75.0.3770.100 / macOS 10.14.5

#### Screenshot / Video

![calypso-signup-account-blog](https://user-images.githubusercontent.com/8658164/60508757-07d65e80-9cd4-11e9-86a9-ebc26768983f.png)


#### Context / Source
#manual-testing






cc @Automattic/start-dev 
