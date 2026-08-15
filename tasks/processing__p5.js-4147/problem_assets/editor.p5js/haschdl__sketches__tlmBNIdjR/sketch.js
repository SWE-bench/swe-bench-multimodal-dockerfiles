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
