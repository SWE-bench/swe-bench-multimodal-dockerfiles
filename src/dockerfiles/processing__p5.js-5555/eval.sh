#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 196d3afbf44de116c84936ff20cf4a5b8056ccb7 test/unit/webgl/p5.RendererGL.js
git apply --verbose --reject - <<'EOF_0914329fd351'
diff --git a/test/unit/webgl/p5.RendererGL.js b/test/unit/webgl/p5.RendererGL.js
index 401e692f06..2195bbe843 100644
--- a/test/unit/webgl/p5.RendererGL.js
+++ b/test/unit/webgl/p5.RendererGL.js
@@ -333,7 +333,7 @@ suite('p5.RendererGL', function() {
       pg.clear();
       myp5.image(pg, -myp5.width / 2, -myp5.height / 2);
       pixel = myp5.get(0, 0);
-      assert.deepEqual(pixel, [0, 255, 255, 255]);
+      assert.deepEqual(pixel, [0, 0, 0, 255]);
       done();
     });
 
@@ -356,7 +356,7 @@ suite('p5.RendererGL', function() {
       pg.background(100, 100, 100, 100);
       myp5.image(pg, -myp5.width / 2, -myp5.height / 2);
       pixel = myp5.get(0, 0);
-      assert.deepEqual(pixel, [39, 194, 194, 194]);
+      assert.deepEqual(pixel, [100, 100, 100, 255]);
       done();
     });
 
@@ -378,7 +378,7 @@ suite('p5.RendererGL', function() {
       pg.clear();
       myp5.image(pg, 0, 0);
       pixel = myp5.get(0, 0);
-      assert.deepEqual(pixel, [0, 255, 255, 255]);
+      assert.deepEqual(pixel, [0, 0, 0, 255]);
       done();
     });
 
@@ -389,7 +389,7 @@ suite('p5.RendererGL', function() {
       pg.background(100, 100, 100, 100);
       myp5.image(pg, 0, 0);
       pixel = myp5.get(0, 0);
-      assert.deepEqual(pixel, [39, 194, 194, 255]);
+      assert.deepEqual(pixel, [100, 100, 100, 255]);
       done();
     });
   });
@@ -437,8 +437,8 @@ suite('p5.RendererGL', function() {
     test('blendModes change pixel colors as expected', function(done) {
       myp5.createCanvas(10, 10, myp5.WEBGL);
       myp5.noStroke();
-      assert.deepEqual([133, 69, 191, 158], mixAndReturn(myp5.ADD, 255));
-      assert.deepEqual([0, 0, 255, 122], mixAndReturn(myp5.REPLACE, 255));
+      assert.deepEqual([133, 69, 191, 255], mixAndReturn(myp5.ADD, 255));
+      assert.deepEqual([0, 0, 255, 255], mixAndReturn(myp5.REPLACE, 255));
       assert.deepEqual([133, 255, 133, 255], mixAndReturn(myp5.SUBTRACT, 255));
       assert.deepEqual([255, 0, 255, 255], mixAndReturn(myp5.SCREEN, 0));
       assert.deepEqual([0, 255, 0, 255], mixAndReturn(myp5.EXCLUSION, 255));

EOF_0914329fd351
: '>>>>> Start Test Output'
sed -i 's/concurrency:[[:space:]]*[0-9][0-9]*/concurrency: 1/g' Gruntfile.js
stdbuf -o 1M ./node_modules/.bin/grunt test --quiet --force
: '>>>>> End Test Output'
git checkout 196d3afbf44de116c84936ff20cf4a5b8056ccb7 test/unit/webgl/p5.RendererGL.js
