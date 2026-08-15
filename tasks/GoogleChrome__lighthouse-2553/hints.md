Hey ! Can I try helping out with this ? I'm new to contributing to projects , so if you could guide me through my first project, I'd appreciate it ! 
@TheAlbinoPanda sure

to start you can look at these docs:

https://github.com/GoogleChrome/lighthouse/blob/556b9b72e729f444bb7ba59aa567d53cd11749da/readme.md
https://github.com/GoogleChrome/lighthouse/blob/556b9b72e729f444bb7ba59aa567d53cd11749da/CONTRIBUTING.md
https://github.com/GoogleChrome/lighthouse/blob/556b9b72e729f444bb7ba59aa567d53cd11749da/docs/architecture.md

you should fork the repo to your user account, then clone locally and get a build up and running with the CLI. and then you can note the numbers in the HTML report (and the "pretty" CLI output) that need to change.. and then adapt the various "formatters" to use toLocaleString as appropriate.

Once you have things looking correct locally you can push a branch to your github repo. and initiate a pull request so we can have a look.
Awesome thank you @paulirish. I'll start working on this tonight !