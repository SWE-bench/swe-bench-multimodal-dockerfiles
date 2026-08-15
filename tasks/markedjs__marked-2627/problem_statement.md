Broken "Strong" transform
**Marked version:** 4.0.1

**Describe the bug**
if inside bold text from the right border there is an escaped square open bracket and there is a closing brace behind "**", then bold text is not recognized

**To Reproduce**

1. [Marked Demo](https://marked.js.org/demo/?outputType=html&text=**strong%20text%5C%5B**%5C%5D&options=%7B%0A%20%22baseUrl%22%3A%20null%2C%0A%20%22breaks%22%3A%20true%2C%0A%20%22extensions%22%3A%20null%2C%0A%20%22gfm%22%3A%20true%2C%0A%20%22headerIds%22%3A%20false%2C%0A%20%22headerPrefix%22%3A%20%22%22%2C%0A%20%22highlight%22%3A%20null%2C%0A%20%22langPrefix%22%3A%20%22language-%22%2C%0A%20%22mangle%22%3A%20false%2C%0A%20%22pedantic%22%3A%20false%2C%0A%20%22sanitize%22%3A%20true%2C%0A%20%22sanitizer%22%3A%20null%2C%0A%20%22silent%22%3A%20false%2C%0A%20%22smartLists%22%3A%20true%2C%0A%20%22smartypants%22%3A%20true%2C%0A%20%22tokenizer%22%3A%20null%2C%0A%20%22walkTokens%22%3A%20null%2C%0A%20%22xhtml%22%3A%20true%0A%7D&version=4.0.1)
2. [CommonMark Demo](https://spec.commonmark.org/dingus/?text=**strong%20text%5C%5B**%5C%5D)

**Expected behavior**
![image](https://user-images.githubusercontent.com/8930952/141372010-ef8bf7de-dff7-4c55-94f7-18357e69acf4.png)

