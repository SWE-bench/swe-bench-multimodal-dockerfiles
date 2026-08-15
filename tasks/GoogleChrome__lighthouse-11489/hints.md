Thanks for filing @acutmore! I agree when the granularity is set to tenths all numbers should be displayed to the tenth 👍 
> I am happy to make the necessarily changes if the feature is agreeable with the team

Sounds good, thanks! Let us know if you need any help.

The relevant code is various functions within https://github.com/GoogleChrome/lighthouse/blob/ec69e56f06b61932712db239c3db1804d260a16a/lighthouse-core/report/html/renderer/i18n.js 

NumberFormatter apparently accepts a minimum significant digits: https://tc39.es/ecma402/#conformance
thanks @patrickhulce and @connorjclark. I'll have a go at making the change within the next few days.
also, Math.log10 will be your friend :) 
![image](https://user-images.githubusercontent.com/4071474/93132632-9e096100-f69b-11ea-8737-09e04b88e0b1.png)
