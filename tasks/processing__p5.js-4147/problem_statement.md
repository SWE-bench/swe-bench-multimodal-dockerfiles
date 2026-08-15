WEBGL vertex color no longer working as expected in 0.8.0
I read multiple issues related to WEBGL but I could not find this one. It seems something broke between 0.8.0 and 0.9.0. 

#### Nature of issue?

- [x] Found a bug
- [ ] Existing feature enhancement
- [ ] New feature request

#### Most appropriate sub-area of p5.js?

- [x] Color
- [ ] Core/Environment/Rendering
- [ ] Data
- [ ] Events
- [ ] Image
- [ ] IO
- [ ] Math
- [ ] Typography
- [ ] Utilities
- [x] WebGL
- [ ] Other (specify if possible)

#### Which platform were you using when you encountered this?

- [ ] Mobile/Tablet (touch devices)
- [x] Desktop/Laptop
- [ ] Others (specify if possible)

#### Details about the bug: 

- p5.js version: 0.9.0
- Web browser and version: 78.0.3904.97
- Operating System: Windows 10
- Steps to reproduce this:

1) Using the p4js editor, create a new sketch, and make sure the HTML has a reference to p5js version 0.9.0
2) Paste the following code to the editor and hit play. A live version is available [here](https://editor.p5js.org/haschdl/sketches/tlmBNIdjR)

```javascript
function setup() {
  createCanvas(500, 500, WEBGL);
}

function draw() {
  beginShape();
  fill(100,100,20);
  vertex(-150, -150);
  fill(250);
  vertex(150, -150);
  fill(200);
  vertex(150, 150);
  fill(100,50, 100);
  vertex(-150, 150);
  endShape(CLOSE);
}
```
3) The output will be as follows (using p5.js version 0.9.0):
![image](https://user-images.githubusercontent.com/9550197/68548929-8b2a5e00-03f2-11ea-9992-02cb1b185d81.png)

Changing the `sketch.hmtl` to use the version **0.8.0**, we get the expected output. A live version is available [here](https://editor.p5js.org/haschdl/sketches/LNpN29qY4). Note the code in `sketch.js` is the same, but the reference inside `sketch.html` is to p5js 0.8.0
![image](https://user-images.githubusercontent.com/9550197/68548937-ae550d80-03f2-11ea-9570-682b42bbd7e0.png)




#### Feature enhancement details:



#### New feature details:


