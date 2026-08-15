Crash when rendering an empty checkbox list item
### Describe the bug
Rendering an empty checkbox list item leads to a crash:
> `Uncaught TypeError: Cannot read property 'type' of undefined`

### To Reproduce

[Click here to see the crash on Marked demo](https://marked.js.org/demo/?text=%20%20-%20%5B%20%5D%20checklist%20item%0A%0A%20%20-%20%5B%20%5D%20&options=%7B%0A%20%22baseUrl%22%3A%20null%2C%0A%20%22breaks%22%3A%20false%2C%0A%20%22gfm%22%3A%20true%2C%0A%20%22headerIds%22%3A%20true%2C%0A%20%22headerPrefix%22%3A%20%22%22%2C%0A%20%22highlight%22%3A%20null%2C%0A%20%22langPrefix%22%3A%20%22language-%22%2C%0A%20%22mangle%22%3A%20true%2C%0A%20%22pedantic%22%3A%20false%2C%0A%20%22sanitize%22%3A%20false%2C%0A%20%22sanitizer%22%3A%20null%2C%0A%20%22silent%22%3A%20false%2C%0A%20%22smartLists%22%3A%20false%2C%0A%20%22smartypants%22%3A%20false%2C%0A%20%22tokenizer%22%3A%20null%2C%0A%20%22xhtml%22%3A%20false%0A%7D&version=master)
![image](https://user-images.githubusercontent.com/1694410/81624131-6de74400-93c3-11ea-8eb7-ac3a1145afc4.png)

### Expected behavior
No crash and a correctly rendered checkbox.

