fill of certain shapes not working properly in Webgl mode 


#### Nature of issue?

- [x ] Found a bug
- [ ] Existing feature enhancement
- [ ] New feature request

#### Most appropriate sub-area of p5.js?

- [ ] Color
- [ ] Core/Environment/Rendering
- [ ] Data
- [ ] Events
- [ ] Image
- [ ] IO
- [ ] Math
- [ ] Typography
- [ ] Utilities
- [ x] WebGL
- [ ] Other (specify if possible)

#### Which platform were you using when you encountered this?

- [x ] Mobile/Tablet (touch devices)
- [x ] Desktop/Laptop
- [ ] Others (specify if possible)

#### Details about the bug: 

- p5.js version 0.7.3: 
- Steps to reproduce this:


**Here is a minimal working example**. It should draw the letter C (works in 2D), but in WEBGL it creates a strange fill from the lower extremity of the C letter to the origin (top left of the letter).
An example can be seen in <https://codepen.io/sixhat/pen/NmNgLj>

<img width="346" alt="p5-webgl-bug-fill" src="https://user-images.githubusercontent.com/614881/55618773-373a0580-578f-11e9-9126-27b137dbc7ca.png">


```javascript
let points;
function setup(){
	createCanvas(innerWidth, innerHeight, WEBGL);
	 points = [
		{x: 0, y:0},
		{x: 4, y:0},
		{x: 4, y:1},
		{x: 1, y:1},
		{x: 1, y:2},
		{x: 4, y:2},
		{x: 4, y:3},
		{x: 0, y:3},
	];
}

function draw(){
	background("gray");

	beginShape()
	for(let p of points){
		vertex(p.x*30,p.y*30, 0);
	} 
	endShape(CLOSE)
}
```


#### Feature enhancement details:



#### New feature details:


