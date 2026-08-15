Checkout: American Express credit card numbers aren't formatted correctly during checkout
#### Steps to reproduce
1. Starting at URL: https://wordpress.com/checkout/example.wordpress.com/personal
2. Try to purchase a Personal plan on a your site
3. In the checkout form, add an Amex number (instead of Visa or Mastercard)
4. Note the expected format is visually incorrect, leading to confusion for customers trying to verify their card number before submitting it

#### What I expected
To see American Express card number format respected: `1234 123456 12345`.

#### What happened instead
It looks like we only format in groups of 4 for all card types, so an Amex number ends up displaying in the form field like this: `1234 1234 5612 345`

#### Screenshot / Video
<img width="768" alt="screen shot 2018-01-29 at 08 24 04" src="https://user-images.githubusercontent.com/66797/35518737-9d088bb6-04cf-11e8-9334-74b20dd2b6d7.png">

#### Context / Source
Source: @m #flowsharing  via a friend of his in #reallife 

