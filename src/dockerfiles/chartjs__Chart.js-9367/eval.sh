#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 840599637f2af797d42731ec27d91e0c82325134 test/specs/plugin.decimation.tests.js
git apply --verbose --reject - <<'EOF_a2a4e54e669c'
diff --git a/test/specs/plugin.decimation.tests.js b/test/specs/plugin.decimation.tests.js
index f9efbc29af7..9f8320b1e72 100644
--- a/test/specs/plugin.decimation.tests.js
+++ b/test/specs/plugin.decimation.tests.js
@@ -179,5 +179,41 @@ describe('Plugin.decimation', function() {
       expect(chart.data.datasets[0].data[3].x).toBe(originalData[5].x);
       expect(chart.data.datasets[0].data[4].x).toBe(originalData[6].x);
     });
+
+    it('should not crash with uneven points', function() {
+      const data = [];
+      for (let i = 0; i < 15552; i++) {
+        data.push({x: i, y: i});
+      }
+
+      function createChart() {
+        return window.acquireChart({
+          type: 'line',
+          data: {
+            datasets: [{
+              data
+            }]
+          },
+          options: {
+            devicePixelRatio: 1.25,
+            parsing: false,
+            scales: {
+              x: {
+                type: 'linear'
+              }
+            },
+            plugins: {
+              decimation: {
+                enabled: true,
+                algorithm: 'lttb'
+              }
+            }
+          }
+        }, {
+          canvas: {width: 511, height: 511},
+        });
+      }
+      expect(createChart).not.toThrow();
+    });
   });
 });

EOF_a2a4e54e669c
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout 840599637f2af797d42731ec27d91e0c82325134 test/specs/plugin.decimation.tests.js
