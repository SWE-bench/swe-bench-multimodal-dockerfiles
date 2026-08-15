Tint() is not supported in WebGL
#### Nature of issue?

- [ ] Found a bug
- [ ] Existing feature enhancement
- [x] New feature request

#### Most appropriate sub-area of p5.js?

- [ ] Color
- [ ] Core
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

- [x] Mobile/Tablet (touch devices)
- [x] Desktop/Laptop
- [x] Others (specify if possible)

#### New feature details:
Tint() is supported in processing with OPENGL render, could p5js also support it in WEBGL?
- p5.js version: p5.js v0.5.16 
- Example Code:
```
var img;
function preload() {
    img = loadImage("https://processing.org/img/processing-web.png");
}

function setup() {
    createCanvas(700,700, WEBGL);
}

function draw() {
    background(200);
    beginShape();
    tint(255,0,0,122);
    texture(img);
    vertex(0, 0, 0,0,0);
    vertex(0, 250, 0,1);
    vertex(250, 250, 0,1,1);
    vertex(250, 0, 0,1,0);
    endShape(CLOSE);
}
```

