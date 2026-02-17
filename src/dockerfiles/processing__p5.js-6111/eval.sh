#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 113b99ea8b249285f1ba2c09d869f0288a256cd4 test/unit/webgl/p5.Camera.js
git apply --verbose --reject - <<'EOF_6f752456474a'
diff --git a/test/unit/webgl/p5.Camera.js b/test/unit/webgl/p5.Camera.js
index f772636e32..28ac1d83f1 100644
--- a/test/unit/webgl/p5.Camera.js
+++ b/test/unit/webgl/p5.Camera.js
@@ -593,7 +593,7 @@ suite('p5.Camera', function() {
         /* eslint-disable indent */
         var expectedMatrix = new Float32Array([
           -2,  0,  0,  0,
-           0, -2,  0,  0,
+           0,  2,  0,  0,
            0,  0, -0, -1,
            0,  0,  2,  0
         ]);
@@ -606,10 +606,10 @@ suite('p5.Camera', function() {
 
       test('frustum() with no parameters specified (sets default)', function() {
         var expectedMatrix = new Float32Array([
-          0, 0,  0,  0,
-          0, 0,  0,  0,
-          0, 0, -1, -1,
-          0, 0, -0,  0
+          1.7320507764816284, 0, 0, 0,
+          0, 1.7320507764816284, 0, 0,
+          0, -0, -1.0202020406723022, -1,
+          0, 0, -17.49546241760254, 0
         ]);
 
         myCam.frustum();

EOF_6f752456474a
: '>>>>> Start Test Output'
sed -i 's/concurrency:[[:space:]]*[0-9][0-9]*/concurrency: 1/g' Gruntfile.js
stdbuf -o 1M ./node_modules/.bin/grunt test --quiet --force
: '>>>>> End Test Output'
git checkout 113b99ea8b249285f1ba2c09d869f0288a256cd4 test/unit/webgl/p5.Camera.js
