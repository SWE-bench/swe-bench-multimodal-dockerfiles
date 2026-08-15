@marc-medley 
May I ask what the `*` property refers to? I can't find it in the linked Wikipedia page.
 `/;.*/` is comment string wildcard 

`property…\*)…` is for a checksum field that may appear at the end of the executable portion of the line:

```
N3 T0*57 ; This is a comment
N4 G92 E0*67
; So is this
N5 G28*22
```
see https://reprap.org/wiki/G-code#.2A:_Checksum

@marc-medley 
Thank you!

We might as well also add [strings](https://reprap.org/wiki/G-code#Quoted_strings) before they destroy our comments.
> … also add strings before they destroy our comments.

good catch.