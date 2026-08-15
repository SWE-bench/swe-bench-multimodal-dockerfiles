Task lists are rendered even when GFM is disabled
**Marked version:**

1.2.3

**Describe the bug**

Even when `gfm: false`, task lists are rendered.

**To Reproduce**

Steps to reproduce the behavior:

1. Setup options with `gfm: false`.
2. Render the following:

```
Unordered:

- [ ] A
- [ ] B
- [ ] C

Ordered:

1. [ ] A
2. [ ] B
3. [ ] C

A | B
--|--
1 | 2
3 | 4
5 | 6
```

3. Confirm that the table is *not* rendered, but the **task list is rendered**:

![image](https://user-images.githubusercontent.com/613788/99151858-00ff8000-266c-11eb-942f-f9596eb92482.png)

Here's some demos:

- [Marked demo showing incorrect behavior](https://marked.js.org/demo/?text=Unordered%3A%0A%0A-%20%5B%20%5D%20A%0A-%20%5B%20%5D%20B%0A-%20%5B%20%5D%20C%0A%0AOrdered%3A%0A%0A1.%20%5B%20%5D%20A%0A2.%20%5B%20%5D%20B%0A3.%20%5B%20%5D%20C%0A%0AA%20%7C%20B%0A--%7C--%0A1%20%7C%202%0A3%20%7C%204%0A5%20%7C%206&options=%7B%0A%20%22baseUrl%22%3A%20null%2C%0A%20%22breaks%22%3A%20false%2C%0A%20%22gfm%22%3A%20false%2C%0A%20%22headerIds%22%3A%20true%2C%0A%20%22headerPrefix%22%3A%20%22%22%2C%0A%20%22highlight%22%3A%20null%2C%0A%20%22langPrefix%22%3A%20%22language-%22%2C%0A%20%22mangle%22%3A%20true%2C%0A%20%22pedantic%22%3A%20false%2C%0A%20%22sanitize%22%3A%20false%2C%0A%20%22sanitizer%22%3A%20null%2C%0A%20%22silent%22%3A%20false%2C%0A%20%22smartLists%22%3A%20false%2C%0A%20%22smartypants%22%3A%20false%2C%0A%20%22tokenizer%22%3A%20null%2C%0A%20%22walkTokens%22%3A%20null%2C%0A%20%22xhtml%22%3A%20false%0A%7D&version=1.2.3)
- [CommonMark demo showing expected behavior](https://spec.commonmark.org/dingus/?text=Unordered%3A%0A%0A-%20%5B%20%5D%20A%0A-%20%5B%20%5D%20B%0A-%20%5B%20%5D%20C%0A%0AOrdered%3A%0A%0A1.%20%5B%20%5D%20A%0A2.%20%5B%20%5D%20B%0A3.%20%5B%20%5D%20C%0A%0AA%20%7C%20B%0A--%7C--%0A1%20%7C%202%0A3%20%7C%204%0A5%20%7C%206)

**Expected behavior**

Task lists are [only an extension of GFM](https://github.github.com/gfm/#task-list-items-extension-), so I would expect the output to match CommonMark by using the `[ ]` as part of the rendered text:

![image](https://user-images.githubusercontent.com/613788/99151912-618ebd00-266c-11eb-9c5c-331921f3c2ef.png)

Task lists are rendered even when GFM is disabled
**Marked version:**

1.2.3

**Describe the bug**

Even when `gfm: false`, task lists are rendered.

**To Reproduce**

Steps to reproduce the behavior:

1. Setup options with `gfm: false`.
2. Render the following:

```
Unordered:

- [ ] A
- [ ] B
- [ ] C

Ordered:

1. [ ] A
2. [ ] B
3. [ ] C

A | B
--|--
1 | 2
3 | 4
5 | 6
```

3. Confirm that the table is *not* rendered, but the **task list is rendered**:

![image](https://user-images.githubusercontent.com/613788/99151858-00ff8000-266c-11eb-942f-f9596eb92482.png)

Here's some demos:

- [Marked demo showing incorrect behavior](https://marked.js.org/demo/?text=Unordered%3A%0A%0A-%20%5B%20%5D%20A%0A-%20%5B%20%5D%20B%0A-%20%5B%20%5D%20C%0A%0AOrdered%3A%0A%0A1.%20%5B%20%5D%20A%0A2.%20%5B%20%5D%20B%0A3.%20%5B%20%5D%20C%0A%0AA%20%7C%20B%0A--%7C--%0A1%20%7C%202%0A3%20%7C%204%0A5%20%7C%206&options=%7B%0A%20%22baseUrl%22%3A%20null%2C%0A%20%22breaks%22%3A%20false%2C%0A%20%22gfm%22%3A%20false%2C%0A%20%22headerIds%22%3A%20true%2C%0A%20%22headerPrefix%22%3A%20%22%22%2C%0A%20%22highlight%22%3A%20null%2C%0A%20%22langPrefix%22%3A%20%22language-%22%2C%0A%20%22mangle%22%3A%20true%2C%0A%20%22pedantic%22%3A%20false%2C%0A%20%22sanitize%22%3A%20false%2C%0A%20%22sanitizer%22%3A%20null%2C%0A%20%22silent%22%3A%20false%2C%0A%20%22smartLists%22%3A%20false%2C%0A%20%22smartypants%22%3A%20false%2C%0A%20%22tokenizer%22%3A%20null%2C%0A%20%22walkTokens%22%3A%20null%2C%0A%20%22xhtml%22%3A%20false%0A%7D&version=1.2.3)
- [CommonMark demo showing expected behavior](https://spec.commonmark.org/dingus/?text=Unordered%3A%0A%0A-%20%5B%20%5D%20A%0A-%20%5B%20%5D%20B%0A-%20%5B%20%5D%20C%0A%0AOrdered%3A%0A%0A1.%20%5B%20%5D%20A%0A2.%20%5B%20%5D%20B%0A3.%20%5B%20%5D%20C%0A%0AA%20%7C%20B%0A--%7C--%0A1%20%7C%202%0A3%20%7C%204%0A5%20%7C%206)

**Expected behavior**

Task lists are [only an extension of GFM](https://github.github.com/gfm/#task-list-items-extension-), so I would expect the output to match CommonMark by using the `[ ]` as part of the rendered text:

![image](https://user-images.githubusercontent.com/613788/99151912-618ebd00-266c-11eb-9c5c-331921f3c2ef.png)

