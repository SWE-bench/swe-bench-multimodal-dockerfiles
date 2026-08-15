This is happening for me with `Text` that is not empty as well, FYI. Removing the `height` style fixes the issue it seems.
I am seeing this bug after upgrading to react 17, then having to reinstall @react-pdf/renderer with the option `--legacy-peer-deps`.  (Just mentioning as that's the only thing that has changed).

I use `height` style on quite a few places, but you're right removing those does avoid this error. Thanks for mentioning - I think I need the height though really.