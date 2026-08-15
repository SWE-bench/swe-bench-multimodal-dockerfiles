Found a dodgy character in the generated JSON coming from the source website.
Removing this fixed it.

Perhaps some more resilience could be added around this / an error explaining.

Thanks for the report and finding the root cause @amk221! 
Can you give us the test URL or identify what character broke the JSON?

Thanks!
```json
{
 "dodgy-char": "  " 
}
```
For those also confused by GitHub's rendering the dodgy character is U+2028 LINE SEPARATOR
http://www.fileformat.info/info/unicode/char/2028/index.htm

Thanks for digging this back up @amk221 !