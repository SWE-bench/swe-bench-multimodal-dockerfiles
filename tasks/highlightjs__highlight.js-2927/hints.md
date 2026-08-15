Never heard of `LL` before... shouldn't be a hard fix I don't think.  Care to try for a PR?
It's the suffix for `long long` which existed as an extension for decades, and was [officially added to C99](https://en.cppreference.com/w/c/language/arithmetic_types) more than 20 years ago
Good to know.  Want to try contributing a PR? :)
Sorry I haven't looked at the source code of highlight.js yet, and currently I don't have enough time to look through it. May be at the weekend
Current rule, line 73 `c-like`:

```
begin: '(-?)\\b([\\d\']+(\\.[\\d\']*)?|\\.[\\d\']+)(u|U|l|L|ul|UL|f|F|b|B)'
```