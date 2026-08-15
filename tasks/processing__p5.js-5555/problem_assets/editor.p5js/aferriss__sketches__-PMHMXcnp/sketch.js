function setup() {
  createCanvas(100, 100, WEBGL);
}

let toggle = true;

function draw() {
  background(0, 0, 0, 255);
  fill(255, 0, 0, 128);
  
  rect(-40, -40, 80, 80);
  
  if(frameCount % 30 == 0){
    toggle = !toggle;
  }
  
  setAttributes('alpha', toggle);
}
