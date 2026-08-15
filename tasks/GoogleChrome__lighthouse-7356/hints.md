I also suspect waitForFCP here. Do we also see a drop in NO_FCP errors? I would hope and expect that we do. 

If we do, then I'd say this is still a net positive.

If we don't, then it seems like all we've done when waiting for FCP is make the user wait longer to get the same error.

Either way, I like the idea of failing early after some `maxWaitForFCP` time that's shorter than `maxWaitForLoad`.