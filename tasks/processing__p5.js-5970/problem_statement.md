On my android phone sometimes objects in sketches drawn with webgl in p5.js disappear
### Most appropriate sub-area of p5.js?

- [ ] Accessibility
- [ ] Color
- [X] Core/Environment/Rendering
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

1.5.0

### Web browser and version

Chrome

### Operating System

Android 12

### Steps to reproduce this

### Steps:
1. First, draw a textured triangle with p5.js webgl.
2. Then use p5.Geometry to draw an untextured square with lighting enabled.
3. However, when I view this sketch on my Android smartphone, this square is not drawn.

### Snippet:

```js
function setup() {
  createCanvas(400, 400, WEBGL);
  const geom = new p5.Geometry();
  geom.vertices.push(
    createVector(-100,-100), createVector(100,-100),
    createVector(100,100), createVector(-100,100)
  );
  geom.faces.push([0,1,2],[0,2,3]);
  geom.computeNormals();
  this._renderer.createBuffers("myPlane", geom);
  
  const gr = createGraphics(100,100);
  gr.background(255);

  background(0);
  texture(gr);
  triangle(-200,-200,0,-200,0,0);

  directionalLight(255,255,255,0,0,-1);
  ambientLight(64);
  ambientMaterial(255);
  fill(0,0,255);
  this._renderer.drawBuffers("myPlane");
}
```
![bugbug2](https://user-images.githubusercontent.com/39549290/213927281-3d1c54a5-7f16-464a-a205-a70074609e25.png)
In order to investigate this phenomenon, various experiments were performed, such as overwriting the drawBuffers function. As a result, it turned out that the cause was in the register.

First, the textured triangle and the square we draw afterward use the same shader.
When you draw a textured triangle, the UV information is stored in registers reserved for textures by the lightingShader. It is data for 3 vertices.
After that, the square created by p5.Geometry is drawn, but since the texture register remains valid at that time, the previous data is used as it is.
Since there are only 3 vertices in the data, it is insufficient to give a square with 4 vertices. This is unusual.
But it's not used for drawing, so it doesn't matter what it contains. At that time, most environments seem to handle the lack of data by filling it with 0 (probably) to prevent problems from occurring.

However, in some environments like my Android, it seems that the lack of data is recognized as abnormal and it does not draw.

Of course, it may occur because the data is not properly prepared, and it can be considered that the person writing the code is bad. However, if you don't assume drawing with textures like this, you'll have to write unnatural code to avoid this. I don't think that's a very good thing.

Problems like this occur with Shaders where not all attributes are used, such as lightingShader. Until 1.5.0, it was possible only with lightingShader, but in the next version, a new attribute called aVertexColor will be implemented. This increases the number of drawing options and makes problems like this even more likely.

Therefore, I would like to propose to disable registers for unused attributes with the disable instruction so that such problems do not occur.

## solution I think

First, let RendererGL have an array that stores flags for whether registers are enabled (For example, with a name like registerEnabled).
```javascript
this.registerEnabled = [];
```
Then set this flag in the enableAttrib function. Use the location number as an argument.
```javascript
if (!attr.enabled) {
  gl.enableVertexAttribArray(loc);
  this._renderer.registerEnabled[loc] = true; // Record register enabled state
  attr.enabled = true;
}
```

Finally, in the _prepareBuffer function, if the if branch is not for an attribute whose length is 0, if the register reserved for that attribute by the shader is enabled, disable it Add processing to make:
```javascript
if (src.length > 0) {
  /* ~~~~~~~~~~~~~~~~~~~~ */
} else {
  // Do nothing if register is not enabled
  const loc = attr.location;
  if (loc == -1 || !this._renderer.registerEnabled[loc]) { return; }
  // If enabled, disable it.
  gl.disableVertexAttribArray(loc);
  attr.enabled = false;
  this._renderer.registerEnabled[loc] = false; // Record register enabled state
}
```
It has been confirmed that the above-mentioned problems can be avoided by this specification change.
However, _prepareBuffer is an important function that affects the entire drawing process, so I can't decide on my own whether or not such a change should be made. So I will wait for the review.
