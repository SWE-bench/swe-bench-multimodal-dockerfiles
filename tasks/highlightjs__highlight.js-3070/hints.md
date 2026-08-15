> but it adds an extra php tag. If I don't give a class, it adds the php class and there is no problem.

For clarity, what is the actual problem you are having with this extra class name?  

---

The inconsistency is not great, but at first glance it's not at all clear that the problem is the classes appearance for PHP, but rather the fact that this isn't the behavior in all cases.  Some of our themes *depend* on this very behavior and would currently be broken for anyone using `lang` prefixes with many of our grammars.

There were some changes made to this code recently.  I'll need to check if we unintentionally broke the prior behavior and if so we will likely restore it (adding extra classes for all grammars). This may not be desirable behavior long-term, but I'm not sure we should forcefully change it until v11 and it's a potentially breaking change for some users.


So this behavior was changed unintentionally in https://github.com/highlightjs/highlight.js/commit/3198e92629c8c09f9372e279dd833884e4edb839 and has been released in 10.5 and 10.6.

The previous behavior was based on string matches (which was never optimal, and part of the reason it was changed).  IE, if "php" was found *anywhere in the full class name*, then it was not added as a separate class. Hence, because `php` can be found in `lang-php` it would not have been added twice... 

_Unless one used an alias..._ such as `lang-php8` or `lang-js`, etc... in which case the alias lookup would first be performed and since `lang-js` does not include `javascript` then `javascript` would be added to the class list.  This behavior is still included and the strange `php` and `isbl` (possibly others) behavior is attributed to the fact that `php` includes `php` as an alias (which it really shouldn't) - which gives it this unique behavior.

---

#### The larger problem


The problem with themes (that hard-code grammar names in the CSS) remains... and another complexity is that `languageDetectRe` is currently configurable... so technically it'd be impossible to say just update our CSS (say to change `.php` to `.language-php`) since users can reconfigure this at will... someone could use `grammar-[lang]` and hence break our themes again.

We could simply remove this configuration with v11, but that would leave no user with tons of static HTML (blog, etc) that already uses one or the other prior convention with no way upgrade path.

The problem with `.php` of course is [I'm assuming?] name collisions (no namespace), though this hasn't seemed to be a practical problem.  I don't recall it coming up before now.  At first glance only a few themes (3-4) include per grammar style tweaks... so this could be something we simply say that we disallow (in 1st party themes) and kick those themes out of core and then there would be no need to ever add the raw names (`php`, `javascript`, etc) to className at all?

@highlightjs/core Any thoughts?
I think smaller-scale I'd be open to a PR that removed `php` and `isbl` from their own `aliases` list, which would effectively restore the behavior from 10.4 - without reverting to the broken string inclusion code.  That would prevent `language-php` from adding `php` as a a class (because the alias lookup for `php` would return `null`)... leaving that behavior ONLY for aliases - which is where we'd still need a discussion to solve the higher-level problem.
There is no problem in terms of operation. It just adds "php" class as an extra. I checked the "highlightBlock" behavior, there is no problem there either. If the "language-php" class exists, it directly emphasizes it with the php language. So, "highlightAuto" is not working as it should be. I just tried to figure out why it added an extra php class, because in working condition there is no problem at all.

Like I found where the problem is.

https://github.com/highlightjs/highlight.js/blob/5b3a22e9be3985ef0c1a98a012462cd3ddc36af9/src/languages/php.js#L106
Yes, that's what I said here: https://github.com/highlightjs/highlight.js/issues/3023#issuecomment-787107000

That solves the immediate reported problem, but not the larger problem I mentioned that some themes REQUIRE this extra css class to work properly... so right now we have a situation where using `language-js` vs `language-javascript` could result in different presentation behavior, which is something we need to sort out.
Yes I understood. Due to alias, extra classes are being added in languages ​​such as `javascript`, `php`, `html`.
If you want to submit a PR to fix `php` and `isbl` aliases (and any others) I'd merge it.
I propose we perhaps make `lang-javascript` or `language-javascript` canonical with v11 (we can leave the config option, but change it to the single "winner") and update any styles referring to languages to this longer class name.  And `updateClassName` would be changed so that upon auto-detection the longer classname would be applied - so we'd always be using the prefixed version.

I first thought of `.hljs.javascript` for our CSS (tags with both `hljs` and `javascript`) but this doesn't solve the issue of potential conflicts with users using `javascript` in their own CSS... although no one has really reporting this as being an actual problem in the past.

I don't consider this a high priority really but if anything makes sense here v11 would be a good time to break the old behavior and usher in the new.

CC @highlightjs/core 
@allejo Any thoughts on this?
I reached out to the Nord author since they are the *only* theme that actually has per-language overrides, making me think we should just stop adding these CSS classes at all (by default).  And disallow themes from setting styles per language (which are also subject to be quite brittle as grammars develop over time but themes tend to be super-static).
@Hirse CCing you since you've done some theme work.
@Hirse HAHA. I was wondering if you had any thoughts on the matter. :)
> @Hirse HAHA. I was wondering if you had any thoughts on the matter. :)

I do. :)

For the CSS classes of tokens (`string`, `variable` etc.) we use prefix to not interfere with other styles, so I would be in favor of not using language names as classes directly either. (I.e. **not** `.hljs.javascript`)

I think I read somewhere that the HTML working draft spec prefers `language-javascript` over `lang-javascript`, but couldn't find it again. I would be in favor of whichever is more "official".

I don't think core-themes should use the language to reduce maintenance overhead, but it might be nice to have the language available as a CSS class for third-party themes.

In summary, I think the language name should be included in a standardized way, either as `hljs-<language_name>` or `lan guage-<language_name>`.
Part of the problem is I'm not sure there is any spec here at all. `hljs-[name]` would be the safest choice from a "do not conflict with other class names" perspective. But then we have a problem if a new language would ever overlap with a highlighting class... so now you're back to `hljs-language-[name]`... a bit of a mouthful, but precise enough.

> but it might be nice to have the language available as a CSS class for third-party themes.

One can also easily do this with a one-line plugin... should we perhaps just let those who wish to have such things do it themselves?  

Example:

https://github.com/highlightjs/highlight.js/blob/main/docs/plugin-recipes.rst#data-language

CC @allejo 

---

So I'm kind of leaning towards:

- `hljs-language-[grammar name]` precise and hopefully future proof.
- Simply do not add a class by default at all, refer people to one line plugin recipe.

Don't feel I have a strong preference.   Either would be a breaking change so this needs to be decided before v11.