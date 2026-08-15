Hey thanks so much for reporting this!

> is there a fix we can do on our side regarding the usage of AccordionItem?

I don't think so unfortunately. I'll put up a PR to change the inbuilt prefix for v10 so there won't be conflicts between libraries.
It's worth mentioning that I think this could also be fixed via https://github.com/carbon-design-system/carbon/issues/11513 but we haven't gotten React 18 support fully baked yet.
@Properko In thinking about this more - I'm curious, would you prefer a way to customize the prefix used for the ids? I think it might be the best way to keep both v10 and v11 backwards compatible while allowing you control so you can avoid duplicates.

I think we could wire up something similar to `ClassPrefix` that would enable you to control the id prefix used at any point in your react/app tree.
> It's worth mentioning that I think this could also be fixed via #11513 but we haven't gotten React 18 support fully baked yet.

I'm not sure we could make the move to React 18 anytime soon either. But it's nice to hear that it gets fixed eventually.

> I think we could wire up something similar to ClassPrefix that would enable you to control the id prefix used at any point in your react/app tree.

Yep, that's a perfectly fine solution. Filling an extra property on `AccordionItem` is much better than creating a new custom component we'd have to maintain. But we do need to fix the accessibility violations.