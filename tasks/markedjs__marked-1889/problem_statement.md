Lines with only spaces are removed, even in code blocks
**Describe the bug**

Spaces are removed from lines with *only* spaces. Though this might make some kind of sense for normal markdown, in code blocks it could be a problem in some esoteric programming languages such as whitespace but, perhaps more importantly, in real-time editing situations which is how it effects my use case.

**To Reproduce**

- [Marked Demo](https://marked.js.org/demo/?outputType=lexer&text=%60%60%60%0AThis%0A%20%20%20%20%20%20%0ATest%0A%20%20.%0A%60%60%60&options=%7B%0A%20%22baseUrl%22%3A%20null%2C%0A%20%22breaks%22%3A%20false%2C%0A%20%22gfm%22%3A%20true%2C%0A%20%22headerIds%22%3A%20true%2C%0A%20%22headerPrefix%22%3A%20%22%22%2C%0A%20%22highlight%22%3A%20null%2C%0A%20%22langPrefix%22%3A%20%22language-%22%2C%0A%20%22mangle%22%3A%20true%2C%0A%20%22pedantic%22%3A%20false%2C%0A%20%22sanitize%22%3A%20false%2C%0A%20%22sanitizer%22%3A%20null%2C%0A%20%22silent%22%3A%20false%2C%0A%20%22smartLists%22%3A%20false%2C%0A%20%22smartypants%22%3A%20false%2C%0A%20%22tokenizer%22%3A%20null%2C%0A%20%22walkTokens%22%3A%20null%2C%0A%20%22xhtml%22%3A%20false%0A%7D&version=master)  (Issue)
  ![image](https://user-images.githubusercontent.com/1341861/102939920-2b1f3b80-447d-11eb-85aa-bb56649cd0e8.png)

- [CommonMark Demo](https://spec.commonmark.org/dingus/?text=%60%60%60%0AThis%0A%20%20%20%20%20%20%20%0Atest%0A%20%20.%0A%60%60%60)  (Works as anticipated)

This caught me off guard because when I tried to fix it by extending the marked tokenizer, I found that the spaces were removed even there!

```js
[
  {type:"code", raw:"```\nThis\n\nTest\n  .\n```", lang:"", text:"This\n\nTest\n  ."}
  //                           ^^^
]
```

The problem is the first line of the lexer `blockTokens` function:
https://github.com/markedjs/marked/blob/c8783a3c1087c5a899ea6c1b96eb8a8e89fcd739/src/Lexer.js#L123

In my project I was forced to override the whole `blockTokens` function removing the first line. What would be the repercussions of removing it in general? Alternatively this could be an option..

Thanks for the great library!
