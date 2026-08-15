Thanks for the report!

Could you make your example fully reproducible by adding the required yaml header, _i.e._, at least `format: revealjs`.
@mcanouil done! 
> I suspect that this is caused by the logic of how standalone images are rendered (and the link is ignored/stripped).

Definitely. This is due to the auto stretch feature. If you opt out on the slide, it will work 
````markdown
## Slide (link won't work) {.nostretch}

[![](https://quarto.org/docs/blog/posts/2023-04-26-1.3-release/arthur-chauvineau-Dn7P1U26ZkE-unsplash.jpeg)](https://google.com) 
````

I don't think the stretch feature from revealjs is applicable to an image inside a link as it works only for first level `<img>` under `<section>`. 🤔 

So we could probably not touch the image if inside a link syntax. That would mean no stretching of size, and size should be manual. Would it be better ? 
> 

> So we could probably not touch the image if inside a link syntax. That would mean no stretching of size, and size should be manual. Would it be better ?

I am converting old RevealJS MD to Quarto, and it was confusing that the link didn't work anymore. If I saw the image wasn't stretched, I think I prefer to fix that problem as a second step. I hope that answers your question.
Yes it makes sense. It won't be possible to apply the stretching feature from image within link though. I don't think that works. 
