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