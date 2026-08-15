The `\n`s aren't a problem, but the single quotes around `'eslint:recommended'` are. ~~I've also never seen `$'something'` before.~~ Edit. Should have read the doc. First point stands tho.
Prism's highlighting is (mostly) correct.

![image](https://user-images.githubusercontent.com/20878432/110240975-b7a2ab80-7f4e-11eb-8734-c6a4b4c6bc3b.png)

In your example, you echo multiple strings that are concatenated and not one long string. As per [spec](https://www.gnu.org/software/bash/manual/html_node/Single-Quotes.html):

> Enclosing characters in single quotes (`‘'’`) preserves the literal value of each character within the quotes. __A single quote may not occur between single quotes__, even when preceded by a backslash.

Here is the output of the echo command on my machine:

```console
micha@DESKTOP-DCVE9I0:/mnt/c/Users/micha$ echo $'module.exports = {\n  extends: [\n    // add more generic rulesets here, such as:\n    // 'eslint:recommended',\n    "plugin:vue/vue3-recommended",\n    "prettier",\n    "prettier/vue",\n  ],\n  rules: {\n    // override/add rules settings here, such as:\n    // 'vue/no-unused-vars': 'error'\n  },\n};'
echo $'module.exports = {\n  extends: [\n    // add more generic rulesets here, such as:\n    // 'eslint:recommended',\n    "plugin:vue/vue3-recommended",\n    "prettier",\n    "prettier/vue",\n  ],\n  rules: {\n    // override/add rules settings here, such as:\n    // 'vue/no-unused-vars': 'error'\n  },\n};'
module.exports = {
  extends: [
    // add more generic rulesets here, such as:
    // eslint:recommended,\n    "plugin:vue/vue3-recommended",\n    "prettier",\n    "prettier/vue",\n  ],\n  rules: {\n    // override/add rules settings here, such as:\n    // vue/no-unused-vars: error\n  },\n};
```

That being said, I'll add support for ANSI-C Quoting.
I see. So, ANSI-C quotes behave differently in `bash` and `zsh`.
![image](https://user-images.githubusercontent.com/46059092/110241801-1a964180-7f53-11eb-9bbe-92488028adef.png)

That's interesting. [zsh docs](http://zsh.sourceforge.net/Doc/Release/Shell-Grammar.html#Quoting) says this:

> A string enclosed between `‘$’’` and `‘’’` is processed the same way as the string arguments of the `print` builtin, and the resulting string is considered to be entirely quoted. A literal `‘’’` character can be included in the string by using the `‘\’’` escape.

Luckily, the [doc for `print`](http://zsh.sourceforge.net/Doc/Release/Shell-Builtin-Commands.html#:~:text=print%20[%20-abcDilmnNoOpPrsSz%20]) doesn't mention how string arguments are processed... At least, I couldn't find it. If I had to guess, then zsh requires a space (or the end of the command/line) after the second `'` for it to be the closing quote.

Anyway, the zsh behavior is incompatible with bash and won't be supported in the bash language.