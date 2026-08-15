Default WebGL premultipliedAlpha to true?
### Increasing Access

Ideally, this would be to let WebGL sketches have an alpha channel by default, same as in 2D mode. We've received a couple GitHub issues (https://github.com/processing/p5.js/issues/5634, https://github.com/processing/p5.js/issues/5890) and a some Discord questions from people not realizing that it was an intentional change, so those people would be less confused. The change was originally made because blending and transparency was working in unexpected ways, but this might help fix that too.

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

### Feature request details

We made the switch after this issue https://github.com/processing/p5.js/issues/5552, which mentions some other issues motivating the change. I think those original issues could be resolved by using premultiplied alpha everywhere:

## https://github.com/processing/p5.js/issues/5195: Antialiasing on transparent regions blend with the background color

The example in the issue creates a box on a transparent background, and the antialiased parts (which would have semitransparent pixels) end up getting tinted towards the RGB value of the background color (ignoring the background's alpha.) This seems to be fixed by enabling premultipliedAlpha:

<table>
<tr>
<td rowspan="2">

```js
function setup() {
  createCanvas(400, 400, WEBGL);
  pixelDensity(2);
  setAttributes({
    alpha: true,
    premultipliedAlpha: true
  });
  noFill();
  stroke(200, 200, 255);
  strokeWeight(1);
}
function draw() {
  // black w/ alpha zero
  background(0, 0, 0, 0);
  scale(4);
  box();
  noLoop();
}
```
</td>
<th>premultipliedAlpha: false</th><th>premultipliedAlpha: true</th>
</tr>
<tr>
<td>
<img src="https://user-images.githubusercontent.com/5315059/206325019-7879028e-85f1-4de3-81bb-896e06fd53ab.png" />
</td><td>
<img src="https://user-images.githubusercontent.com/5315059/206325076-3630d492-55fd-41b5-b999-6d6e2a1bc872.png"/>
</td>
</tr>
</table>

Live: https://editor.p5js.org/davepagurek/sketches/Cxslk3v1I

## https://github.com/processing/p5.js/issues/5451: Transparent objects cut away the background

This one has the same issues the previous one, but showcases how just turning on premultiplied alpha isn't enough, as it also shows some blending issues. At my workplace, we use premultiplied alpha everywhere, and use `blendFunc(ONE, ONE_MINUS_SRC_ALPHA)`, and that seems to work here too (CSS version on top for reference, p5 on bottom):

<table>
<tr>
<td rowspan="6">

```js
function setup() {
  createCanvas(100, 100, WEBGL);
  setAttributes({ alpha: true, premultipliedAlpha: true })
}

function draw() {
  background(0, 0, 0, 255);
  translate(-width/2, -height/2);
  noStroke();
  fill(255, 0, 0, 128);
  rect(10, 10, 80, 80);
  rect(40, 40, 40, 40);
  noLoop();
}
p5.RendererGL.prototype._applyBlendMode = function() {
  drawingContext.enable(drawingContext.BLEND);
  drawingContext.blendEquation(drawingContext.FUNC_ADD);
  drawingContext.blendFunc(
    drawingContext.ONE,
    drawingContext.ONE_MINUS_SRC_ALPHA
  );
  // TODO support the non default blend modes here
}
p5.RendererGL.prototype._getColorShader = function() {
  if (!this._defaultImmediateModeShader) {
    this._defaultImmediateModeShader = new p5.Shader(
      this,
      defaultShaders.normalVert,
      basicFrag
    );
    console.log('made new shader')
  }

  return this._defaultImmediateModeShader;
};

const basicFrag = `
precision mediump float;
uniform vec4 uMaterialColor;
void main(void) {
  // OLD VERSION:
  // gl_FragColor = uMaterialColor;
  
  // NEW VERSION:
  gl_FragColor = vec4(uMaterialColor.rgb, 1.) * uMaterialColor.a;
}
`
```

</td>
<th>premultipliedAlpha: false</th>
</tr>
<tr>
<td>
<img src="https://user-images.githubusercontent.com/5315059/206326621-b6ea1410-b8be-4e13-bd81-39f537731c4d.png" />
</td></tr>
<tr><th>premultipliedAlpha: true</th></tr>
<tr><td>
<img src="https://user-images.githubusercontent.com/5315059/206327415-76c55a18-f26d-4581-b353-95bc185168fd.png"/>
</td>
</tr>
<tr><th>premultipliedAlpha: true + blending changes</th></tr>
<tr><td>
<img src="https://user-images.githubusercontent.com/5315059/206326541-988089d8-e985-497f-998c-580979f71cb0.png"/>
</td>
</tr>
</table>

Live: https://editor.p5js.org/davepagurek/sketches/u4L4gBOOM

Unfortunately that means that this will be a bigger change than just flipping a premultiplied alpha switch, as (1) the shaders need to be updated to write premultiplied alpha, (2) the blend functions might all need to be updated, and (3) I suspect we'll also need to set `gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true)` in order for images to also premultiply their alphas when sent to shaders to keep things in the same format.

### Cost of this

In addition to changing all those things, any shaders that dealt with transparency before will work differently after this change, as they will need to either turn off premultiplied alpha, or update their shader code to handle colors being premultiplied alpha. Thankfully it seems like shaders with transparency seem to be in the minority, and just about all the examples I see online using shaders don't output any transparent pixels.

Anyway this might not be something we want to do immediately because it does take time to test that all the shader and blend mode combinations work as expected, but might be something to think about!
