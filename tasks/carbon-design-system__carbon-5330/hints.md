Related: https://github.com/carbon-design-system/carbon/issues/4665

@dakahn does an item with `role="search"` need an `aria-label` as well? Or does `Search` need to take in an `aria-label`

I'm not getting any DAP issues, @clarebyrne what errors are you seeing?
@clarebyrne can you tell us a little about what you're trying to achieve or accomplish here and why? Right now the table toolbar search element has the label "Filter Table" seen here:
![2020-02-07 16_43_36-Storybook](https://user-images.githubusercontent.com/40970507/74071279-2074c880-49c9-11ea-8c16-a2ac6889b7aa.png)

Thanks @dakahn, i'm trying to put an aria-label within the **role="search"** div, not the **role="searchbox"** div. But aria-label or aria-labelledby aren't defined in div section of the component.

<img width="1323" alt="Screenshot 2020-02-10 at 16 06 11" src="https://user-images.githubusercontent.com/59689747/74167011-7b076200-4c1f-11ea-8428-fc83dc86db46.png">

This is the accessibility rule I was given:
https://aat.w3ibm.mybluemix.net/token/a80a8d09-7f5a-480a-adcc-7e22f77482b0/c19cc7e4-e2e6-4475-89d7-533c2bc34979/archives/2019NovDeploy//doc/w3/help/en-US/idhi_accessibility_check_g1097.html
i'm not currently seeing a DAP error for our table toolbar -- who is reporting this error? 
I can only reproduce the DAP error only when there are at least two search bars with the same role=search tag, on the same page.
<img width="1358" alt="Screenshot 2020-02-11 at 10 09 44" src="https://user-images.githubusercontent.com/59689747/74227807-244d6700-4cb7-11ea-8d6e-8884d01eac76.png">

<img width="1526" alt="Screenshot 2020-02-11 at 12 52 23" src="https://user-images.githubusercontent.com/59689747/74238320-78634600-4ccd-11ea-9732-2b9bd578c950.png">
@dakahn I'm getting the DAP warning on this page too: https://www.carbondesignsystem.com/components/search/code/