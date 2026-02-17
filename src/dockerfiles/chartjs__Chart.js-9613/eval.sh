#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 8d68b119bcb95af182cc69d42acad8490af53d3e test/specs/core.plugin.tests.js
git apply --verbose --reject - <<'EOF_40e43572daf2'
diff --git a/test/specs/core.plugin.tests.js b/test/specs/core.plugin.tests.js
index 5c1c9cccb8d..285dbab5b54 100644
--- a/test/specs/core.plugin.tests.js
+++ b/test/specs/core.plugin.tests.js
@@ -398,10 +398,10 @@ describe('Chart.plugins', function() {
       const results = [];
       const chart = window.acquireChart({
         options: {
-          events: ['mousemove', 'test', 'test2'],
+          events: ['mousemove', 'test', 'test2', 'pointerleave'],
           plugins: {
             testPlugin: {
-              events: ['test']
+              events: ['test', 'pointerleave']
             }
           }
         },
@@ -418,7 +418,8 @@ describe('Chart.plugins', function() {
       await jasmine.triggerMouseEvent(chart, 'mousemove', {x: 0, y: 0});
       await jasmine.triggerMouseEvent(chart, 'test', {x: 0, y: 0});
       await jasmine.triggerMouseEvent(chart, 'test2', {x: 0, y: 0});
-      expect(results).toEqual(['beforetest', 'aftertest']);
+      await jasmine.triggerMouseEvent(chart, 'pointerleave', {x: 0, y: 0});
+      expect(results).toEqual(['beforetest', 'aftertest', 'beforemouseout', 'aftermouseout']);
     });
   });
 });

EOF_40e43572daf2
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout 8d68b119bcb95af182cc69d42acad8490af53d3e test/specs/core.plugin.tests.js
