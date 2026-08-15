thanks for the issue, I was able to repro it!

Unfortunately, it looks like there wasn't enough interest from the team
or community to implement this change. While we wish we'd be able to
accommodate everyone's requests, we do need to prioritize. We've found
that accepted issues failing to be implemented after 90 days tend to
never be implemented, and as such, we [close those issues](https://eslint.org/docs/maintainer-guide/issues#when-to-close-an-issue).
This doesn't mean the idea isn't interesting or useful, just that it's
not something the team can commit to.

Thanks for contributing to ESLint and we appreciate your understanding.

[//]: # (auto-close)

reopen as it is happening in latest eslint and default parser: I've created a mini [demo](https://eslint.org/demo#eyJ0ZXh0IjoiLyplc2xpbnQgXCJrZXktc3BhY2luZ1wiOiBbXCJ3YXJuXCIsIHtcIm11bHRpTGluZVwiOiB7XCJhbGlnblwiOiBcInZhbHVlXCJ9fV0qL1xuXG5zdHlsZT17XG4gbWFyZ2luUmlnaHQ6ICc0cHgnLCBjb2xvcjogJyMwQzA5MEEnLFxufVxuIiwib3B0aW9ucyI6eyJwYXJzZXJPcHRpb25zIjp7ImVjbWFWZXJzaW9uIjoxMCwic291cmNlVHlwZSI6InNjcmlwdCIsImVjbWFGZWF0dXJlcyI6eyJqc3giOnRydWV9fSwicnVsZXMiOnt9LCJlbnYiOnt9fX0=)
@aladdin-add 
For fixing this issue, 
I thought that `the multiple properties on a single line` should be treated as a single line. And fix it. (#12472) . Am I missing something?
```js
({
   a: 1, b: 3, c:4, // single line.
});
```
We decided to revert the PR that closed this due to a regression. @yeonjuan We would love to work with you on finding an alternate solution, if you'd like still to work on this!
@kaicataldo 
I still want to work on this :).
This is an alternative solution what I thought.
```js
const obj = {
    key1: "value1", key2: "value2",  // (1)
}
```
The line *(1)* should be checked by a multiline option(`multiLine.beforeColon, multiLine.afterColon`) because the *obj* should be considered as a multi-line object.

But the `multiLine.align` is for vertical aligning. So what about just ignoring a `multiLine.align`option in this case(multiple props on the same line)?

The configuration options for this rule are really confusing 😬 

I think your proposal makes sense and we should ignore aligning a line when it contains multiple properties. 

So these would be correct:

```js
/*eslint "key-spacing": [2, {
    "singleLine": {
        "beforeColon": false,
        "afterColon": true
    },
    "multiLine": {
        "beforeColon": true,
        "afterColon": true,
        "align": "colon"
    }
}]*/
var obj = { one: 1, "two": 2, three: 3 };
var obj2 = {
    "two" : 2,
    three : 3
};
var obj2 = {
    one : 1, "two" : 2, three : 3 
};
```

Also curious what other team members think.
thanks for the issue, I was able to repro it!

Unfortunately, it looks like there wasn't enough interest from the team
or community to implement this change. While we wish we'd be able to
accommodate everyone's requests, we do need to prioritize. We've found
that accepted issues failing to be implemented after 90 days tend to
never be implemented, and as such, we [close those issues](https://eslint.org/docs/maintainer-guide/issues#when-to-close-an-issue).
This doesn't mean the idea isn't interesting or useful, just that it's
not something the team can commit to.

Thanks for contributing to ESLint and we appreciate your understanding.

[//]: # (auto-close)

reopen as it is happening in latest eslint and default parser: I've created a mini [demo](https://eslint.org/demo#eyJ0ZXh0IjoiLyplc2xpbnQgXCJrZXktc3BhY2luZ1wiOiBbXCJ3YXJuXCIsIHtcIm11bHRpTGluZVwiOiB7XCJhbGlnblwiOiBcInZhbHVlXCJ9fV0qL1xuXG5zdHlsZT17XG4gbWFyZ2luUmlnaHQ6ICc0cHgnLCBjb2xvcjogJyMwQzA5MEEnLFxufVxuIiwib3B0aW9ucyI6eyJwYXJzZXJPcHRpb25zIjp7ImVjbWFWZXJzaW9uIjoxMCwic291cmNlVHlwZSI6InNjcmlwdCIsImVjbWFGZWF0dXJlcyI6eyJqc3giOnRydWV9fSwicnVsZXMiOnt9LCJlbnYiOnt9fX0=)
@aladdin-add 
For fixing this issue, 
I thought that `the multiple properties on a single line` should be treated as a single line. And fix it. (#12472) . Am I missing something?
```js
({
   a: 1, b: 3, c:4, // single line.
});
```
We decided to revert the PR that closed this due to a regression. @yeonjuan We would love to work with you on finding an alternate solution, if you'd like still to work on this!
@kaicataldo 
I still want to work on this :).
This is an alternative solution what I thought.
```js
const obj = {
    key1: "value1", key2: "value2",  // (1)
}
```
The line *(1)* should be checked by a multiline option(`multiLine.beforeColon, multiLine.afterColon`) because the *obj* should be considered as a multi-line object.

But the `multiLine.align` is for vertical aligning. So what about just ignoring a `multiLine.align`option in this case(multiple props on the same line)?

The configuration options for this rule are really confusing 😬 

I think your proposal makes sense and we should ignore aligning a line when it contains multiple properties. 

So these would be correct:

```js
/*eslint "key-spacing": [2, {
    "singleLine": {
        "beforeColon": false,
        "afterColon": true
    },
    "multiLine": {
        "beforeColon": true,
        "afterColon": true,
        "align": "colon"
    }
}]*/
var obj = { one: 1, "two": 2, three: 3 };
var obj2 = {
    "two" : 2,
    three : 3
};
var obj2 = {
    one : 1, "two" : 2, three : 3 
};
```

Also curious what other team members think.