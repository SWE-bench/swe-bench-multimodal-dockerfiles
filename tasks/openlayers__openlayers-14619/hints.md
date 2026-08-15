The documentation for `setScale()` says `Set the scale and updates the width and height correspondingly.`  However the only update which would make sense would be to clear any width or height already set, in which case `setWidth()` and `setHeight()` should be available as API methods to reset them.  The alternative would be to throw the same assertion as the constructor if conflicting settings are attempted.
Yes, this would be better. If `setScale()` sets width and height it can't be used afterwards anymore.
@M-Bitt Nonetheless, the cloned icon should result in the same visual result, doesn't it?

I created #14606 to fix the case where the cloned icon would get a zero width and height and a scale of 1, regardless of what the original had. For other cases, the visual appearance of original and clone should be the same.
@mike-000 

> The alternative would be to throw the same assertion as the constructor if conflicting settings are attempted.

This would be one way to solve the underlying problem, but I think removing `setWidth()` and `setHeight()` altogether would save us headache in the future.
@ahocevar Yes, of course the cloned icon should be the same. But when the clone gets basically a Scale of 1 it is not the same as the original and still has to be set manually after cloning, right? Why not setting the scale of the original icon? 
@M-Bitt This problem with the scale of 1 will be fixed by #14606.
@ahocevar Oh sorry, I missunderstood your comment. 