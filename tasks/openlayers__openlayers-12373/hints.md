Maybe it is a feature request....
The template is effectively hardcoded into TileDebug, but you could create your own using XYZ and a custom tileLoadFunction to replace the src url with a dataUrl from a canvas https://codesandbox.io/s/simple-forked-37r37
I have also tried to add an property to the Tiledebug (dashY (true/false) to control this.

![image](https://user-images.githubusercontent.com/7397743/119868320-e5174980-beec-11eb-90de-b3fab72ca6e1.png)

Do you think it is better to  add a property or rely on a custom tileLoadFunction  ?

If there is to be a change to TileDebug it might be more flexible to call the tileUrlFunction to produce text based on either a default template or one specified in the constructor https://codesandbox.io/s/simple-forked-u3w0i