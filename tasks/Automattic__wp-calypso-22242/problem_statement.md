Jetpack Connect: Recognize and try to handle site URLs with /wp-admin appended


#### Steps to reproduce
1. Starting at URL: https://wordpress.com/jetpack/connect
2. Enter the URL of a self-hosted site's WP Admin dashboard
3. Note that the next step is "Ready for installation" even if Jetpack is installed and activated on the site.
4. Click "Install Jetpack."

#### What I expected

I expected Jetpack Connect to detect that I was entering the URL for my site's WP Admin dashboard and either handle that case correctly or warn me that I was entering the wrong URL.

#### What happened instead

Jetpack Connect asked to install Jetpack (even though it was already installed/activated) and then sent me to `/wp-admin/wp-admin/plugin-install.php?tab=plugin-information&plugin=jetpack&calypso_env=stage` (note the double `/wp-admin`) which resulted in a 404 error on my site.

#### Browser / OS version

Chrome 64 / macOS 10.13.3


#### Screenshot / Video

![screenshot 2018-02-07 14 13 42](https://user-images.githubusercontent.com/8658164/35920944-3ccf80d0-0c11-11e8-94e6-01fb41274819.png)

#### Context / Source
#manual-testing #flow-mapping






