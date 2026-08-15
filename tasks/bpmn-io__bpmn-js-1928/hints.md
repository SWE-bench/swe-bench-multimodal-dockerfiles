Hi, can I get assigned to this issue, Thanks

@MaverickDe If you're interested go ahead and file a PR.
Hi, can I get assigned to this issue, Thanks

@jyzib You don't need to be assigned. If you want to contribute, please open a PR that fixes this issue (or attempts a fix).
I have a fix ready for the space-tool behavior, but I wonder if it _generally_ should be impossible to resize an empty pool vertically.

The bug description by @nikku says:

> An empty pool has a dedicated, fixed height shape to distinguish it from lanes / expanded pools. Using the space tool it gets resized however:

Maybe I am misunderstanding this, but should the following be possible or not?

![emptypool](https://github.com/bpmn-io/bpmn-js/assets/27265759/4b970d48-442e-4f41-bff6-b1e25117eadf)

@hkupitz That is an interesting question. I'd argue: A default size empty pool makes it simpler to recognize it and not confuse it with a lane. So :+1: from my side.
On the other hand making something not resizable is a bold move; we may not be aware of all scenarios, and we may not be ready for on-direction resizing either, nor won't be our users. I.e. I don't know this to be a thing from a drawing tool.

So let's decouple this fix from the general "should be resizable" discussion. In terms of resizing we are well covered; essentially we want empty pools to behave like text annotations; these do not resize either (in any direction):

![capture 74IzGE_optimized](https://github.com/bpmn-io/bpmn-js/assets/58601/ef5a35d1-5fb7-4fa1-90df-e3711fb3c624)

I think using the spacing tool along the x-axis should be allowed as empty pools quite often stretch along another accompanied pools:

![spacetool_yaxis_disabled](https://github.com/bpmn-io/bpmn-js/assets/27265759/5c7ef6b5-c2f1-43b4-9cb5-8ab43a1ec256)

When disabling both axes, this leads to - in my opinion - unexpected behavior:

![spacetool_fully_disabled](https://github.com/bpmn-io/bpmn-js/assets/27265759/6cf0036a-3020-4781-a6f2-32c767222cb6)

What do you think, @nikku?
100% agreed.