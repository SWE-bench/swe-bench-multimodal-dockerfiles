_Confirmed the overall issue._  

PHP has no real awareness of anonymous functions. (though it may work if you use `{`, etc...  I wonder if we just shouldn't add `endsParent` to the `=>` rule?

> The comments are colored orange because they are considered title.

I wonder if this should not be dealt with as a separate fix (still part of this issue).  IE, fix comments THEN fix the function detection.


> >    The comments are colored orange because they are considered title.
> 
> I wonder if this should not be dealt with as a separate fix (still part of this issue). IE, fix comments THEN fix the function detection.

I meant to say that the comments don't get recognized correctly because of the arrow-function.
The comments look correct if I remove the first line of the example:

![Comments without arrow-function](https://user-images.githubusercontent.com/2564094/107474168-bab0a480-6b26-11eb-8090-cf1ae2bc02af.png)
Yes, I understand, but line comments are technically possible anywhere (I'd assume), even in the middle of a function definition... just because the scope changes doesn't mean everything should be a title - comments should still be recognized as comments.  To me this is a separate bug/issue.
 ```diff
{
  className: 'function',
  relevance: 0,
  beginKeywords: 'fn function', end: /[;{]/, excludeEnd: true,
  illegal: '[$%\\[]',
  contains: [
    hljs.UNDERSCORE_TITLE_MODE,
    {
      begin: '=>', // No markup, just a relevance booster
+    endsParent: true,
    },
    {
      className: 'params',
      begin: '\\(', end: '\\)',
      excludeBegin: true,
      excludeEnd: true,
      keywords: KEYWORDS,
      contains: [
        'self',
        VARIABLE,
        hljs.C_BLOCK_COMMENT_MODE,
        STRING,
        NUMBER
      ]
    }
  ]
}
```

The above code does solve the problem and all the existing test also pass. 
![image](https://user-images.githubusercontent.com/4337699/107857760-87d41c80-6e56-11eb-9830-7d437bb16d6d.png)

Shall I create a pull request?

@il3ven Can you check if it also fixes this edge case:
```php
$fn2 = function ($x) use ($y) {
    return $x + $y;
};
```
`use` is supposed to be a keyword here.
See https://www.php.net/manual/en/functions.arrow.php
@Hirse If not I think only this would need to be added, no?  To add the `use` keyword in the function scope.

```js
keywords: 'fn function use'
```
![image](https://user-images.githubusercontent.com/4337699/107859629-ac34f680-6e60-11eb-8d8c-57c57ddb2907.png)

It is correct. Right?
Oh, title will match it... so you'd just need a special case rule inside `contains` to explicitly handle `use` and mark it as a keyword... I'm assuming use is not a valid function name.

Perhaps:

```
 contains: [
   { beginKeywords: "use" },
   hljs.UNDERSCORE_TITLE_MODE,
```
> Oh, title will match it... so you'd just need a special case rule inside contains to explicitly handle use and mark it as a keyword... I'm assuming use is not a valid function name.

This does it.

![image](https://user-images.githubusercontent.com/4337699/107859758-a55ab380-6e61-11eb-8601-84c5071eaabf.png)
