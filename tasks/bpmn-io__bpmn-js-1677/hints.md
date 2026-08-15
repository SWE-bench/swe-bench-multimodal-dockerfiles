This was first seen in the most recent `demo.bpmn.io` deployment. It may be a regression in one of the releases since the Heroku incident.
I am still able to reproduce it. It seems the fix works only for empty text box, but when you type anything, delete action leads to an error as previously.

https://user-images.githubusercontent.com/28307541/172607481-0c0e1600-6e1b-4896-af79-d5fcd423907d.mov

I'll look into this.