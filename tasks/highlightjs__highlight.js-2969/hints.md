Good find.  How did you get the expected behavior shot? :)  Is there a PR forthcoming? :)

I think all of these look fixable at first glance.
Agreed, most should be a simple regex change, though I don't quite understand why the single unicode char (`あ`) is not supported currently.

I might look into a PR later, but for the expected image I manually hacked the html. :D
> I don't quite understand why the single unicode char (あ) is not supported currently.

It's not in the regex?

```
        begin: /\B\?(\\\d{1,3}|\\x[A-Fa-f0-9]{1,2}|\\u[A-Fa-f0-9]{4}|\\?\S)\b/
```

I am not sure that \S works with fancy UTF-8 stuff.
`\S` seems to match unicode:
![image](https://user-images.githubusercontent.com/2564094/103816702-4449ef80-501a-11eb-9c79-bb11a1e44e2a.png)
https://regexr.com/5jodu
Ah, but that character does not form a word boundary so `\b` will abort the match.

If we're going to fix this we need variants, not one big regex. :)