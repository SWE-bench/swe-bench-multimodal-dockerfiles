#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 2a8152e66e02cf71406fb96e3c49642946a24be0 packages/stylesheet/tests/resolve.test.js
git apply --verbose --reject - <<'EOF_60a79f397a04'
diff --git a/packages/stylesheet/tests/resolve.test.js b/packages/stylesheet/tests/resolve.test.js
index b2ace6c16..f858bce84 100644
--- a/packages/stylesheet/tests/resolve.test.js
+++ b/packages/stylesheet/tests/resolve.test.js
@@ -455,6 +455,24 @@ describe('stylesheet resolve', () => {
     expect(styles).toEqual({ fontWeight: 800 });
   });
 
+  test('should keep flex basis percent value', () => {
+    const styles = resolve({}, { flexBasis: '40%' });
+
+    expect(styles).toEqual({ flexBasis: '40%' });
+  });
+
+  test('should keep flex shrink percent value', () => {
+    const styles = resolve({}, { flexShrink: '40%' });
+
+    expect(styles).toEqual({ flexShrink: '40%' });
+  });
+
+  test('should keep flex grow percent value', () => {
+    const styles = resolve({}, { flexGrow: '40%' });
+
+    expect(styles).toEqual({ flexGrow: '40%' });
+  });
+
   test('should resolve max-height media queries on narrow container', () => {
     const styles = resolve(
       { height: 300 },

EOF_60a79f397a04
: '>>>>> Start Test Output'
NODE_OPTIONS="--experimental-vm-modules" ./node_modules/.bin/jest --no-color
: '>>>>> End Test Output'
git checkout 2a8152e66e02cf71406fb96e3c49642946a24be0 packages/stylesheet/tests/resolve.test.js
