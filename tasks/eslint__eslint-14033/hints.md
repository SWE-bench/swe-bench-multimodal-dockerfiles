Hi @darlandemarco, thanks for the issue!

I can confirm that `let foo = undefined;` gets auto-fixed to `const foo;`

You're using an old ESLint version, but this happens in the actual version as well: [Online Demo](https://eslint.org/demo#eyJ0ZXh0IjoiLyogZXNsaW50IHByZWZlci1jb25zdDogXCJlcnJvclwiICovXG4vKiBlc2xpbnQgbm8tdW5kZWYtaW5pdDogXCJlcnJvclwiICovXG5cbmxldCBmb28gPSB1bmRlZmluZWQ7XG4iLCJvcHRpb25zIjp7InBhcnNlck9wdGlvbnMiOnsiZWNtYVZlcnNpb24iOjYsInNvdXJjZVR5cGUiOiJzY3JpcHQiLCJlY21hRmVhdHVyZXMiOnt9fSwicnVsZXMiOnt9LCJlbnYiOnt9fX0=) 
> **Are you willing to submit a pull request to fix this bug?**
> Yes, need some guidance but I can do this :)

That would be great, thanks!

I think the "fix range" of `prefer-const` should be extended to the whole declaration, in order to prevent other fixes in the same pass. Then, in the second pass, `no-undef-init` will see `const` and won't report an error.

There's [fix-tracker](https://github.com/eslint/eslint/blob/master/lib/rules/utils/fix-tracker.js) helper for this purpose. We should call [retainRange](https://github.com/eslint/eslint/blob/110cf962d05625a8a1bf7b5f4ec2194db150eb32/lib/rules/utils/fix-tracker.js#L41) and then [replaceTextRange](https://github.com/eslint/eslint/blob/110cf962d05625a8a1bf7b5f4ec2194db150eb32/lib/rules/utils/fix-tracker.js#L83).

You can find some examples of use in rules such as `semi`, `no-extra-semi`, `no-else-return`, and `no-useless-return`.

A test case for `prefer-const` that should pass after the change:

```js
// https://github.com/eslint/eslint/issues/13899
{
    code: "/*eslint no-undef-init:error*/ let foo = undefined;",
    output: "/*eslint no-undef-init:error*/ const foo = undefined;",
    errors: 2
}
```
Can I work on this issue?
@snitin315 sure, thanks! It doesn't seem anyone is working on this at the moment.