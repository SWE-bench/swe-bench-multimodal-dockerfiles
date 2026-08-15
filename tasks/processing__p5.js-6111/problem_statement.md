About the problem that ortho() and frustum() cannot set near/farclip and other small bugs
### Most appropriate sub-area of p5.js?

- [ ] Accessibility
- [ ] Color
- [ ] Core/Environment/Rendering
- [ ] Data
- [ ] DOM
- [ ] Events
- [ ] Image
- [ ] IO
- [ ] Math
- [ ] Typography
- [ ] Utilities
- [X] WebGL
- [ ] Build Process
- [ ] Unit Testing
- [ ] Internalization
- [ ] Friendly Errors
- [ ] Other (specify if possible)

### p5.js version

1.6.0

### Web browser and version

Chrome

### Operating System

Windows11

### Steps to reproduce this

## Steps:
1. Set near and far to -400 and 400 with ortho().
2. Using console.log(), access the camera with this._renderer._curCamera and output cameraNear and cameraFar.
3. It outputs the default camera values ​​instead of -400 and 400.

## Snippet:

```js
function setup() {
  createCanvas(400, 400, WEBGL);
  ortho(-200, 200, -200, 200, -400, 400);
  const cam = this._renderer._curCamera;
  
  console.log(cam.cameraNear);
  console.log(cam.cameraFar);
}
```
## result
![nearとfarが正しくない](https://user-images.githubusercontent.com/39549290/232802867-1afecea7-0462-4214-a3d3-b99cece25621.png)


Something similar is happening with frustum:
![nearとfarが正しくない2](https://user-images.githubusercontent.com/39549290/232803488-f712a22a-f47c-4e12-ad57-00b00578c45a.png)

## other small bugs
First, frustum() defaults to something close to ortho(), but frustum() behaves more like perspective(), so it should default to that. If you call it normally without arguments, the object will disappear.

```js
if (left === undefined) left = - this._renderer.width / 2;
if (right === undefined) right = + this._renderer.width / 2;
if (bottom === undefined) bottom = - this._renderer.height / 2;
if (top === undefined) top = + this._renderer.height / 2;
if (near === undefined) near = 0;
if (far === undefined) far = Math.max(this._renderer.width, this._renderer.height);
```
![frustumでは消えてしまう](https://user-images.githubusercontent.com/39549290/232804546-a972431b-745a-41bd-a4c7-2c468cea7e02.png)

In addition, when correcting, it is necessary to reverse the sign only at y in the matrix component calculation. Otherwise the vertical direction will be reversed.
![yの向きが逆ですよ](https://user-images.githubusercontent.com/39549290/232805390-09d84183-fd08-4b01-a74c-0b9a1d9a9f07.png)

In addition, I would like to solve the problem that the vertical rotation direction is reversed when the 3rd and 4th arguments of ortho() and frustum() are reversed.
This has been verified and is caused by the determinant of the projection matrix being negative, so multiplying by the sign eliminates it. I will fix this as well.

https://user-images.githubusercontent.com/39549290/232807717-8b1dfde2-ff46-443d-94c7-7802bc719c35.mp4


