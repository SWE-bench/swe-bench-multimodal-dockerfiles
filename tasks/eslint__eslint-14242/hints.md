It looks like there is probably a bug when quiet and max-warnings are used together. In that case, it should still exit with a 1 exit code saying that there were too many warnings.

I think it makes sense to not show warnings in this case.
> It looks like there is probably a bug when quiet and max-warnings are used together. In that case, it should still exit with a 1 exit code saying that there were too many warnings.

I agree that `--max-warnings` indicates that the user wants a non-zero exit code when there are too many warnings, even with `--quiet`. Otherwise, this combination wouldn't make sense, and if a non-zero exit code isn't desired behavior then they can just remove `--max-warnings` from the command.

> I think it makes sense to not show warnings in this case.

I don't have a strong opinion on this. Not showing warnings looks less surprising, but the list of warnings might be valuable in this case. 

I agree that this is a bug and that `--max-warnings` should trigger a non-zero exit code when the limit is exceeded even if used with `--quiet`.

> I think it makes sense to not show warnings in this case.

I also agree that this is the correct behavior because we should respect `--quiet` and not show warnings even if `--max-warnings` is exceeded.
Okay, so it sounds like we've agreed that the current behavior is a bug.

Current behavior: When using `--quiet` with `--max-warnings`, we are not showing an error even when the number of warnings exceeds the threshold for errors.

Desired behavior: When using `--quiet` with `--max-warnings`, we should show the error that the maximum number of warnings has been reached and not show the actual warnings.
Should we show the number of found warnings in the message?

Current message is: `ESLint found too many warnings (maximum: 100).`

https://github.com/eslint/eslint/blob/ebd70263f6e6fe597613d90f4b8de84710c2f3d6/lib/cli.js#L315-L318

Without `--quiet`, formatter is expected to show the number of warnings.

With `--quiet`, formatter will show either nothing or, if it's a formatter that always show a summary, something like `warnings: 0`.
I don’t think that’s necessary. The max allowable warnings is already shown so I don’t think there’s any need to show the actual number  