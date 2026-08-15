[BUG] The fenced code block that follows the list is strange.
**Marked version:**
4.0.16

**Describe the bug**
The fenced code block that follows the list is strange.
If code block contains blankline, it is not judged as code block.

**To Reproduce**

![repro1](https://user-images.githubusercontent.com/80378/169825319-7f786584-0be3-4694-8962-530731a28ad0.png)

[Marked Demo permalink](https://marked.js.org/demo/?outputType=html&text=-%20abc%0A%60%60%60ruby%0Aa%0A%0Ab%0A%60%60%60%0A&options=%7B%0A%20%22baseUrl%22%3A%20null%2C%0A%20%22breaks%22%3A%20false%2C%0A%20%22extensions%22%3A%20null%2C%0A%20%22gfm%22%3A%20true%2C%0A%20%22headerIds%22%3A%20true%2C%0A%20%22headerPrefix%22%3A%20%22%22%2C%0A%20%22highlight%22%3A%20null%2C%0A%20%22langPrefix%22%3A%20%22language-%22%2C%0A%20%22mangle%22%3A%20true%2C%0A%20%22pedantic%22%3A%20false%2C%0A%20%22sanitize%22%3A%20false%2C%0A%20%22sanitizer%22%3A%20null%2C%0A%20%22silent%22%3A%20false%2C%0A%20%22smartLists%22%3A%20false%2C%0A%20%22smartypants%22%3A%20false%2C%0A%20%22tokenizer%22%3A%20null%2C%0A%20%22walkTokens%22%3A%20null%2C%0A%20%22xhtml%22%3A%20false%0A%7D&version=4.0.16)

[CommonMark Dingus permalink](https://spec.commonmark.org/dingus/?text=-%20abc%0A%60%60%60ruby%0Aa%0A%0Ab%0A%60%60%60%0A)

----

**If there is no blankline, no problem.**

[Marked Demo permalink](https://marked.js.org/demo/?outputType=html&text=-%20abc%0A%60%60%60ruby%0Aa%0Ab%0A%60%60%60%0A&options=%7B%0A%20%22baseUrl%22%3A%20null%2C%0A%20%22breaks%22%3A%20false%2C%0A%20%22extensions%22%3A%20null%2C%0A%20%22gfm%22%3A%20true%2C%0A%20%22headerIds%22%3A%20true%2C%0A%20%22headerPrefix%22%3A%20%22%22%2C%0A%20%22highlight%22%3A%20null%2C%0A%20%22langPrefix%22%3A%20%22language-%22%2C%0A%20%22mangle%22%3A%20true%2C%0A%20%22pedantic%22%3A%20false%2C%0A%20%22sanitize%22%3A%20false%2C%0A%20%22sanitizer%22%3A%20null%2C%0A%20%22silent%22%3A%20false%2C%0A%20%22smartLists%22%3A%20false%2C%0A%20%22smartypants%22%3A%20false%2C%0A%20%22tokenizer%22%3A%20null%2C%0A%20%22walkTokens%22%3A%20null%2C%0A%20%22xhtml%22%3A%20false%0A%7D&version=4.0.16)

**Expected behavior**
Fences that follow the list should ignore blank lines.
I want the following HTML output.

```html
<ul>
<li>abc<pre><code class="language-ruby">a

b
</code></pre>
</li>
</ul>
```

