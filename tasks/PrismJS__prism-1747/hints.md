I'm guessing this is the pertinent test file...
https://github.com/PrismJS/prism/blob/master/tests/languages/smalltalk/string_feature.test

which I'm guessing should maybe be like this...
```
''
'foobar'
'foo''bar
baz'
----------------------------------------------------
[
	["string", "''"],
	["string", "'foobar'"],
	["string", "'foo''bar\r\nbaz'"]
]
```