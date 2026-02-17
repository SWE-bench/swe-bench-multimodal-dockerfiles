#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 0cf6487547791c9ef9519752f5b434abe27857b4 test/unit/webgl/p5.RendererGL.js
git apply --verbose --reject - <<'EOF_a89ebc86e168'
diff --git a/test/unit/webgl/p5.RendererGL.js b/test/unit/webgl/p5.RendererGL.js
index dbecaee74f..e0eabf65b7 100644
--- a/test/unit/webgl/p5.RendererGL.js
+++ b/test/unit/webgl/p5.RendererGL.js
@@ -622,6 +622,19 @@ suite('p5.RendererGL', function() {
       );
       done();
     });
+
+    test('blendModes are applied to point drawing', function(done) {
+      myp5.createCanvas(32, 32, myp5.WEBGL);
+      myp5.background(0);
+      myp5.blendMode(myp5.ADD);
+      myp5.strokeWeight(32);
+      myp5.stroke(255, 0, 0);
+      myp5.point(0, 0, 0);
+      myp5.stroke(0, 0, 255);
+      myp5.point(0, 0, 0);
+      assert.deepEqual(myp5.get(16, 16), [255, 0, 255, 255]);
+      done();
+    });
   });
 
   suite('BufferDef', function() {

EOF_a89ebc86e168
: '>>>>> Start Test Output'
sed -i 's/concurrency:[[:space:]]*[0-9][0-9]*/concurrency: 1/g' Gruntfile.js
stdbuf -o 1M ./node_modules/.bin/grunt test --quiet --force
: '>>>>> End Test Output'
git checkout 0cf6487547791c9ef9519752f5b434abe27857b4 test/unit/webgl/p5.RendererGL.js
