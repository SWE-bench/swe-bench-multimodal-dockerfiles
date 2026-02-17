#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 74f2f85ec3798e9d72c9b40aaac01aa4b4d8658e test/specs/core.ticks.tests.js
git apply --verbose --reject - <<'EOF_b1b443ae24cb'
diff --git a/test/specs/core.ticks.tests.js b/test/specs/core.ticks.tests.js
index 149d19e72e6..52857b649aa 100644
--- a/test/specs/core.ticks.tests.js
+++ b/test/specs/core.ticks.tests.js
@@ -96,4 +96,13 @@ describe('Test tick generators', function() {
     expect(xLabels).toEqual(['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1']);
     expect(yLabels).toEqual(['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1']);
   });
+
+  describe('formatters.numeric', function() {
+    it('should not fail on empty or 1 item array', function() {
+      const scale = {chart: {options: {locale: 'en'}}, options: {ticks: {format: {}}}};
+      expect(Chart.Ticks.formatters.numeric.apply(scale, [1, 0, []])).toEqual('1');
+      expect(Chart.Ticks.formatters.numeric.apply(scale, [1, 0, [{value: 1}]])).toEqual('1');
+      expect(Chart.Ticks.formatters.numeric.apply(scale, [1, 0, [{value: 1}, {value: 1.01}]])).toEqual('1.00');
+    });
+  });
 });

EOF_b1b443ae24cb
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout 74f2f85ec3798e9d72c9b40aaac01aa4b4d8658e test/specs/core.ticks.tests.js
