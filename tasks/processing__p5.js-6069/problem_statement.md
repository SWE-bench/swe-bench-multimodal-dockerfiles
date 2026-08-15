blendMode not working when doing point() drawing in webgl
### Most appropriate sub-area of p5.js?

- [ ] Accessibility
- [X] Color
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

### Steps:
1. Specify ADD blend using blendMode()
2. Draw a red point and a blue point so that they overlap using point()
3. The color of the overlapping part becomes the color of the point drawn later

### Snippet:

```js
function setup(){
  createCanvas(400,400,WEBGL);
  background(0);
  blendMode(ADD);
  strokeWeight(100);

  stroke(255,0,0);
  point(0,0,0);
  stroke(0,0,255);
  point(50,0,0);
}
```
Drawing result:
![pointBug2](https://user-images.githubusercontent.com/39549290/224692482-4f21d9f9-f473-4312-a79b-844ebfdc75af.png)

Expected result:
![pointBug](https://user-images.githubusercontent.com/39549290/224692573-a7465678-65ed-4264-ac33-d898b2cf784e.png)

### Suggestion for solution
It is probably because _applyColorBlend() is not executed in _drawPoints(), so I think that this one line should be added.

```javascript
_main.default.RendererGL.prototype._drawPoints = function (vertices, vertexBuffer) {
  var gl = this.GL;
  var pointShader = this._getImmediatePointShader();
  this._setPointUniforms(pointShader);
  this._bindBuffer(vertexBuffer, gl.ARRAY_BUFFER, this._vToNArray(vertices), Float32Array, gl.STATIC_DRAW);
  pointShader.enableAttrib(pointShader.attributes.aPosition, 3);

  this._applyColorBlend(this.curStrokeColor); // I think adding this line will fix the bug.

  gl.drawArrays(gl.Points, 0, vertices.length);
  pointShader.unbindShader();
};
```
