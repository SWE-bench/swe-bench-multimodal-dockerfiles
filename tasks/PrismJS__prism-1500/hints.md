@fabsenet me too :grinning:

I however use it more for documentation. 
From a really quick look at it, it appears to be more about the `''` part of the string than about the comment. I think our component does not handle "quote-escaped quotes" (is there a name for this?) in [the string pattern](https://github.com/PrismJS/prism/blob/master/components/prism-sql.js#L7) at the moment.