There are two approaches to fixing this:

1. Fix the icon fill for the offending pseudo classes
`.bx--search-input:-internal-autofill-selected ~ .bx--search-close { fill: currentColor; }`

2. Ensure that the background color of the clear button is no longer transparent.

I used the first option as a quick fix in our project, but I'm thinking now that I prefer the second option as a longer term fix because it doesn't involve going down the road of learning / overwriting strange browser-specific pseudo classes.


HI @SimonFinney Thanks for bringing this to our attention! What browser are you finding this in and would you be able to provide a code sandbox reproducing this problem? At first glance, this issue seems to come from your implementation of the Search component.  The icons in our Search component are black by default and pass color contrast with the new `skyblue` autofill color. ![Screen Shot 2019-12-12 at 11.18.43 AM.png](https://images.zenhubusercontent.com/57a65257e40e5714b16d08ab/e79cdf43-482b-4ae1-8101-17408a1bcb1f)
Closing this since a solution is posted above! Re-open if anyone feels like the problem still needs to be addressed 👍 
@abbeyhrt I believe this will be affected in darker themes, like gray 100, where the icon defaults to white. Unfortunately, I don't have the permissions to reopen this issue but it still exists.
Can confirm that this issue exists on Chrome 78, OSX. We should reopen this issue.
@SimonFinney thanks for pointing that out! Reopening for further investigation 