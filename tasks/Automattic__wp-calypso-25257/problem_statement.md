Products cannot be added to Store if category contains an "&".


#### Steps to reproduce
1. Starting at URL: https://wordpress.com/store/
2. Click "add" to create a product: https://wordpress.com/store/products/
3. Enter a title, price, etc.
4. For the category, either select one that's already made that has an "&" in it (via WP-Admin for example), or create a new one. Example: "Hats & Visors".
5. If this is the first product, it sometimes will successfully publish the product.
6. For any subsequent product in that category, or if the category already existed, error "There was a problem saving" "Please try again" will display.

#### What I expected
To successfully save & publish a new product.

#### What happened instead
Error  "There was a problem saving" "Please try again" displayed.

#### Browser / OS version
Firefox 59.0.3 / Windows 10

#### Screenshot / Video

![screenshot-2018-4-30 new product est 1999 wordpress com](https://user-images.githubusercontent.com/10121835/39454068-c9affc3c-4c9e-11e8-9141-eef8b77d2dc8.png)

#### Context / Source


3251489-hc

Products created via WP-Admin are unaffected by the issue.



