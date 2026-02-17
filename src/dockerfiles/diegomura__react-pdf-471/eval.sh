#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 23b89c2869f75f4f843522de5e348c2f92e87a67 tests/flattenStyles.test.js
git apply --verbose --reject - <<'EOF_f2638b8f2f79'
diff --git a/tests/flattenStyles.test.js b/tests/flattenStyles.test.js
index 5c14a4fa1..36512cf0d 100644
--- a/tests/flattenStyles.test.js
+++ b/tests/flattenStyles.test.js
@@ -28,4 +28,11 @@ describe('flatten styles', () => {
 
     return expect(flatten).toEqual({ fontSize: 16, color: 'white' });
   });
+
+  test('should flat nested arrays', () => {
+    const styles = [{ fontSize: 16, color: 'white' }, [{ color: 'red' }]];
+    const flatten = StyleSheet.flatten(styles);
+
+    return expect(flatten).toEqual({ fontSize: 16, color: 'red' });
+  });
 });

EOF_f2638b8f2f79
: '>>>>> Start Test Output'
./node_modules/.bin/jest --no-color
: '>>>>> End Test Output'
git checkout 23b89c2869f75f4f843522de5e348c2f92e87a67 tests/flattenStyles.test.js
