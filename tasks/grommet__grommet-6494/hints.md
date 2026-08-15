Hi @jcfilben,
I checked this and found there is a default user agent style adding the extra margin to the Range Input Component.
As mentioned below.

<img width="694" alt="RangeInputIssuePNG" src="https://user-images.githubusercontent.com/36879900/201529105-99e90e78-875b-4159-9c6b-e03bfa6e30c6.PNG">

It can be removed and set a default margin to `0px` or `unset`. 
Then it will fix the issue

<img width="503" alt="RangeInputSol" src="https://user-images.githubusercontent.com/36879900/201529230-b8b8bf6a-4a30-41d0-b280-23362c2924a5.PNG">

Output:
<img width="276" alt="RangeInputSol1" src="https://user-images.githubusercontent.com/36879900/201534603-b3b3fd61-d2b4-40ba-9084-b55e1b8ce798.PNG">


Thanks,
Umesh

Hi @umeshiscreative thanks for looking into this! Would you be willing to file a PR to add 
 `margin: 0px` to StyledRangeInput?
@jcfilben Sure, I will raise a PR for this.