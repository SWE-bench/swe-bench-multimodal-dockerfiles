Happiness Support card needs preventWidows treatment


Following from #33040 

#### Steps to reproduce
1. Starting at URL: `plans/my-plan`
2. Notice the widows when looking at the "Priority support" card (try resizing your browser)

#### What I expected

"your account." should be on the same line

#### What happened instead

"account." was on its own (see screenshot)

#### Screenshot

![widow](https://user-images.githubusercontent.com/177929/58649318-b49f7380-8303-11e9-8f78-6a8dead59f41.png)

#### Note

I tried to apply `preventWidows()` to `this.getSupportText()` (L171 client/components/happiness-support/index.jsx) but this doesn't seem to work because of the `<strong />` component.
