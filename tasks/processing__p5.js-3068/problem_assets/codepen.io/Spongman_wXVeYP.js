var strings;
function preload() {
  strings = loadStrings('https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.6.1/addons/p5.dom.js');
}
function setup() {
  createCanvas(windowWidth, windowHeight);
}

function draw() {
  background(0);
  fill(255);
  for(var i = 0; i < 100; i ++) {
    text(strings[i+24], 0, 10 + i * 12);
  }
}