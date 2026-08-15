I think it is because the default intervals are not well suited to the default format

for DMS instead of  `0.5, 0.2, 0.1, 0.05, 0.01, 0.005, 0.002, 0.001`

intervals such as

`30/60, 20/60, 10/60, 5/60, 2/60, 1/60, 30/3600, 20/3600, 10/3600, 5/3600, 2/3600, 1/3600`

would be more suitable


However, the problem still persists

![image](https://user-images.githubusercontent.com/49240900/181242169-82d0bf0a-68e0-43a4-8d43-0378b1c11a68.png)

Or should `ceil` be `round` here? https://github.com/openlayers/openlayers/blob/main/src/ol/coordinate.js#L171

That works https://29r9yf.csb.app/

The default intervals 0.002, 0.001 are fractions of a second and should not be used with DMS format
That works https://29r9yf.csb.app/   yes !!  That seems works well ! 
Mays be is to much to ask but when we have rounded value why keep the subunits it will be more clear no ??
<img width="1119" alt="Capture d’écran 2022-07-27 à 20 00 08" src="https://user-images.githubusercontent.com/328101/181341244-c26a0389-14a3-45f3-b8a5-2ae531b60cb1.png">

