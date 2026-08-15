function setup() {
  createCanvas(100, 100, WEBGL);
  setAttributes({ alpha: true, premultipliedAlpha: true })
}

function draw() {
  background(0, 0, 0, 255);
  translate(-width/2, -height/2);
  noStroke();
  fill(255, 0, 0, 128);
  rect(10, 10, 80, 80);
  rect(40, 40, 40, 40);
  noLoop();
}
p5.RendererGL.prototype._applyBlendMode = function() {
  drawingContext.enable(drawingContext.BLEND);
  drawingContext.blendEquation(drawingContext.FUNC_ADD);
  drawingContext.blendFunc(drawingContext.ONE, drawingContext.ONE_MINUS_SRC_ALPHA);
}
p5.RendererGL.prototype._getColorShader = function() {
  if (!this._defaultImmediateModeShader) {
    this._defaultImmediateModeShader = new p5.Shader(
      this,
      normalVert,
      basicFrag
    );
  }

  return this._defaultImmediateModeShader;
};

const normalVert = `
attribute vec3 aPosition;
attribute vec3 aNormal;
attribute vec2 aTexCoord;

uniform mat4 uModelViewMatrix;
uniform mat4 uProjectionMatrix;
uniform mat3 uNormalMatrix;

varying vec3 vVertexNormal;
varying highp vec2 vVertTexCoord;

void main(void) {
  vec4 positionVec4 = vec4(aPosition, 1.0);
  gl_Position = uProjectionMatrix * uModelViewMatrix * positionVec4;
  vVertexNormal = normalize(vec3( uNormalMatrix * aNormal ));
  vVertTexCoord = aTexCoord;
}
`

const basicFrag = `
precision mediump float;
uniform vec4 uMaterialColor;
void main(void) {
  gl_FragColor = vec4(uMaterialColor.rgb, 1.) * uMaterialColor.a;
}
`
