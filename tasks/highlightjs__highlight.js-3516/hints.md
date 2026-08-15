_Highlight.js_ has its own way to construct regular expression. If you are okay with plain regex, then I would recommend this:

~~~ js
const STR_REGEX = new RegExp('"(?:\\\\.|[^"])*"|\'(?:\\\\.|[^\'])*\'');
const CSS_URL_REGEX = new RegExp('\\burl\\((?:"(?:\\\\.|[^"])*"|\'(?:\\\\.|[^\'])*\'|[^\\s()]+)\\)');
~~~

 - `"(?:\\.|[^"])*"` (double quote string)
 - `'(?:\\.|[^'])*'` (single quote string)
 - `[^\s()]+` (any character sequence but white-space, `(` and `)`
Try to include the `STRINGS` regex here:

https://github.com/highlightjs/highlight.js/blob/d64f68e8aabc67820eec2459bff9a7a0fcc06b95/src/languages/css.js#L85-L94

~~~ js
contains: [
  ...STRINGS, // <-- this!
  {
    className: "string",
    // any character other than `)` as in `url()` will be the start
    // of a string, which ends with `)` (from the parent mode)
    begin: /[^)]/,
    endsWithParent: true,
    excludeEnd: true
  }
]
~~~