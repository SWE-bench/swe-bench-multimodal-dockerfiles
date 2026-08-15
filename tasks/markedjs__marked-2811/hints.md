looks like the issue is that `、` is not included as [punctuation](https://github.com/markedjs/marked/blob/master/src/rules.js#L184) for left delimiter.

According to the [spec](https://spec.commonmark.org/0.30/#unicode-punctuation-character) the puctuation should include:
> an [ASCII punctuation character](https://spec.commonmark.org/0.30/#ascii-punctuation-character) or anything in the general Unicode categories `Pc`, `Pd`, `Pe`, `Pf`, `Pi`, `Po`, or `Ps`.
So, now you support only ASCII punctuations, right?

The character [`、` (`U+3001`, Ideographic Comma)][Unicode_IdeographicComma] being in Unicode `Po` category,
it's one of 'Unicode punctuation character'.

[Unicode_IdeographicComma]: https://www.compart.com/en/unicode/U+3001

Could you support such Unicode punctuations?

And, [`　` (`U+3000`, Ideographic Space)][Unicode_IdeographicSpace] is a ['Unicode whitespace character'][UnicodeWhiteSpaceCharacter] as `Zs` category character.

I think it should be also supported as a space character besides space (`U+0020`) and tab (`U+0009`), if not yet.

[UnicodeWhiteSpaceCharacter]: https://spec.commonmark.org/0.30/#unicode-whitespace-character
[Unicode_IdeographicSpace]:   https://www.compart.com/en/unicode/U+3000

Hi @UziTech can I work on this too? This one looks interesting 😀 . I might need to have some tests for japanese and chinese texts too.
@azmy60 ya you can take any that you think you can help with
There is an exhaustive collection of [utf8 punctuation in CommonMark](https://github.com/commonmark/cmark/blob/7195c6735f29be947ddc41f86c9ddfc8621d33b9/src/utf8.c#L256). Do you think we should add all of it @UziTech ? I'm not really sure how to make the tests though. Adding the _Ideographic Comma_ (as @KSR-Yasuda suggested) to the [punctuation list](https://github.com/markedjs/marked/blob/master/src/rules.js#L184) works just fine with his example.

[UPDATE]
There is a [stackoverflow answer](https://stackoverflow.com/a/37668315) for the punctuation codes. It's only up to 4 hex-digits since JavaScript only support up to `\uFFFF`.

Apparently, adding the rest of unicode punctuations also fixes #2041 by having `\uFF01`.
[marked demo](https://marked.js.org/demo/?text=**STRONG**.%20%20OK%20%20%0A**STRONG**%E3%80%82%20%20OK%20%20%0A**STRONG**%EF%BC%81%20%20OK%20%20%0A**STRONG**M%20%20OK%0A%0A**%5BSTRONG%5D(%20http%3A%2F%2Fabc.com%20)**!%20%20%20%20OK%20%20%0A**%5BSTRONG%5D(%20http%3A%2F%2Fabc.com%20)**.%20%20%20%20OK%20%20%0A**%5BSTRONG%5D(%20http%3A%2F%2Fabc.com%20)**%EF%BC%81%20%20%20bad!%20%20%0A**%5BSTRONG%5D(%20http%3A%2F%2Fabc.com%20)**%20%EF%BC%81%20%20%20OK%20%20%20%0A**%5BSTRONG%5D(%20http%3A%2F%2Fabc.com%20)**M%20%20%20bad!%20%20%0A**%5BSTRONG%5D(%20http%3A%2F%2Fabc.com%20)**%20M%20%20%20OK%20%20%20%20&options=%7B%0A%20%22baseUrl%22%3A%20null%2C%0A%20%22breaks%22%3A%20false%2C%0A%20%22gfm%22%3A%20true%2C%0A%20%22headerIds%22%3A%20true%2C%0A%20%22headerPrefix%22%3A%20%22%22%2C%0A%20%22highlight%22%3A%20null%2C%0A%20%22langPrefix%22%3A%20%22language-%22%2C%0A%20%22mangle%22%3A%20true%2C%0A%20%22pedantic%22%3A%20false%2C%0A%20%22sanitize%22%3A%20false%2C%0A%20%22sanitizer%22%3A%20null%2C%0A%20%22silent%22%3A%20false%2C%0A%20%22smartLists%22%3A%20false%2C%0A%20%22smartypants%22%3A%20false%2C%0A%20%22tokenizer%22%3A%20null%2C%0A%20%22walkTokens%22%3A%20null%2C%0A%20%22xhtml%22%3A%20false%0A%7D&version=master)
[CommonMark demo](https://spec.commonmark.org/dingus/?text=**STRONG**.%20%20OK%20%20%0A**STRONG**%E3%80%82%20%20OK%20%20%0A**STRONG**%EF%BC%81%20%20OK%20%20%0A**STRONG**M%20%20OK%0A%0A**%5BSTRONG%5D(%20http%3A%2F%2Fabc.com%20)**!%20%20%20%20OK%20%20%0A**%5BSTRONG%5D(%20http%3A%2F%2Fabc.com%20)**.%20%20%20%20OK%20%20%0A**%5BSTRONG%5D(%20http%3A%2F%2Fabc.com%20)**%EF%BC%81%20%20%20bad!%20%20%0A**%5BSTRONG%5D(%20http%3A%2F%2Fabc.com%20)**%20%EF%BC%81%20%20%20OK%20%20%20%0A**%5BSTRONG%5D(%20http%3A%2F%2Fabc.com%20)**M%20%20%20bad!%20%20%0A**%5BSTRONG%5D(%20http%3A%2F%2Fabc.com%20)**%20M%20%20%20OK%20%20%20%20)
Github Demo:

---

**STRONG**.  OK  
**STRONG**。  OK  
**STRONG**！  OK  
**STRONG**M  OK

**[STRONG]( http://abc.com )**!    OK  
**[STRONG]( http://abc.com )**.    OK  
**[STRONG]( http://abc.com )**！   bad!  
**[STRONG]( http://abc.com )** ！   OK   
**[STRONG]( http://abc.com )**M   bad!  
**[STRONG]( http://abc.com )** M   OK     

---

Looks like the second `**[STRONG]( http://abc.com )**!` needs to get fixed but the `**[STRONG]( http://abc.com )**M` is the same in CommonMark (and GitHub) so that is how it is supposed to be displayed.
PRs are always welcome 😁👍
I think the conflicting rule is this:

> A right-flanking delimiter run is a delimiter run that is (1) not preceded by Unicode whitespace, and either (2a) not preceded by a punctuation character, or (2b) **preceded by a punctuation character** and **followed by Unicode whitespace or a punctuation character.** For purposes of this definition, the beginning and the end of the line count as Unicode whitespace.

In this case, the ending `**` in example 3 ends with a `)`, and so Marked.js expects either a whitespace or a punctuation character after. Normal exclamation points (example 1) are included in our list of "punctuation characters", but the character `U+FF01 : FULLWIDTH EXCLAMATION MARK` in example 3 is not currently included in that list: From the Spec:

> A punctuation character is an ASCII punctuation character or anything in the general Unicode categories Pc, Pd, Pe, Pf, Pi, Po, or Ps.
>
> An ASCII punctuation character is !, ", #, $, %, &, ', (, ), *, +, ,, -, ., / (U+0021–2F), :, ;, <, =, >, ?, @ (U+003A–0040), [, \, ], ^, _, ` (U+005B–0060), {, |, }, or ~ (U+007B–007E).

So following that, the solution is to make sure we include the general Unicode categories listed above because `U+FF01 ` is part of the "Po (other punctuation)" set.  https://www.compart.com/en/unicode/U+FF01. `M` however is not punctuation or whitespace, so `)**M` Is not valid.