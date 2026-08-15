[This](https://github.com/GoogleChrome/lighthouse/blob/main/report/renderer/report-renderer.js#L147) is where the `Emulated Moto G4 with Lighthouse 9.6.8` string is built.

That depends on the [`deviceEmulation` value created here](https://github.com/GoogleChrome/lighthouse/blob/e3f2337d73b7b9e6a9ff01b85cd0750e8e10e86a/report/renderer/util.js#L515-L518).

I don't believe`settings.formFactor` can be null, it must either be `mobile` or `desktop`, at least when invoking the option with the CLI. So seems like a bug?
I found a couple confusing things going on here:
- `settings.formFactor` represents how the report is scored, not what device is being used. However the report seems to indicate that `settings.formFactor` reflects the emulated device.
- The string will say "Emulated Moto G4" for *any* settings with mobile form factor, even if a different mobile device is being emulated or a real device is being used.

We could use `settings.screenEmulation` to determine this string and then generalize the mobile version so it's not specific to the Moto G4. Ex "Emulated Mobile Device with Lighthouse 9.6.8."

Another option would be to reword the strings like "Score based on Moto G4 with Lighthouse 9.6.8" and leave the `settings.formFactor` logic in place.

This was discussed previously (and @paulirish explored it in #11796). 

I'd opt to leave `formFactor` as is and update the mobile descriptor to be more generic (i.e.: Not mention a specific device, because people get hung up on that anyway). 