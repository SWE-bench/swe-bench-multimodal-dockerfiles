Hmmm, interesting. Do you know how to reproduce this issue in https://www.typescriptlang.org/play? This could well be a bug, I’m just trying to see the error somewhere. AFAIR, Prettier retains `<T,>` in `tsx` files to avoid confusion with `<JsxTags>`. We might need to apply the same rule to `mts` extension and maybe even some other ESM ones?
Hmm, looking around I can't... I don't know if you can set the file type to .mts in the TS Playground, because the issue does not happen with a `.ts` extension. Also, it doesn't seem to matter what any other settings concerning `"module": true` in the package.json or "module"/"moduleResolution" in the tsconfig. If it has a .mts extension it throws the error. I am surprised I hadn't found this issue mentioned much because .mts extensions have been supported since typescript 4.7.
@kachkaev TS doesn't introduce 'x' counterparts for .mts / .cts (they are just a kind of workaround), so it's impossible to detect JSX syntax by file extension. And TS team decided to make those files universal, with all existing .tsx restrictions.
mts/cts files don't actually support JSX syntax - instead TS just bans ambiguous syntax that would be disallowed if the file had JSX.

From the perspective of prettier - it should treat the file as a `.tsx` file.
I see. If Prettier formats all files (`.ts`, `.mts`, `.cts`) as `.tsx` (i.e. with `,`), what problems can this cause?
People will complain. 😄 
Maybe we should change this https://github.com/prettier/prettier/blob/78b0a6bb80b73553c1bfe5b003e51e7946086b35/src/language-js/print/type-parameters.js#L77-L80

to 

```diff
        getFunctionParameters(node).length === 1 &&
-       isTSXFile(options) &&
+       !isTsFile() &&
+       hasTrailingComma() &&
        !node[paramsKey][0].constraint &&
        path.parent.type === "ArrowFunctionExpression"
```
What if we replace `isTSXFile(options)` with `doesTsFileRequireTrailingCommasInGenerics(options)`? It will return `false` for `ts` but `true` for all others (`tsx`, `mts` and `cts`).
That's what I mean ` !isTsFile()`, but I want to do an additional check to make sure there was a trailing comma originally.
But maybe `<T,>` can write as `< T>` to omit comma? （I mean before format, user may do that, if possible.）
> but I want to do an additional check to make sure there was a trailing comma originally

It's a bit hard to exactly test this - but I believe that:
In a `tsx` file, `<T>() => {}` is a hard fatal TS parser error.
In a `mts`/`cts` file, the same code is a soft TS semantic error.

Which means if you check for a trailing comma and only insert it if it was there - you could format "broken" code to remain "broken". IDK if prettier specifically cares about that though.

> But maybe <T,> can write as < T> to omit comma?

You cannot - the TS parser ignores the leading space
> you could format "broken" code to remain "broken". 

I think we can accept that. Unless we can get an earlier error from parser. Is it possible to check such syntax in `@typescript-eslint/typescript-estree` if we pass the filename?
The main plan we had for our parser errors was really just to enforce that the AST doesn't violate the types we provide, and expose semantic errors where it is easy enough to do.

We hadn't thought about enforcing punctuator-level syntax with our errors.