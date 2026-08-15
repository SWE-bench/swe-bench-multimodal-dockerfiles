var sh;

function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL);
  
  sh = createShader(
    'attribute vec3 aPosition; void main() { gl_Position = vec4(aPosition, 1.0); }',
    'void main() { gl_FragColor = vec4(1.0,1.0,1.0,1.0); }'
  );
  
  shader(sh);
  noStroke();
  sphere(200);
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}

function draw() {
  background(0);
  
  // draw an orange sphere
  fill(255, 128, 0);
  directionalLight(255, 255, 255, 1, 1, -1);
  sphere(200);
}