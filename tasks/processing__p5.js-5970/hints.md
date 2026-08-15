Thanks for isolating the problem! Adding `geom.uvs.push([0, 0], [0, 0], [0, 0], [0, 0])` to your sketch seems to fix the issue, so that can be a temporary fix if anyone else stumbles upon this issue.

I think your solution of enabling/disabling attributes works! I think the question will be whether or not we want our shaders (and users' custom shaders) to have to handle attributes potentially being disabled. How do you feel about, for now, auto-filling geometry buffers with 0s when we first use them? Then user shaders can always assume the `aTexCoord` attribute will exist without having to worry about whether or not a given geometry has them? Otherwise, if a user's custom shader uses `aTexCoord` but a geometry doesn't have any, maybe we'd want to display a friendly error.
Actually, if the attribute is disabled, it seems like one can still use `aTexCoord` in a shader, given that your sphere example works. So I think either approach is fine! I'm not sure without looking more closely if anything else relies on all the attribute data being defined/enabled, so if we implement this by enabling/disabling attributes, let's just make sure we add unit tests to make sure switching between shaders and immediate/retained geometry and retained geometry with/without attribute data works.
First of all, I think that it is better not to adopt the method of filling with 0.
The reason is that if you do it by drawing with fill, _useVertexColor, which is determined by the length of the array, will become true, and even if you try to draw in a single color, you will only be able to draw in black.
Regarding stroke, this problem does not occur because the vertexStrokeColors array used for judgment and the array configured by _edgesToVertices to send to the buffer are separate, but if you try to do the same thing with fill, the array will be duplicated. You will have to.
You'll have to do something like this every time you add a new attribute, but relying on register enable/disable allows you to handle any number of attributes in the same way.

Here's an example to show that the problem is with registers on and off.
[vertexColor_bug_sample](https://editor.p5js.org/dark_fox/sketches/NukJ-i3oK)
```javascript
let gr;

function setup() {
  createCanvas(400, 400, WEBGL);

  noStroke();
  gr = createGraphics(256, 256);
  gr.background(255);

  image(gr, -200, -200, 400, 400);

  fill(255, 0, 0);
  sphere(120); // The red sphere disappears.
}
```
In this example, the 3rd register is turned on when drawing with the image function. If it does not close, it will be judged that the information necessary for drawing is insufficient, and the red sphere will not be displayed in the center on my Android.
Closing the register like this draws nicely on my Android as well.
resolve version: [vertexColor_bug_resolve](https://editor.p5js.org/dark_fox/sketches/x6PFRwB5x)
This uses a non-lighting shader to draw the sphere, but using a lighting shader gives the same result.
[vertexColor_bug_sample2](https://editor.p5js.org/dark_fox/sketches/hl2NEt7vP)
[vertexColor_bug_resolve2](https://editor.p5js.org/dark_fox/sketches/PQS6H9adE)

I'm not familiar with it, so I can't decide which is more disadvantageous for drawing, turning registers on and off or padding arrays. However, it seems somewhat reasonable to rely on register on/off.

By recording the on/off status of registers in the global array, you can also avoid calling functions that close registers unnecessarily.
Also, when closing a register, it notifies the shader's attributes that use that register that it has been closed (attr.enabled = false), so it can be reliably enabled if the register is needed for subsequent drawing. And if you draw under the same conditions, the register will be left open and enabled will not be called unnecessarily.

And about the unit test, I'm sorry, I'm not familiar with it, but can it handle environment-dependent bugs? If possible, I'd like to create appropriate tests with examples like the ones I've given here.
I think you can try it with your normal workflow to see if this specification change has any effect on conventional drawing. If that doesn't work, I guess I'll try another method...