@Maledong Thanks for reporting this bug!

Here's a smaller repro steps:

```md
[One](https://example.com/1) ([Two](https://example.com/2)) [Three](https://example.com/3)
```

[marked demo](https://marked.js.org/demo/?text=%5BOne%5D(https%3A%2F%2Fexample.com%2F1)%20(%5BTwo%5D(https%3A%2F%2Fexample.com%2F2))%20%5BThree%5D(https%3A%2F%2Fexample.com%2F3)&options=%7B%0A%20%22baseUrl%22%3A%20null%2C%0A%20%22breaks%22%3A%20false%2C%0A%20%22gfm%22%3A%20true%2C%0A%20%22headerIds%22%3A%20true%2C%0A%20%22headerPrefix%22%3A%20%22%22%2C%0A%20%22highlight%22%3A%20null%2C%0A%20%22langPrefix%22%3A%20%22language-%22%2C%0A%20%22mangle%22%3A%20true%2C%0A%20%22pedantic%22%3A%20false%2C%0A%20%22sanitize%22%3A%20false%2C%0A%20%22sanitizer%22%3A%20null%2C%0A%20%22silent%22%3A%20false%2C%0A%20%22smartLists%22%3A%20false%2C%0A%20%22smartypants%22%3A%20false%2C%0A%20%22tables%22%3A%20true%2C%0A%20%22xhtml%22%3A%20false%0A%7D&version=0.6.1)

/cc @UziTech looks like a regression in 0.6.1 because it works fine in 0.6.0