Hi @diego-codes does your overflow menu in data table have `data-floating-menu-primary-focus` attribute?
Hi @asudoh, no. I searched the entire DOM for this attribute and nothing came up.
OK would you want to try adding that attribute to the focusable DOM node in the first menu item?
Adding the `data-floating-menu-primary-focus` attribute to the DOM node works! It appears that it is not applied to the menu in the `DataTable` by default then.
Related to #2481
We've marked this issue as stale because there hasn't been any activity for a couple of weeks. If there's no further activity on this issue in the next three days then we'll close it. You can keep the conversation going with just a short comment. Thanks for your contributions.

As there's been no activity since this issue was marked as stale, we are auto-closing it.
