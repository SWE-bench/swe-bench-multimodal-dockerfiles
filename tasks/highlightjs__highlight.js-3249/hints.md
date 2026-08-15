> TeX magic comments are, in most editors, case insensitive, s

That could well be a bug with the editor or it's highlighting... I presume you also mean that LaTex itself draws no distinction, am I correct?  Or are we speaking about multiple flavors of LaTex here with different behaviors?

I don't think I see any real issue with this though (making comment detection case insensitive).  Thoughts? CC @schtandard


> That could well be a bug with the editor or it's highlighting... I presume you also mean that LaTex itself draws no distinction, am I correct? Or are we speaking about multiple flavors of LaTex here with different behaviors?

No, as far as LaTeX is concerned magic comments are just comments: completely ignored.  The magic is a feature implemented in some LaTeX-aware IDEs so that you can easily change command-line options from within the source (for example, with standard settings, an editor would run `pdflatex <some file>.tex`, but with the magic comment `% !TeX program = lualatex` it would run `lualatex <some file>.tex` instead).  Then, while searching for the pattern, most IDEs use a case-insensitive search, so changing the syntax highlighting to reflect that seems appropriate.
I don't see a reason why we couldn't accept a PR to fix this.
@joshgoebel I'd write the PR myself, but I'm afraid my javascript knowledge is roughly zero, sorry: I just know enough LaTeX to come here and complain :)

This is really of minor importance, so I'm fine with whenever someone knowledgeable has some free time to dedicate to this
I fully agree that this should be changed and I can take care of this. The space in front of the `!` also seems to be optional, at least in TeXStudio. @PhelypeOleinik For TeXStudio, only the `e` seems to be case insensitive. Do you know if this is universal or should we just make the whole word case insensitive in case other editors are more lenient?
@schtandard I did some digging, and the results vary wildly :)

 - TeXShop seems to be case-sensitive: it uses `rangeOfString:@"%!TEX TS-program ="`, which as far as I could guess, uses the case-sensitive function `rangeOfString` (with no options to make it case-insensitive). Also no spaces around the `!`;
 - TeXStudio, as you said, allows `e` and `E`: `rxMagicTexComment("^%\\ ?!T[eE]X");`, with an optional space before the `!`. It also recognizes a `BIB` magic comment: `rxMagicBibComment("^%\\ ?!BIB");`;
 - TeXWorks is case-insensitive with as many spaces as you like almost everywhere: `RegExp("% *!TEX +spellcheck *=", "i");`
 - LaTeXTools (Sublime Text) is case insensitive for the `TEX` string, plus it allows things like `%%% ​ ​ !tEx ​ ​ <thing> ​ ​ = ​ ​ `. Pretty wild: `r'%+\s*!(?:T|t)(?:E|e)(?:X|x)\s+([\w-]+)\s*=\s*' +`;
 - LaTeX-Workshop (VSCode) allows `e` and `E` as TeXStudio, and spaces wherever you fancy: `regexTex = /^(?:%\s*!\s*T[Ee]X\s(?:TS-)?program\s*=\s*([^\s]*)$)/m`. It also recognizes `BIB` comments (case insensitive);
 - Atom-LaTeX allows `e` and `E` and spaces mostly everywhere: `RegExp('^%\\s*!T[Ee]X\\s+(\\w+)\\s*=\\s*(.*)$')`;

I couldn't find anything about VimTeX or Overleaf, but [this post](https://tex.stackexchange.com/a/84687/134574) says they support magic comments.

AUCTeX uses its own thing at the end of the file; not sure if worth supporting, mostly because they aren't as “magic looking”:
```tex
% Local Variables:
% mode: doctex
% TeX-master: t
% End:
```

Finally, web2c implementations also allow a comment on the first line of a file of the format `%&<format>` which, in this case, is parsed by the TeX engine (sort of). But I don't think this is used enough to be worth highlighting. For example, you can run this example with `pdftex` and it will select the right format:
```latex
%&latex
\documentclass{article}
\begin{document}
\end{document}
```

---

*TL;DR*

Thinking a bit more about it, I don't think it's a good thing to highlight all the possible combinations (like `%%% ​ ​ !tEx ​ ​ <thing> ​ ​ = ​ ​ `). I think I'd take a good enough subset, maybe (in PCRE): `^% ?! ?T[eE]X ([\w-]+) ?= ?.+$`, because mostly only `TeX` and `TEX` are used, and spaces are optional (because I'd be the first to forget where they are required/forbidden :). Since this seems to require a begin and end, then `begin: '^% ?! ?T[eE]X '` and `end: $`. What do you think?

Oh, and maybe `begin: '^% ?! ?BIB '` as well?
@PhelypeOleinik Thanks a lot for your research! I mostly agree with your conclusions, except for two minor points. I don't feel strongly about either of them, though.
- I would omit the optional space after the `!`. I have never seen this and according to your list only LaTeX-Workshop supports it. I guess the idea is to allow `%! TeX` and I sympathise with your point about remembering where spaces are allowed, but this feels like too much of a niche case to me.
- I agree that case mixing like `tEx` is a bit absurd, but should we maybe allow `tex` and `bib`? This seems a reasonable spelling to me (for the editors that support them) and is also in line with the "just use lowercase" default many technical users may be used to.

About the `^`: At least TeXStudio accepts magic comments anywhere in the document with no restriction of being the only thing on that line. (I didn't test any other editors.) While I myself only ever use them on the first lines of a document (with no indentation), I wouldn't make that a requirement for highlighting.

With all this my suggested regex would be `% ?!(?:T[eE]X|tex|BIB|bib)`. Any comments? (No pun intended.)
>     * I would omit the optional space after the `!`. I have never seen this and according to your list only LaTeX-Workshop supports it. I guess the idea is to allow `%! TeX` and I sympathise with your point about remembering where spaces are allowed, but this feels like too much of a niche case to me.

Sounds reasonable. Given the plethora of different implementations, some level of restriction is good, so I'm fine with no space after `!`.

>     * I agree that case mixing like `tEx` is a bit absurd, but should we maybe allow `tex` and `bib`? This seems a reasonable spelling to me (for the editors that support them) and is also in line with the "just use lowercase" default many technical users may be used to.

Sounds good too.

> With all this my suggested regex would be `% ?!(?:T[eE]X|tex|BIB|bib)`. Any comments? (No pun intended.)

Go for it! (the regex, not the pun :)