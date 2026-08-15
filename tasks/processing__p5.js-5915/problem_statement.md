To color the colors of the curves vertex-wise so that they are interpolated.
### Increasing Access

From beginShape to endShape, if you call the fill function just before calling the vertex function, you can give each vertex a different color.
```javascript
function setup() {
  createCanvas(400, 400, WEBGL);
  beginShape();
  fill(255);
  vertex(0,0,0);
  fill(0,0,255);
  vertex(100,0,0);
  fill(255,0,0);
  vertex(0,100,0);
  endShape();
}
```
![lineColor_0](https://user-images.githubusercontent.com/39549290/209168825-373f404d-216c-45d2-9b6e-4c632a42c1a8.png)

However, stroke does not do this kind of interpolation. By design, only information from the last call to the stroke function is accepted.
```javascript
function setup() {
  createCanvas(400, 400, WEBGL);
  strokeWeight(2);
  noFill();
  beginShape();
  stroke(255);
  vertex(0,0,0);
  stroke(0,0,255);
  vertex(100,0,0);
  stroke(255,0,0);
  vertex(0,100,0);
  stroke(255);
  vertex(0,0,0);
  endShape();
}
```
![lineColor_1](https://user-images.githubusercontent.com/39549290/209169526-55a8712b-ec32-4401-9353-da867f5a974b.png)

What we want to do is store information about the line color in the vertex each time we call the stroke function, and interpolate the line color as well.
Expect output like this:
![lineColor_3](https://user-images.githubusercontent.com/39549290/209170179-95220ff8-4976-4c7d-9651-3b6e736c22d8.png)


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

### Feature request details

First, modify the vertexShader so that it can receive the line color for each vertex as an attribute variable, and prepare a new varying variable to send it to the fragmentShader.

In fragmentShader, prepare a flag to decide whether to decide the color for each vertex or apply the same color to all as before, and branch the processing.

Next, define the flags used in the fragmentShader when constructing Renderer.GL, and prepare a new p5.Renderbuffer corresponding to the attribute variable used in the vertexShader (retained, immediate, each prepared).

```javascript
new _main.default.RenderBuffer(4, 'lineVertexColors', 'lineColorBuffer', 'aVertexColor', this, this._flatten),
```

We also make p5.Geometry have a new array that stores the color information used to color the lines. The flag to color each vertex should be determined by whether color information is stored in this array.

```javascript
this.lineVertexColors = [];
```

Finally, in p5.Geometry's _edgesToVertices function, where we create the array of vertices for line drawing, we complete the array where the per-vertex color is stored. This is easily constructed by ordering the corresponding color information in the same order as the vertices.

```javascript
_main.default.Geometry.prototype._edgesToVertices = function () {
  const data = this.lineVertexColors.slice();
  this.lineVertexColors.length = 0;
  /* ------- */
  for (var i = 0; i < this.edges.length; i++) {
    const e0 = this.edges[i][0];
    const e1 = this.edges[i][1];
    /* ------- */
    if(data.length > 0){
      var beginColor = [data[4*e0], data[4*e0+1], data[4*e0+2], data[4*e0+3]];
      var endColor = [data[4*e1], data[4*e1+1], data[4*e1+2], data[4*e1+3]];
      this.lineVertexColors.push(beginColor, beginColor, endColor, endColor, beginColor, endColor);
    }
  }
```
