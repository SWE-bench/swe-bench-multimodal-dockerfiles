#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 275fdaf3dad77908053e4598a52093f671dc7b9e test/specs/controller.polarArea.tests.js test/specs/scale.radialLinear.tests.js
git apply --verbose --reject - <<'EOF_dce92e6b3896'
diff --git a/test/specs/controller.polarArea.tests.js b/test/specs/controller.polarArea.tests.js
index 46c9eb612b7..459d60e9696 100644
--- a/test/specs/controller.polarArea.tests.js
+++ b/test/specs/controller.polarArea.tests.js
@@ -160,7 +160,11 @@ describe('Chart.controllers.polarArea', function() {
           legend: false,
           title: false,
         },
-        startAngle: 90, // default is 0
+        scales: {
+          r: {
+            startAngle: 90, // default is 0
+          }
+        },
         elements: {
           arc: {
             backgroundColor: 'rgb(255, 0, 0)',
diff --git a/test/specs/scale.radialLinear.tests.js b/test/specs/scale.radialLinear.tests.js
index 955a0353a6d..68ed3224949 100644
--- a/test/specs/scale.radialLinear.tests.js
+++ b/test/specs/scale.radialLinear.tests.js
@@ -31,6 +31,8 @@ describe('Test the radial linear scale', function() {
         circular: false
       },
 
+      startAngle: 0,
+
       ticks: {
         color: Chart.defaults.color,
         showLabelBackdrop: true,
@@ -500,6 +502,7 @@ describe('Test the radial linear scale', function() {
       options: {
         scales: {
           r: {
+            startAngle: 15,
             pointLabels: {
               callback: function(value, index) {
                 return index.toString();
@@ -507,7 +510,6 @@ describe('Test the radial linear scale', function() {
             }
           }
         },
-        startAngle: 15
       }
     });
 
@@ -521,7 +523,7 @@ describe('Test the radial linear scale', function() {
       expect(radToNearestDegree(chart.scales.r.getIndexAngle(i))).toBe(15 + (slice * i));
     }
 
-    chart.options.startAngle = 0;
+    chart.scales.r.options.startAngle = 0;
     chart.update();
 
     for (var x = 0; x < 5; x++) {
@@ -569,7 +571,7 @@ describe('Test the radial linear scale', function() {
       textAlign: ['right', 'right', 'left', 'left', 'left'],
       y: [82, 366, 506, 319, 53]
     }].forEach(function(expected) {
-      chart.options.startAngle = expected.startAngle;
+      scale.options.startAngle = expected.startAngle;
       chart.update();
 
       scale.ctx = window.createMockContext();

EOF_dce92e6b3896
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout 275fdaf3dad77908053e4598a52093f671dc7b9e test/specs/controller.polarArea.tests.js test/specs/scale.radialLinear.tests.js
