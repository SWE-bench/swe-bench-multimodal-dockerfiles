It does seem like the behavior might have changed between versions. It would be helpful if you minimize  the code to isolate what's causing the issue.

Can you please be more specific about what's not being calculated correctly?

The workaround is to use `maxTicksLimit: 3`
Here's an example: https://jsfiddle.net/37eyrsh2/
The issue is too many labels are being generated, see this jsfiddle where I've lowered the height of the wrapping div but the labels then overlap each other: https://jsfiddle.net/sv2autz6/1/

I can see the `maxTicksLimit:3` could work here, however we've got around 40 charts of different sizes and we're displaying financial data which could vary from thousands to billions.

I've changed the code example to have the bare minimum data that causes this issue
Another workaround is to use `autoSkipPadding`:  https://jsfiddle.net/vy8kf3ps/