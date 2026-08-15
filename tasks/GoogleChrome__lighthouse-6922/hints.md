Great question and nice research @oddui! You are correct, Lighthouse does not handle out-of-process-iframes properly yet, but it's on our plate for this quarter.

@paulirish you mentioned dgozman was working on something to make target juggling easier, is that finished and I should get started on this?
@patrickhulce that's great to hear.

Can I ask why you specifically say **out-of-process-iframes**? Are there any in-process-iframes?

The reason I ask is that sometimes I do seem to get requests from iframes by just sending `Network.enable` to a target, using the chrome-remote-interface library. However I don't get those requests from iframes using the chrome extension debugger API. 😕 
You can [read a little more](https://www.chromium.org/developers/design-documents/site-isolation) about [OOPIFs](https://www.chromium.org/developers/design-documents/oop-iframes) if you're curious, but basically cross-origin frames have been slowly moved to their own separate processes distinct from the main frame's process (site isolation). A couple of wins from this are isolating performance from misbehaving frames and security benefits to mitigate spectre-style attacks.

When the frames were all in the same process, we got all the network information just by listening to the main target/process. Now that they are separate processes we need to be listening to all the targets to get all the network information. AFAIK, we should still be getting information from frames that aren't OOP.
@patrickhulce i spoke with dgozman and he said it's not ready yet. Currently the Browser domain is flattened, but Page is still in progress. ~4w from now we can check in again.

Here's the implementation issue: https://bugs.chromium.org/p/chromium/issues/detail?id=775132
update: dgozman sez the implementation is good enough for us to use the new flattened target mgmt.

He does note the structure of service worker targets will change soon, though.