#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout c6d686ed53d9de61240939c7e5d85e1f3eb29072 test/manual-test-examples/webgl/geometryImmediate/sketch.js test/unit/webgl/p5.RendererGL.js
git apply --verbose --reject - <<'EOF_8488736ad98c'
diff --git a/test/manual-test-examples/webgl/geometryImmediate/sketch.js b/test/manual-test-examples/webgl/geometryImmediate/sketch.js
index 295e2b0188..f6404ea99f 100644
--- a/test/manual-test-examples/webgl/geometryImmediate/sketch.js
+++ b/test/manual-test-examples/webgl/geometryImmediate/sketch.js
@@ -27,7 +27,7 @@ function draw() {
 }
 
 function ngon(n, x, y, d) {
-  beginShape();
+  beginShape(TESS);
   for (let i = 0; i < n + 1; i++) {
     angle = TWO_PI / n * i;
     px = x + sin(angle) * d / 2;
diff --git a/test/unit/webgl/p5.RendererGL.js b/test/unit/webgl/p5.RendererGL.js
index 82599db9a4..de324b6c96 100644
--- a/test/unit/webgl/p5.RendererGL.js
+++ b/test/unit/webgl/p5.RendererGL.js
@@ -445,7 +445,7 @@ suite('p5.RendererGL', function() {
       myp5.stroke(255);
       myp5.triangle(0, 0, 1, 0, 0, 1);
 
-      var buffers = renderer.gHash['tri'];
+      var buffers = renderer.retainedMode.geometry['tri'];
 
       assert.isObject(buffers);
       assert.isDefined(buffers.indexBuffer);

EOF_8488736ad98c
: '>>>>> Start Test Output'
sed -i 's/concurrency:[[:space:]]*[0-9][0-9]*/concurrency: 1/g' Gruntfile.js
stdbuf -o 1M ./node_modules/.bin/grunt test --quiet --force
: '>>>>> End Test Output'
git checkout c6d686ed53d9de61240939c7e5d85e1f3eb29072 test/manual-test-examples/webgl/geometryImmediate/sketch.js test/unit/webgl/p5.RendererGL.js
