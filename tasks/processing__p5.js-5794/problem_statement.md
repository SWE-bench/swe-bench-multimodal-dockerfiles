blendMode() not working in WebGL mode
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

1.4.2

### Web browser and version

Firefox 104.0.1

### Operating System

MacOS 12.5.3

### Steps to reproduce this

### Steps:
- Set `blendMode` to something non default (e.g. `MULTIPLY`)
- Change from 2D mode to WebGL mode
- Overlapping colours don't blend the same way

### Snippet:

<table>
<tr>
<th>WebGL</th>
<td>

```js
function setup() {
  createCanvas(400, 400, WEBGL);
}

function draw() {
  background(255);
  
  blendMode(MULTIPLY);
  
  noStroke();
  
  fill('red');
  circle(-width/4, -height/4, width);
  
  fill('blue');
  circle(width/4, height/4, width);
}
```

</td>
<td>

![image](https://user-images.githubusercontent.com/5315059/189218282-e2f8b950-24a8-427e-be45-bb2c9ae51a00.png)

</td>
</tr>
<tr>
<th>
2D
</th>
<td>

```js
function setup() {
  createCanvas(400, 400);
}

function draw() {
  background(255);
  translate(width/2, height/2);
  
  blendMode(MULTIPLY);
  
  noStroke();
  
  fill('red');
  circle(-width/4, -height/4, width);
  
  fill('blue');
  circle(width/4, height/4, width);
}
```

</td>
<td>

![image](https://user-images.githubusercontent.com/5315059/189218451-af43d81b-8fa7-4d27-90b1-3a0fc7cd6d30.png)


</td>
</tr>
</table>
