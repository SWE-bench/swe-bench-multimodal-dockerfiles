WebGL blending doesn't always work with transparent textures
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

Firefox 106.0.2

### Operating System

MacOS 12.5.1

### Steps to reproduce this

When rendering text, the rectangle in which we draw each character sets each pixel to the fill color, but with alpha based on whether each pixel is inside or outside the glyph's shapes. In MULTIPLY blend mode, the alpha is ignored, so it looks like `text()` is just drawing rectangles:

<table>
<tr>
<td>

```js
let font

function preload() {
  font = loadFont(
    'https://fonts.gstatic.com/s/inter/v3/UcCO3FwrK' +
    '3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVu' + 
    'GKYMZhrib2Bg-4.ttf'
  )
}

function setup() {
  createCanvas(300, 300, WEBGL)
  pixelDensity(2)
  noLoop()
}

function draw() {
  push()
  
  background(255)
  textFont(font)
  textSize(31.5)
  textAlign(CENTER, CENTER)
  
  blendMode(MULTIPLY)
  
  push()
  fill(255, 0, 0)
  translate(-100, -100)
  text(
    'The quick brown fox jumps over the lazy dog',
    0, 0, 200, 200
  )
  pop()
  
  push()
  fill(0, 0, 255)
  translate(-95, -95)
  text(
    'The quick brown fox jumps over the lazy dog',
    0, 0, 200, 200
  )
  pop()
  
  pop()
}
```

</td>
<td>

<img src="https://user-images.githubusercontent.com/5315059/200186009-b63449c6-38e4-4b35-8b01-7f807cd6ec5a.png" />

</td>
</tr>
</table>

This isn't an issue with the ADD blend mode:

<table>
<tr>
<td>

```js
let font

function preload() {
  font = loadFont(
    'https://fonts.gstatic.com/s/inter/v3/UcCO3FwrK' +
    '3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVu' + 
    'GKYMZhrib2Bg-4.ttf'
  )
}

function setup() {
  createCanvas(300, 300, WEBGL)
  pixelDensity(2)
  noLoop()
}

function draw() {
  push()
  
  background(0)
  textFont(font)
  textSize(31.5)
  textAlign(CENTER, CENTER)
  
  blendMode(ADD)
  
  push()
  fill(255, 0, 0)
  translate(-100, -100)
  text(
    'The quick brown fox jumps over the lazy dog',
    0, 0, 200, 200
  )
  pop()
  
  push()
  fill(0, 0, 255)
  translate(-95, -95)
  text(
    'The quick brown fox jumps over the lazy dog',
    0, 0, 200, 200
  )
  pop()
  
  pop()
}
```

</td>
<td>

<img src="https://user-images.githubusercontent.com/5315059/200186082-5789a1c4-fbc4-4dd3-a244-54c96f0ee608.png" />

</td>
</tr>
</table>

