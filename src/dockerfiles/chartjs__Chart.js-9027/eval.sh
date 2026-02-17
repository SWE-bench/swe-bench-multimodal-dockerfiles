#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout e021a77214daecbca0502da9d4245acbc2c46a1e test/specs/scale.linear.tests.js
git apply --verbose --reject - <<'EOF_a569829c5702'
diff --git a/test/specs/scale.linear.tests.js b/test/specs/scale.linear.tests.js
index 9ff00e7240f..c523afea9db 100644
--- a/test/specs/scale.linear.tests.js
+++ b/test/specs/scale.linear.tests.js
@@ -1220,4 +1220,31 @@ describe('Linear Scale', function() {
     expect(scale.getValueForPixel(end)).toBeCloseTo(min, 4);
     expect(scale.getValueForPixel(start)).toBeCloseTo(max, 4);
   });
+
+  it('should not throw errors when chart size is negative', function() {
+    function createChart() {
+      return window.acquireChart({
+        type: 'bar',
+        data: {
+          labels: [0, 1, 2, 3, 4, 5, 6, 7, '7+'],
+          datasets: [{
+            data: [29.05, 4, 15.69, 11.69, 2.84, 4, 0, 3.84, 4],
+          }],
+        },
+        options: {
+          plugins: false,
+          layout: {
+            padding: {top: 30, left: 1, right: 1, bottom: 1}
+          }
+        }
+      }, {
+        canvas: {
+          height: 0,
+          width: 0
+        }
+      });
+    }
+
+    expect(createChart).not.toThrow();
+  });
 });

EOF_a569829c5702
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout e021a77214daecbca0502da9d4245acbc2c46a1e test/specs/scale.linear.tests.js
