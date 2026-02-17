#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout e3953acf1edb80c3e99c53ea22634304f3c31afa test/specs/core.plugin.tests.js
git apply --verbose --reject - <<'EOF_b71f681954a4'
diff --git a/test/specs/core.plugin.tests.js b/test/specs/core.plugin.tests.js
index c709846d1e9..af93dc53af3 100644
--- a/test/specs/core.plugin.tests.js
+++ b/test/specs/core.plugin.tests.js
@@ -342,5 +342,24 @@ describe('Chart.plugins', function() {
 
 			expect(plugin.hook).not.toHaveBeenCalled();
 		});
+
+		it('should not restart plugins when a double register occurs', function() {
+			var results = [];
+			var chart = window.acquireChart({
+				plugins: [{
+					start: function() {
+						results.push(1);
+					}
+				}]
+			});
+
+			Chart.register({id: 'abc', hook: function() {}});
+			Chart.register({id: 'def', hook: function() {}});
+
+			chart.update();
+
+			// The plugin on the chart should only be started once
+			expect(results).toEqual([1]);
+		});
 	});
 });

EOF_b71f681954a4
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout e3953acf1edb80c3e99c53ea22634304f3c31afa test/specs/core.plugin.tests.js
