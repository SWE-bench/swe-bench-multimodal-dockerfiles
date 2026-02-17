#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 12c5f9a8396f2a472f331ef772d6c7ba5cd62513 test/fixtures/controller.line/stacking/bounds-data.png test/specs/controller.line.tests.js
mkdir -p test/fixtures/controller.line/stacking
curl -o test/fixtures/controller.line/stacking/bounds-data.png https://raw.githubusercontent.com/chartjs/Chart.js/871293fb6caf7b7a63dd6249e9fc39b99a121c2d/test/fixtures/controller.line/stacking/bounds-data.png
chmod 777 test/fixtures/controller.line/stacking/bounds-data.png
git apply --verbose --reject - <<'EOF_9202a80f886b'
diff --git a/test/fixtures/controller.line/stacking/bounds-data.png b/test/fixtures/controller.line/stacking/bounds-data.png
index 90ce6a30c28..71ea7e96392 100644
Binary files a/test/fixtures/controller.line/stacking/bounds-data.png and b/test/fixtures/controller.line/stacking/bounds-data.png differ
diff --git a/test/specs/controller.line.tests.js b/test/specs/controller.line.tests.js
index 7210367ca95..684b1919bb2 100644
--- a/test/specs/controller.line.tests.js
+++ b/test/specs/controller.line.tests.js
@@ -59,6 +59,32 @@ describe('Chart.controllers.line', function() {
     expect(createChart).not.toThrow();
   });
 
+  it('should find min and max for stacked chart', function() {
+    var chart = window.acquireChart({
+      type: 'line',
+      data: {
+        datasets: [{
+          data: [10, 11, 12, 13]
+        }, {
+          data: [1, 2, 3, 4]
+        }],
+        labels: ['a', 'b', 'c', 'd']
+      },
+      options: {
+        scales: {
+          y: {
+            stacked: true
+          }
+        }
+      }
+    });
+    expect(chart.getDatasetMeta(0).controller.getMinMax(chart.scales.y, true)).toEqual({min: 10, max: 13});
+    expect(chart.getDatasetMeta(1).controller.getMinMax(chart.scales.y, true)).toEqual({min: 11, max: 17});
+    chart.hide(0);
+    expect(chart.getDatasetMeta(0).controller.getMinMax(chart.scales.y, true)).toEqual({min: 10, max: 13});
+    expect(chart.getDatasetMeta(1).controller.getMinMax(chart.scales.y, true)).toEqual({min: 1, max: 4});
+  });
+
   it('Should create line elements and point elements for each data item during initialization', function() {
     var chart = window.acquireChart({
       type: 'line',

EOF_9202a80f886b
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout 12c5f9a8396f2a472f331ef772d6c7ba5cd62513 test/fixtures/controller.line/stacking/bounds-data.png test/specs/controller.line.tests.js
