Alt text with escaped characters breaks image links
I'm not sure if this is a bug or not, but I would love any suggestions on how to resolve if possible.

I have a situation where image links are not rendering as I would expect because the Alt text part of the image contains escaped square bracket characters.

For example:

```md
[![\[Manny Pacquiao\]](https://img.youtube.com/vi/s6bCmZmy9aQ/0.jpg)](https://youtu.be/s6bCmZmy9aQ)
```

This results in the following:

![image](https://user-images.githubusercontent.com/10571313/82298114-bd52f300-9a07-11ea-805b-854f69d2ecb0.png)

[Here](https://marked.js.org/demo/?text=%23%20Expected%20result%0A%0A%5B!%5BManny%20Pacquiao%5D(https%3A%2F%2Fimg.youtube.com%2Fvi%2Fs6bCmZmy9aQ%2F0.jpg%20%22manny%22)%5D(https%3A%2F%2Fyoutu.be%2Fs6bCmZmy9aQ)%0A%0A%23%20Actual%20result%0A%0A%5B!%5B%5C%5BManny%20Pacquiao%5C%5D%5D(https%3A%2F%2Fimg.youtube.com%2Fvi%2Fs6bCmZmy9aQ%2F0.jpg%20%22manny%22)%5D(https%3A%2F%2Fyoutu.be%2Fs6bCmZmy9aQ)%0A%0A%0A&options=%7B%0A%20%22baseUrl%22%3A%20null%2C%0A%20%22breaks%22%3A%20true%2C%0A%20%22gfm%22%3A%20true%2C%0A%20%22headerIds%22%3A%20true%2C%0A%20%22headerPrefix%22%3A%20%22%22%2C%0A%20%22highlight%22%3A%20null%2C%0A%20%22langPrefix%22%3A%20%22language-%22%2C%0A%20%22mangle%22%3A%20true%2C%0A%20%22pedantic%22%3A%20false%2C%0A%20%22sanitize%22%3A%20false%2C%0A%20%22sanitizer%22%3A%20null%2C%0A%20%22silent%22%3A%20false%2C%0A%20%22smartLists%22%3A%20false%2C%0A%20%22smartypants%22%3A%20false%2C%0A%20%22tokenizer%22%3A%20null%2C%0A%20%22walkTokens%22%3A%20null%2C%0A%20%22xhtml%22%3A%20false%0A%7D&version=master) is the demo page with examples.

I don't mind creating a pull request, but I'd love any pointers as to where this problem lies.
