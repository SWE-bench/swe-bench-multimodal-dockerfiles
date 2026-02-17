#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 4bd856aab025d4081d650d45402c7fcab78ccb1e test/unit/webgl/p5.RendererGL.js
git apply --verbose --reject - <<'EOF_a40026d1f707'
diff --git a/test/unit/webgl/p5.RendererGL.js b/test/unit/webgl/p5.RendererGL.js
index b0f60762f4..b10bcdda0a 100644
--- a/test/unit/webgl/p5.RendererGL.js
+++ b/test/unit/webgl/p5.RendererGL.js
@@ -447,7 +447,9 @@ suite('p5.RendererGL', function() {
       assert.deepEqual([133, 255, 133, 255], mixAndReturn(myp5.SUBTRACT, 255));
       assert.deepEqual([255, 0, 255, 255], mixAndReturn(myp5.SCREEN, 0));
       assert.deepEqual([0, 255, 0, 255], mixAndReturn(myp5.EXCLUSION, 255));
-      assert.deepEqual([0, 0, 0, 255], mixAndReturn(myp5.MULTIPLY, 255));
+      // Note that in 2D mode, this would just return black, because 2D mode
+      // ignores alpha in this case.
+      assert.deepEqual([133, 69, 202, 255], mixAndReturn(myp5.MULTIPLY, 255));
       assert.deepEqual([255, 0, 255, 255], mixAndReturn(myp5.LIGHTEST, 0));
       assert.deepEqual([0, 0, 0, 255], mixAndReturn(myp5.DARKEST, 255));
       done();
@@ -486,18 +488,22 @@ suite('p5.RendererGL', function() {
         }
       };
 
-      const red = '#F53';
-      const blue = '#13F';
-      assertSameIn2D(red, blue, myp5.BLEND);
-      assertSameIn2D(red, blue, myp5.ADD);
-      assertSameIn2D(red, blue, myp5.DARKEST);
-      assertSameIn2D(red, blue, myp5.LIGHTEST);
-      assertSameIn2D(red, blue, myp5.EXCLUSION);
-      assertSameIn2D(red, blue, myp5.MULTIPLY);
-      assertSameIn2D(red, blue, myp5.SCREEN);
-      assertSameIn2D(red, blue, myp5.REPLACE);
-      assertSameIn2D(red, blue, myp5.REMOVE);
-      done();
+      for (const alpha of [255, 200]) {
+        const red = myp5.color('#F53');
+        const blue = myp5.color('#13F');
+        red.setAlpha(alpha);
+        blue.setAlpha(alpha);
+        assertSameIn2D(red, blue, myp5.BLEND);
+        assertSameIn2D(red, blue, myp5.ADD);
+        assertSameIn2D(red, blue, myp5.DARKEST);
+        assertSameIn2D(red, blue, myp5.LIGHTEST);
+        assertSameIn2D(red, blue, myp5.EXCLUSION);
+        assertSameIn2D(red, blue, myp5.MULTIPLY);
+        assertSameIn2D(red, blue, myp5.SCREEN);
+        assertSameIn2D(red, blue, myp5.REPLACE);
+        assertSameIn2D(red, blue, myp5.REMOVE);
+        done();
+      }
     });
 
     test('blendModes are included in push/pop', function(done) {

EOF_a40026d1f707
: '>>>>> Start Test Output'
sed -i 's/concurrency:[[:space:]]*[0-9][0-9]*/concurrency: 1/g' Gruntfile.js
stdbuf -o 1M ./node_modules/.bin/grunt test --quiet --force
: '>>>>> End Test Output'
git checkout 4bd856aab025d4081d650d45402c7fcab78ccb1e test/unit/webgl/p5.RendererGL.js
