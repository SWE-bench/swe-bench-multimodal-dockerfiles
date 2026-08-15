@nknapp Any thoughts?
I'd say this rule needed to be extended to allow for the possibility of `else if`

```js
      {
        className: 'template-tag',
        begin: /\{\{(?=else\}\})/,
        end: /\}\}/,
        keywords: 'else'
      },
```

Care to take a pass at a PR?
Sure! Thanks for digging up that rule, that should make it pretty straightforward!
Any interesting in trying to make a PR?
I am! Apologies for the delay here. I will try to get to this and polish up the other PR I have open sometime in the next couple days.
@chriskrycho - would you mind if I took this off you, I've hit this exact problem and will need to patch our build, so I might as well share that; unless you've started already?