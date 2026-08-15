Just to be clear is this an issue with latest v11 also then?
Ahh sorry, yes the wasn't very clear.

I found the problem in 11.1.0.

10.3.0 only came up because that was the first version I could find which showed the problem.


Isn't `<>` typecasting deprecated in favor of `as`?

```
  parse: <From extends string>(
    value: From
  ) => number;
```

I'm not sure I'm even following what this is doing sytantically.