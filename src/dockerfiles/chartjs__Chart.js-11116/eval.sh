#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 23e8f7d378a84dddd17d958a888ffff7f120c38c test/specs/scale.linear.tests.js
git apply --verbose --reject - <<'EOF_43eb30c4c272'
diff --git a/test/specs/scale.linear.tests.js b/test/specs/scale.linear.tests.js
index 9fbe5467a2d..a8ad53995b1 100644
--- a/test/specs/scale.linear.tests.js
+++ b/test/specs/scale.linear.tests.js
@@ -684,6 +684,28 @@ describe('Linear Scale', function() {
     expect(getLabels(chart.scales.y)).toEqual(['1', '3', '5', '7', '9', '11']);
   });
 
+  it('Should not generate any ticks > max if max is specified', function() {
+    var chart = window.acquireChart({
+      type: 'line',
+      options: {
+        scales: {
+          x: {
+            type: 'linear',
+            min: 2.404e-8,
+            max: 2.4143e-8,
+            ticks: {
+              includeBounds: false,
+            },
+          },
+        },
+      },
+    });
+
+    expect(chart.scales.x.min).toBe(2.404e-8);
+    expect(chart.scales.x.max).toBe(2.4143e-8);
+    expect(chart.scales.x.ticks[chart.scales.x.ticks.length - 1].value).toBeLessThanOrEqual(2.4143e-8);
+  });
+
   it('Should not generate insane amounts of ticks with small stepSize and large range', function() {
     var chart = window.acquireChart({
       type: 'bar',

EOF_43eb30c4c272
: '>>>>> Start Test Output'
pnpm install
pnpm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.cjs --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout 23e8f7d378a84dddd17d958a888ffff7f120c38c test/specs/scale.linear.tests.js
