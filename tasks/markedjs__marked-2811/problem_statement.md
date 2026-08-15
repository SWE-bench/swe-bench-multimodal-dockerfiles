Syntax parse fails with Japanese punctuation (`、`), strong syntax and code syntax
**Marked version:**

* v4.0.18

**Describe the bug**
A clear and concise description of what the bug is.

Copy from https://github.com/volca/markdown-preview/issues/135.

The case below, it does not parse syntax correctly.

```bash
% cat test.md
* ×: あれ、**`foo`これ**、それ
* ○: あれ、 **`foo`これ**、それ
* ×: あれ、**`foo`これ** 、それ

* ○: あれ、**fooこれ**、それ
* ○: あれ、 **fooこれ**、それ
* ○: あれ、**fooこれ** 、それ

% npx marked --version
4.0.18

% npx marked < test.md
<ul>
<li><p>×: あれ、**<code>foo</code>これ**、それ</p>
</li>
<li><p>○: あれ、 <strong><code>foo</code>これ</strong>、それ</p>
</li>
<li><p>×: あれ、**<code>foo</code>これ** 、それ</p>
</li>
<li><p>○: あれ、<strong>fooこれ</strong>、それ</p>
</li>
<li><p>○: あれ、 <strong>fooこれ</strong>、それ</p>
</li>
<li><p>○: あれ、<strong>fooこれ</strong> 、それ</p>
</li>
</ul>
```

With Japanese punctuation (`、`), strong syntax (`**`), and code syntax (`` ` ``),
it needs some space to make them parsed correctly (The former 3 examples).

Although, without code syntax, no extra space is required (The latter 3 examples).

So it isn't a syntax parsing problem with CJK symbol characters?

**To Reproduce**
Steps to reproduce the behavior:

As above.







**Expected behavior**
A clear and concise description of what you expected to happen.

Parse the syntax correctly as [Pandoc](https://github.com/jgm/pandoc).

```bash
% pandoc --version
pandoc.exe 2.18
Compiled with pandoc-types 1.22.2, texmath 0.12.5, skylighting 0.12.3,
citeproc 0.7, ipynb 0.2, hslua 2.2.0
Scripting engine: Lua 5.4
User data directory: C:\Users\yasuda\AppData\Roaming\pandoc
Copyright (C) 2006-2022 John MacFarlane. Web:  https://pandoc.org
This is free software; see the source for copying conditions. There is no
warranty, not even for merchantability or fitness for a particular purpose.

% pandoc < test.md
<ul>
<li><p>×: あれ、<strong><code>foo</code>これ</strong>、それ</p></li>
<li><p>○: あれ、 <strong><code>foo</code>これ</strong>、それ</p></li>
<li><p>×: あれ、<strong><code>foo</code>これ</strong> 、それ</p></li>
<li><p>○: あれ、<strong>fooこれ</strong>、それ</p></li>
<li><p>○: あれ、 <strong>fooこれ</strong>、それ</p></li>
<li><p>○: あれ、<strong>fooこれ</strong> 、それ</p></li>
</ul>
```

link inside of  Strong delimiter, the strong delimiter not work
**Marked version: https://github.com/markedjs/marked/blob/009427f65dadd5dff9ec0189e008677aea9fbcfa/lib/marked.js**

**Describe the bug**
When there is a link inside of a strong delimiter, followed closely by a character other than `[ .!,;] ....`, the strong delimiter is broken.

**To Reproduce**
![image](https://user-images.githubusercontent.com/11593903/117394732-a582c080-af31-11eb-919b-c15cf5f16069.png)

```
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
```

**Info**
Old Version don't have this issue.  
- A chrome extension called [Markdown Preview Plus](https://chrome.google.com/webstore/detail/febilkbfcbhebfnokafefeacimjdckgl) uses a relatively new version of marked, and it has this same problem.
- The [browserify-markdown-editor](https://github.com/thlorenz/browserify-markdown-editor) uses an old version of marked ( 0.2.9 ), and it don't have this problem. https://thlorenz.com/browserify-markdown-editor/ 


**Expected behavior**  
The strong delimiter should bolden the wrapped text no matter of what's inside and what's behind.

