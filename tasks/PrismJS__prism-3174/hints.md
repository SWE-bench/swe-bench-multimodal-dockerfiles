Good find!

Would you like to make a PR @AvdLee?
@RunDevelopment normally I wouldn't even open this issue since it's only one keyword, though, since this is in the method body I wasn't sure how to solve this. It's not like simply adding an extra keyword since this keyword is already in the list of recognised keywords.

It should work like `inout` which is also placed in front:

```swift
func doubleInPlace(number: inout Int) {
    number *= 2
}
```

We do seem to support that variant, so I wonder why the `isolated` isn't working in this case 🤔 

> It's not like simply adding an extra keyword since this keyword is already in the list of recognised keywords.

No, it's just that easy because it's not in that list, only `nonisolated` is.
> No, it's just that easy because it's not in that list, only nonisolated is.

I did not realise that! Let me open a PR 🚀 