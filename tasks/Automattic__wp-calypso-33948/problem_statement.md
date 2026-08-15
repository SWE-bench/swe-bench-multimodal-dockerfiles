localForage uses an Apache 2.0 license, which is incompatible with GPL v2
It looks like localForage, which is in use by WordPress.com/Calypso, isn't actually compatible with the GPLv2 license in use by WordPress.com. I encountered this working on Gutenberg, which is also GPLv2 or later, and runs a script to ensure dependency compatibility:

<img width="707" alt="screenshot 2018-11-20 at 16 55 46" src="https://user-images.githubusercontent.com/90871/48789508-222f6f00-ece5-11e8-9246-c29e957a492c.png">

I'm noting this here to track the issue in WP.com. As the maintainer of localForage, it's possible an easy solution would be to relicense/dual license the next major version of localForage, which I'm not really opposed to doing. But I wanted to log this here so it could be tracked.
