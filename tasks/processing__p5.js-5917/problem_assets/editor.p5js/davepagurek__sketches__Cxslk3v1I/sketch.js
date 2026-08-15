function setup() {
  createCanvas(400, 400, WEBGL);
  pixelDensity(2);
  setAttributes({ alpha: true, premultipliedAlpha: true });
  noFill();
  stroke(200, 200, 255);
  strokeWeight(1);
}
function draw() {
  background(0, 0, 0, 0); // black w/ alpha zero
  scale(4);
  box();
  noLoop();
}
