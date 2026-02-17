#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 69702de9f245b2b960fa24f127e5e3b2b3d21ecc test/unit/webgl/p5.RendererGL.js
git apply --verbose --reject - <<'EOF_3eb7660ec797'
diff --git a/test/unit/webgl/p5.RendererGL.js b/test/unit/webgl/p5.RendererGL.js
index bd6b915a2e..99bd247a65 100644
--- a/test/unit/webgl/p5.RendererGL.js
+++ b/test/unit/webgl/p5.RendererGL.js
@@ -1392,6 +1392,44 @@ suite('p5.RendererGL', function() {
     });
   });
 
+  suite('Test for register availability', function() {
+    test('register enable/disable flag test', function(done) {
+      const renderer = myp5.createCanvas(16, 16, myp5.WEBGL);
+
+      // geometry without aTexCoord.
+      const myGeom = new p5.Geometry(1, 1, function() {
+        this.gid = 'registerEnabledTest';
+        this.vertices.push(myp5.createVector(-8, -8));
+        this.vertices.push(myp5.createVector(8, -8));
+        this.vertices.push(myp5.createVector(8, 8));
+        this.vertices.push(myp5.createVector(-8, 8));
+        this.faces.push([0, 1, 2]);
+        this.faces.push([0, 2, 3]);
+        this.computeNormals();
+      });
+
+      myp5.fill(255);
+      myp5.directionalLight(255, 255, 255, 0, 0, -1);
+
+      myp5.triangle(-8, -8, 8, -8, 8, 8);
+
+      // get register location of
+      // lightingShader's aTexCoord attribute.
+      const attributes = renderer._curShader.attributes;
+      const loc = attributes.aTexCoord.location;
+
+      assert.equal(renderer.registerEnabled[loc], true);
+
+      myp5.model(myGeom);
+      assert.equal(renderer.registerEnabled[loc], false);
+
+      myp5.triangle(-8, -8, 8, 8, -8, 8);
+      assert.equal(renderer.registerEnabled[loc], true);
+
+      done();
+    });
+  });
+
   suite('setAttributes', function() {
     test('It leaves a reference to the correct canvas', function(done) {
       const renderer = myp5.createCanvas(10, 10, myp5.WEBGL);

EOF_3eb7660ec797
: '>>>>> Start Test Output'
sed -i 's/concurrency:[[:space:]]*[0-9][0-9]*/concurrency: 1/g' Gruntfile.js
stdbuf -o 1M ./node_modules/.bin/grunt test --quiet --force
: '>>>>> End Test Output'
git checkout 69702de9f245b2b960fa24f127e5e3b2b3d21ecc test/unit/webgl/p5.RendererGL.js
