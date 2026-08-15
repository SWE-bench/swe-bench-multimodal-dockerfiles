> Technically, as far as the C++ standard is concerned, primitive types are keywords.

This isn't highly relevant though (for us), as often we make decisions that improve the consistency of highlighting (across languages) without overly weighting any particular language.  The idea being that highlighting snippets somewhat consistently across languages is a higher (and more achievable) goal than absolutely correctness with accordance to one particular language.  IE: It doesn't matter if type is literally a type in C while literally a keyword in CPP, etc... C and C++ code (two different grammar types for us) should highlight similarly - with things that appear to be primitive types highlighted at `type`.

I think if anything we should perhaps add the type modifiers so that they also highlight as `type`... making the entire "type definition" (sorry, terminology) highlight as a type...  since that seems to be your real concern here - the modifiers having different highlighting than the types themselves.

At the very least...

- `signed int`
- `unsigned int`

...do seem broken the way we're doing it now, as my understanding is the type name includes the signed/unsigned prefix.

Also worth pointing out this is entirely within the users control via CSS:

```css
.language-cpp .hljs-type {
  color: /* whatever */
}
```

... if they want to erase the type/keyword distinction for `cpp`.

@joshgoebel, thanks for the detailed reply!

> > Technically, as far as the C++ standard is concerned, primitive types are keywords.
> 
> This isn't highly relevant though (for us), as often we make decisions that improve the consistency of highlighting (across languages) without overly weighting any particular language. The idea being that highlighting snippets somewhat consistently across languages is a higher (and more achievable) goal than absolutely correctness with accordance to one particular language. IE: It doesn't matter if type is literally a type in C while literally a keyword in CPP, etc... C and C++ code (two different grammar types for us) should highlight similarly - with things that appear to be primitive types highlighted at `type`.

I get the point. I just wanted to point out that the current highlighting looks
unusual in the C/C++ context. One small comment: primitive types are also
keywords in [C standard](https://en.cppreference.com/w/c/keyword) :)

> I think if anything we should perhaps add the type modifiers so that they also highlight as `type`... making the entire "type definition" (sorry, terminology) highlight as a type... since that seems to be your real concern here - the modifiers having different highlighting than the types themselves.
> 
> At the very least...
> 
> * `signed int`
> * `unsigned int`
> 
> ...do seem broken the way we're doing it now, as my understanding is the type name includes the signed/unsigned prefix.

Okey.

> Also worth pointing out this is entirely within the users control via CSS:
> 
> ```css
> .language-cpp .hljs-type {
>   color: /* whatever */
> }
> ```
> 
> ... if they want to erase the type/keyword distinction for `cpp`.

The CSS rule also affects type names with the `_t` suffix, which are usually
highlighted separately from primitive types:

Highlightjs ([jsfiddle](https://jsfiddle.net/aLcy6gpo/)):
<img width="200" alt="hljs" src="https://user-images.githubusercontent.com/15797194/130642653-a787be14-91b0-45fd-a7a5-fa029bd4c981.png">
IDEs:
<img width="200" alt="VisualStudioCode" src="https://user-images.githubusercontent.com/15797194/130641161-ff4bc4a0-f793-4698-b7d6-032225a6a941.png">
<img width="200" alt="CLion" src="https://user-images.githubusercontent.com/15797194/130641150-3dea31fc-5cd2-4c44-95b4-77568dcc3fd9.png">
<img width="200" alt="XCode" src="https://user-images.githubusercontent.com/15797194/130641162-c2119913-cede-444e-81e3-d916595c0d7d.png">

The separation of primitive types and types that have definitions can be
another argument in favor of recognizing primitive types as keywords. May I get
your opinion?