It looks like the `near` and `far` parameters to `ortho` are being used correctly in the perspective matrix, so the clipping planes are being set correctly for rendering, but it just isn't setting the camera's `cameraNear` and `cameraFar` properties. Thankfully that means we probably just need to add some lines like `this.cameraNear = near` to fix it!

> First, frustum() defaults to something close to ortho(), but frustum() behaves more like perspective(), so it should default to that. If you call it normally without arguments, the object will disappear.

I think that makes sense, maybe we can default to values that match the `perspective()` camera?

> In addition, when correcting, it is necessary to reverse the sign only at y in the matrix component calculation. Otherwise the vertical direction will be reversed.

I think for `frustum` it's actually correct but for `ortho` it's not: in your example, you have -20 as `bottom` and `20` as `top` (the `bottom` param comes first according to the docs), leading to the camera being flipped vertically. (`ortho` does the opposite, so definitely one of them should be changed!)

That said, do you think in both `ortho` and `frustum`, we should change the parameter order to be `top, bottom` instead of `bottom, top`? Right now the formula we use [is the same as the one on Wikipedia](https://en.wikipedia.org/wiki/Orthographic_projection#Geometry), but that assumes up is positive, where in p5 it's negative. Changing it might reduce confusion so that we consistently go in order of smallest-to-largest in the x, y, and z axes.

> In addition, I would like to solve the problem that the vertical rotation direction is reversed when the 3rd and 4th arguments of ortho() and frustum() are reversed.

I'm on the fence about whether this should be considered intentional behaviour or not. It definitely is confusing, but I wonder if changing the parameter order to be consistent will do enough to reduce the confusion?
Thanks for reply! Here is sample code: [fix_ortho_frustum](https://editor.p5js.org/dark_fox/sketches/YXKR_M1mr)

I dealt with near and far by adding two lines each. The frustum defaults now match the default camera. At that time, the order of signs was changed to -+-+.
But doing so would reverse the direction of the y-axis. Whether or not this should be fixed seems debatable. I don't know much about it because not many people use it. It's easy to fix by just reversing the sign of some variables.
It's the same for me, but it's hard to think about things like bottom and top in my head. It's easier mentally to think that -+-+ is fine, so I think it's easier to use if the direction of the axes is kept in the same order.

Regarding the direction of rotation, for example, when dropping a model from blender, you may want to reverse the direction of the y-axis. Only frustum() and ortho() can do that. At that time, it would be difficult to intuitively understand if the direction of rotation was reversed, so I thought it would be better to rotate in the same direction.

sample code: [model_download_test](https://editor.p5js.org/dark_fox/sketches/RBRuCiMWL)
If you don't reverse the y-axis in frustum, it will look something like this: (forward:Y, up:Z)
![向きが逆です](https://user-images.githubusercontent.com/39549290/232944656-3103dedd-bb69-471d-adeb-35cb053c30bc.png)
Whereas in blender it looks like this:
![このモデル](https://user-images.githubusercontent.com/39549290/232944723-1d69cff7-d51f-465e-aad2-886fd3fc67bd.png)
I thought that it would be easier to understand the operation if the direction of rotation when dragging the mouse vertically was the same.
> But doing so would reverse the direction of the y-axis. Whether or not this should be fixed seems debatable. I don't know much about it because not many people use it. It's easy to fix by just reversing the sign of some variables.

True, I guess by making `ortho` and `frustum` consistent, one of them will have to be a breaking change. I think the fixing the current inconsistency is probably more important than maintaining backwards compatibility here.

> Regarding the direction of rotation, for example, when dropping a model from blender, you may want to reverse the direction of the y-axis. Only frustum() and ortho() can do that. At that time, it would be difficult to intuitively understand if the direction of rotation was reversed, so I thought it would be better to rotate in the same direction.

That's a good point, I suppose the best experience for people would be to not use frustum() and ortho() to flip and instead use scale() so that camera control is unaffected. Sounds good then!
I see. I would like to make some additional comments on this matter.

First of all, I wanted to set cameraNear and cameraFar because I needed to use them in the zooming method that you merged earlier. In fact, this value is almost never used, so there was no problem until now, but I decided to fix it because it would be bad if it was not used for zooming.

I'm going to modify the default value of frustum() to:
```js
  if (left === undefined) left = -this._renderer.width * 0.05;
  if (right === undefined) right = +this._renderer.width * 0.05;
  if (bottom === undefined) bottom = -this._renderer.height * 0.05;
  if (top === undefined) top = +this._renderer.height * 0.05;
  if (near === undefined) near = this.defaultCameraNear;
  if (far === undefined) far = this.defaultCameraFar;
```
This is because the object will be lost if it is called without arguments (I don't know if there is such a chance...).

Also, between ortho() and frustum(), I think it is appropriate to change the sign of frustum(). In fact, the corresponding y component of the projection matrix is ​​y instead of -y only in frustum(). I don't know what the intention is with this, but I think it's better to be consistent.

Finally, regarding the direction of rotation, you can set SensitivityY to -1, so
I thought it would be up to the user to decide. So I will pass it on.
I would like to create a pull request with the above content.
> Also, between ortho() and frustum(), I think it is appropriate to change the sign of frustum(). In fact, the corresponding y component of the projection matrix is ​​y instead of -y only in frustum(). I don't know what the intention is with this, but I think it's better to be consistent.

Just to clarify, this would be to make camera rotation not be backwards any more for frustum() when passing in values with the pattern `low, high, low, high, low, high` right? My comment before about frustum() technically being correct is only because of the ordering of `bottom` coming before `top` in the parameters. Flipping the sign makes sense if we also switch the names of the parameters. That would mean changing the parameters list and having these lines too, I think:
```js
if (bottom === undefined) bottom = this._renderer.height * 0.05; // used to be negative, now positive
if (top === undefined) top = -this._renderer.height * 0.05; // used to be positive, now negative
```
...which hopefully will make more sense to other maintainers reading the code (bottom being larger than top.)

> Finally, regarding the direction of rotation, you can set SensitivityY to -1, so I thought it would be up to the user to decide. 

Sounds good, we can have a consistent behaviour across all camera modes, and then users can change it if they want using the sensitivity parameters.

> I would like to create a pull request with the above content.

Thanks! I'll assign this to you.
Ok, I'd like to change the default sign like so.

I have one more suggestion. Regarding the scale conversion of ortho(), I added the code to change the matrix elements as follows:

```js
const uP = this._renderer.uPMatrix.mat4;

if (this._mouseWheelDeltaY !== 0) {
  // zoom according to direction of mouseWheelDeltaY rather than value
  const mouseWheelSign = (this._mouseWheelDeltaY > 0 ? 1 : -1);
  const deltaRadius = mouseWheelSign * sensitivityZ * zoomScaleFactor;
  this._renderer._curCamera._orbit(0, 0, deltaRadius);
  // if ortho, scale change.
  if (uP[15] !== 0) {
    uP[0] *= Math.pow(10, -deltaRadius);
    uP[5] *= Math.pow(10, -deltaRadius);
  }
  /*
  if (this._mouseWheelDeltaY > 0) {
    this._renderer._curCamera._orbit(0, 0, sensitivityZ * zoomScaleFactor);
  } else {
    this._renderer._curCamera._orbit(0, 0, - sensitivityZ * zoomScaleFactor);
  }
  */
}
this._mouseWheelDeltaY = 0;
```
Then, it became possible to change the size naturally as follows. (I'll fix the translation of camera in the future...)

https://user-images.githubusercontent.com/39549290/233231189-6c7d337c-0ddf-4bd1-b0d0-e630b4374c6d.mp4

So I would like to change this as well. In terms of changing ortho(), I don't think it's out of scope...
Nice, this looks good!