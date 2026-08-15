webgl: render buffers are not not always created correctly
0.8.0 webgl.

(from #3764)

the issue is that when creating a retained-mode geometry (any geometry, not just the glyph quad), it's checking the _current_ fill and stroke shaders for which buffers to create and which attributes to enable.

https://github.com/processing/p5.js/blob/6640d149348dea0a1b3df61f0cf8442222403a9f/src/webgl/p5.RendererGL.Retained.js#L171-L172

this means that if you choose a shader that doesn't have a particular attribute, then create a (cached) geometry, that geometry won't have a buffer created for it that corresponds to that attribute. then, if you switch the current shader to one that _does_ have that attribute, it will fail to render because that buffer won't have been created.

repro, here: https://codepen.io/Spongman/pen/ZNoZoM?editors=0010

this test case creates and uses a shader that doesn't have a full suite of attributes. it then draws a sphere (in the `setup()` function). the sphere's geometry is created & cached. the bug is that the render buffers are also created at this time, and they're only created if the _current_ shader has the corresponding attribute. subsequently, when a regular fill shader is used to render the sphere (in the `draw()` function), the required render buffers are missing, and the sphere is drawn incorrectly, or not at all (probably depending on the webgl implementation):

![image](https://user-images.githubusercontent.com/1088194/58386210-0f0d9c80-7fb1-11e9-96db-0734d8bdcf3a.png)


```javascript
var sh;

function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL);
  
  sh = createShader(
    'attribute vec3 aPosition; void main() { gl_Position = vec4(aPosition, 1.0); }',
    'void main() { gl_FragColor = vec4(1.0,1.0,1.0,1.0); }'
  );
  
  shader(sh);
  noStroke();
  sphere(200);
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}

function draw() {
  background(0);
  
  // draw an orange sphere
  fill(255, 128, 0);
  directionalLight(255, 255, 255, 1, 1, -1);
  sphere(200);
}
```


