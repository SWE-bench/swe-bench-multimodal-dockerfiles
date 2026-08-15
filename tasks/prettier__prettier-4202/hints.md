Make sense, but could you provide the example input so we can use it as a test case? 
Updated. Thanks for picking this up quickly.
What about reprinting everything between `<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->` and `<!-- ALL-CONTRIBUTORS-LIST:END -->` as-is, additionally?
@j-f1 Sure! There are two specs I've ever seen - official-one you mentioned and also [Atom plugin](https://github.com/o-d-i-n/all-contributors-atom) which comprises of two parts:

```
<!-- Contributors START
Contributors END -->
```

and 

```
<!-- Contributors table START -->
<!-- Contributors table END -->
```

normally these two chunks are tightly close, on nearby-lines. 

Maybe there are more specs.
I like the idea to have a special case for `<!-- Contributors table START -->...` (or whatever it will be), but I would still like to format tables normally regardless the length.

What about just use the `<!-- prettier-ignore -->`, if someone doesn't want the specific table to be formatted?