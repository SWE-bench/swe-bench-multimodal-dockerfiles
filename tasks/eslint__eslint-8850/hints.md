Thanks for reporting, I can reproduce this. It was probably caused by https://github.com/eslint/eslint/commit/b5a70b4e8c20dc1ea3e31137706fc20da339f379.

Simplified reproduction case:

```js
/* eslint indent: error */
<div>
    {
        (
            1
        )
    }
</div>
```

An error is reported, and the rule corrects it to the following (incorrect) code:

```js
/* eslint indent: error */
<div>
    {
    (
        1
    )
    }
</div>
```