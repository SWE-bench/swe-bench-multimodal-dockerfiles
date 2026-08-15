Thanks for letting us know @tofumatt! Are you still willing to dual-license it?

cc @Automattic/team-calypso @sgomes 
Like I mentioned: doing so in a new release should be fine. The intent of the Apache 2.0 license was to make the code safer to use regarding patent clause nonsense; I think https://opensource.com/article/18/2/how-make-sense-apache-2-patent-license is a decent writeup from my skimming it, because I don't want to re-write my thinking on it 😆

If @thgreasi is cool with it we can go ahead with offering it under another license. I've opened an issue to track it: https://github.com/localForage/localForage/issues/892
@tofumatt I have no objection on something like this but also don't have enough background. Imo dual licensing sounds like a smaller change but again I'm not an expert on licensing.
@blowery As far as I can tell, `localforage` is mainly used in Calypso as a way of having a`localStorage`-like API with promises, while being able to use `IndexedDB` as a target too. Beyond that, there's a convenient `bypass` module that instead stores everything in memory (for use when data shouldn't be persisted, such as during support), and can be activated when needed.

With the licensing situation, and given that `localforage` weighs over 8KB (compressed) in our critical path, I'd argue this is a good time to reevaluate if we really need it, or if a small wrapper with bypass support (perhaps writing to `sessionStorage`?) would suffice instead.
Writing to `sessionStorage` would lose out on both the Promises and the `IndexedDB` benefits of localForage. Are you using localForage's in-memory driver to do the `bypass` module? localForage has an in-memory driver in localForage as well, so simply switching to that when you want to avoid persistence might simplify your code path if you're currently doing the `bypass` mode yourself. 

Side note: I've been thinking about removing callback support in the next version of localForage to get the size of the library down (it would remove a fair bit of code we only support to have callbacks, which at this point are an uncommon API or at least one I'm not interested in keeping around in V2).

That won't happen for awhile though. Seems like there's not an issue with dual-licensing though, so I'll cut a new minor release of localForage with a new dual-license this week and update this issue when it's out.
> As far as I can tell, localforage is mainly used in Calypso as a way of having a localStorage-like API with promises, while being able to use IndexedDB as a target too

We use `localforage` to store Redux state to IndexedDB:
<img width="495" alt="Screenshot 2019-06-12 at 17 48 44" src="https://user-images.githubusercontent.com/664258/59366413-93df1100-8d3a-11e9-8f4d-2a74ec6f4d5f.png">

That's all. There a handful of other cases where we store stuff to localStorage directly, using the `store` library or directly, and that's all theoretically legacy code that should be migrated to Redux.

Today, in practice, I think we always use IndexedDB and none of the fallbacks. IE 11 has ["partial support"](https://caniuse.com/#feat=indexeddb), which is probably sufficient for us. And Safari supports it fully since version 10, released in Sep 2016.

Trying to create a minimal wrapper that provides a set/get API with promises on top of the verbose low-level IndexedDB seems like a good idea to me. It should have just a few lines.
Ah, okay, thanks for the extra context.

It sounds like there isn’t an interest in the continued use of localForage in WP.com; if that’s the case I don’t think I should bother re-licensing localForage as I would have mainly done so for Calypso 😄. Dual-licensing could be confusing for others so I think it's best localForage avoids that.

I'll close this issue as it sounds like the solution to this licensing issue is to move away from localForage. (As a side note: it might be helpful to check out Gutenberg's GPL checker to make sure there aren't other software packages you're using that are not GPL 2-compatible 💡)

Cheers!