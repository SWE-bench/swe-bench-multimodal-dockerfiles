Reader: rename showEmailSettings to showNotificationSettings
Renames the prop `showEmailSettings` to `showNotificationSettings` to reflect the fact that the popover now deals with new post notifications _and_ email notification settings (see https://github.com/Automattic/wp-calypso/pull/20824).

<img width="286" alt="33993970-aa3dba40-e0d0-11e7-85d0-ce073095b506" src="https://user-images.githubusercontent.com/17325/34728766-ae1c4992-f552-11e7-9f13-13a2314655d2.png">

### To test

In http://calypso.localhost:3000/following/manage, ensure that the recommended sites under the search box do not have a 'Settings' link, even if you're following one of them:

![screen shot 2018-01-09 at 15 27 36](https://user-images.githubusercontent.com/17325/34728795-c63610b2-f552-11e7-9bf0-5fa45c7c8ae7.png)

