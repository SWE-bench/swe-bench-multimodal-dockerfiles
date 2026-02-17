#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 6e1550c4c722cddbda9c09d3d375d37f477b7b3d packages/textkit/tests/layout/applyDefaultStyles.test.js
git apply --verbose --reject - <<'EOF_d26fb93a4ae3'
diff --git a/packages/render/tests/utils/parseColor.test.js b/packages/render/tests/utils/parseColor.test.js
new file mode 100644
index 000000000..8f53261a6
--- /dev/null
+++ b/packages/render/tests/utils/parseColor.test.js
@@ -0,0 +1,28 @@
+import parseColor from '../../src/utils/parseColor';
+
+describe('parse color util', () => {
+  test(`should parse regular hex color`, () => {
+    const color = parseColor('#FF00FF');
+    expect(color.value).toBe('#FF00FF');
+  });
+
+  test(`should parse opacity as 1 if not provided`, () => {
+    const color = parseColor('#FF00FF');
+    expect(color.opacity).toBe(1);
+  });
+
+  test(`should parse opacity as 1 when provided`, () => {
+    const color = parseColor('#FF00FFFF');
+    expect(color.opacity).toBe(1);
+  });
+
+  test(`should parse opacity as 0 when provided`, () => {
+    const color = parseColor('#FF00FF00');
+    expect(color.opacity).toBe(0);
+  });
+
+  test(`should parse opacit provided`, () => {
+    const color = parseColor('#FF00FF54');
+    expect(color.opacity).toBe(0.32941176470588235);
+  });
+});
diff --git a/packages/textkit/tests/layout/applyDefaultStyles.test.js b/packages/textkit/tests/layout/applyDefaultStyles.test.js
index 9155e94f9..831b22dd5 100644
--- a/packages/textkit/tests/layout/applyDefaultStyles.test.js
+++ b/packages/textkit/tests/layout/applyDefaultStyles.test.js
@@ -23,7 +23,6 @@ const DEFAULTS = {
   link: null,
   marginLeft: 0,
   marginRight: 0,
-  opacity: 1,
   paddingTop: 0,
   paragraphSpacing: 0,
   underline: false,

EOF_d26fb93a4ae3
: '>>>>> Start Test Output'
NODE_OPTIONS="--experimental-vm-modules" ./node_modules/.bin/jest --no-color
: '>>>>> End Test Output'
git checkout 6e1550c4c722cddbda9c09d3d375d37f477b7b3d packages/textkit/tests/layout/applyDefaultStyles.test.js
