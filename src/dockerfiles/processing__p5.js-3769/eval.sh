#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout f310e50d8b94ade1ed6b5759b0713d3a67301517 test/unit/webgl/p5.RendererGL.js
git apply --verbose --reject - <<'EOF_ebe118371b89'
diff --git a/test/unit/webgl/p5.RendererGL.js b/test/unit/webgl/p5.RendererGL.js
index 7659a70426..dff7ada827 100644
--- a/test/unit/webgl/p5.RendererGL.js
+++ b/test/unit/webgl/p5.RendererGL.js
@@ -285,4 +285,28 @@ suite('p5.RendererGL', function() {
       done();
     });
   });
+
+  suite('BufferDef', function() {
+    test('render buffer properties are correctly set', function(done) {
+      var renderer = myp5.createCanvas(10, 10, myp5.WEBGL);
+
+      myp5.fill(255);
+      myp5.stroke(255);
+      myp5.triangle(0, 0, 1, 0, 0, 1);
+
+      var buffers = renderer.gHash['tri'];
+
+      assert.isObject(buffers);
+      assert.isDefined(buffers.indexBuffer);
+      assert.isDefined(buffers.vertexBuffer);
+      assert.isDefined(buffers.lineNormalBuffer);
+      assert.isDefined(buffers.lineVertexBuffer);
+      assert.isDefined(buffers.vertexBuffer);
+
+      assert.equal(buffers.vertexCount, 3);
+      assert.equal(buffers.lineVertexCount, 18);
+
+      done();
+    });
+  });
 });

EOF_ebe118371b89
: '>>>>> Start Test Output'
sed -i 's/concurrency:[[:space:]]*[0-9][0-9]*/concurrency: 1/g' Gruntfile.js
stdbuf -o 1M ./node_modules/.bin/grunt test --quiet --force
: '>>>>> End Test Output'
git checkout f310e50d8b94ade1ed6b5759b0713d3a67301517 test/unit/webgl/p5.RendererGL.js
