Thanks for reporting @ro2ni3! This definitely seems like a bug. The copyright notices should definitely not be ~97% savings on the file we're saying :) We'll take a closer look
Turns out this is a bug in esprima which we use to tokenize the JS. It seems to erroneously think the snippet from line 54 of that file (reproduced below) has an illegal token (though oddly when invoking `esprima.parse` it is able to handle it correctly)

```js
if (-1 !== d.indexOf(","))
  for (d = d.split(","), k = 0; k < d.length; k++)
    /* fails on this regex here --> */ /^[+-]?\d+$/.test(d[k]) && (d[k] = Number(d[k]));
```

because LH uses tolerant mode, it reports what it was able to parse which is the first 3% of the file hence 97% savings :)
basically esprima sucks with regex sometimes. we use tolerant because of that

options:

1. switch from esprima to acorn or something else
2. turn back off tolerant, and deal with the errors (airhorner, etc)
3. fix this upstream in esprima? :/ 

