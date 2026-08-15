TypeScript too. Ideally we'd be able to remove the `typescript` dependency too and go through babylon, as it will be much faster.
Are there benchmarks comparing with Babylon 7 beta? AFAIK it's supposed to be much faster than 6
  
Note that it [only supports stage 3 features](https://github.com/cherow/cherow#features) which could be a problem for users of stage 0-2 features.

It might be better to create a `prettier-plugin-cherow` module that allows people to opt into Cherow if they’re using stage 3+ JS features.
We should probably benchmark how much time is actually spent parsing before pursuing this, to avoid implementing a premature optimization.

I think it should definitely be a plugin, though, rather than a builtin parser, due to the limitations.
`cherow` is no longer maintained.
its successor: https://github.com/meriyah/meriyah