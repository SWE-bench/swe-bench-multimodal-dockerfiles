Vertex ordering for beginShape(QUADS) is different in WebGL from 2D mode
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

Commit c9fb107 on main

### Web browser and version

Firefox 103.0.2

### Operating System

MacOS

### Steps to reproduce this

### Steps:

Quads rendered with `beginShape(QUADS)` that look like rectangles in 2D mode end up with self-intersections in WebGL mode. This is because it currently treats the vertex ordering the same way `QUAD_STRIP` does, which does one side after the other in the same order, rather than going around one quad in a consistent CW or CCW direction.

### Snippet:

With the following code:

```js
function setup() {
  createCanvas(256, 256, WEBGL);
}
function draw() {
  background(240);
  stroke(0);
  fill(255, 0, 0)
  beginShape(QUADS);
  vertex(-25, -25, 0);
  vertex(25, -25, 0);
  vertex(25, 25, 0);
  vertex(-25, 25, 0);
  endShape(CLOSE);
}
```

the resulting shape looks different when you change the environment:

<table>
<tr>
<td>
<img src="https://user-images.githubusercontent.com/5315059/187053713-e8562d29-3958-4b5a-8c3a-c7b3fd091910.png">
</td>
<td>
<img src="https://user-images.githubusercontent.com/5315059/187053706-c374deb2-22ae-4e81-b27c-d3ee66dd3452.png">
</td>
</tr>
<tr>
<th><em>2D</em></th><th><em>WebGL</em></th>
</tr>
</table>



