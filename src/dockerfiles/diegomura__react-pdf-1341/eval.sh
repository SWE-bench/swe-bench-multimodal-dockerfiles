#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout c961db4bf2ba81581c7c0eda02e9fc5f5ef78f01 packages/stylesheet/tests/flex.test.js
git apply --verbose --reject - <<'EOF_5b7c501ed228'
diff --git a/packages/stylesheet/tests/flex.test.js b/packages/stylesheet/tests/flex.test.js
index a24ded307..38ce5d788 100644
--- a/packages/stylesheet/tests/flex.test.js
+++ b/packages/stylesheet/tests/flex.test.js
@@ -10,4 +10,34 @@ describe('stylesheet flex transform', () => {
       flexBasis: 'auto',
     });
   });
+
+  test('should process flex shorthand with one digit', () => {
+    const styles = processFlex('flex', 1);
+
+    expect(styles).toEqual({
+      flexGrow: 1,
+      flexShrink: 1,
+      flexBasis: 0,
+    });
+  });
+
+  test("should process flex '1'", () => {
+    const styles = processFlex('flex', '1');
+
+    expect(styles).toEqual({
+      flexGrow: 1,
+      flexShrink: 1,
+      flexBasis: 0,
+    });
+  });
+
+  test('should process flex shorthand with two digits', () => {
+    const styles = processFlex('flex', '1 0');
+
+    expect(styles).toEqual({
+      flexGrow: 1,
+      flexShrink: 0,
+      flexBasis: 0,
+    });
+  });
 });

EOF_5b7c501ed228
: '>>>>> Start Test Output'
NODE_OPTIONS="--experimental-vm-modules" ./node_modules/.bin/jest --no-color
: '>>>>> End Test Output'
git checkout c961db4bf2ba81581c7c0eda02e9fc5f5ef78f01 packages/stylesheet/tests/flex.test.js
