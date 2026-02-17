#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
echo "No test files to reset"
git apply --verbose --reject - <<'EOF_c178eda33996'
diff --git a/packages/layout/tests/fullPageView.test.js b/packages/layout/tests/fullPageView.test.js
new file mode 100644
index 000000000..fdec3879a
--- /dev/null
+++ b/packages/layout/tests/fullPageView.test.js
@@ -0,0 +1,56 @@
+import resolvePagination from '../src/steps/resolvePagination';
+import resolveDimensions from '../src/steps/resolveDimensions';
+
+const calcLayout = node => resolvePagination(resolveDimensions(node));
+
+describe('layout', () => {
+  const root = {
+    type: 'DOCUMENT',
+    children: [
+      {
+        type: 'PAGE',
+        box: {},
+        style: {
+          width: 100,
+          height: 100,
+        },
+        children: [
+          {
+            type: 'VIEW',
+            box: {},
+            style: {
+              position: 'absolute',
+              width: '50%',
+              top: 0,
+              bottom: 0,
+            },
+            props: {},
+            children: [],
+          },
+          {
+            type: 'TEXT',
+            box: {},
+            style: {},
+            props: {},
+            children: [
+              {
+                type: 'TEXT_INSTANCE',
+                value: 'hello world',
+              },
+            ],
+          },
+        ],
+      },
+    ],
+  };
+
+  test('should stretch absolute block to full page size', () => {
+    const layout = calcLayout(root);
+
+    const page = layout.children[0];
+    const view = layout.children[0].children[0];
+
+    expect(page.box.height).toBe(100);
+    expect(view.box.height).toBe(100);
+  });
+});

EOF_c178eda33996
: '>>>>> Start Test Output'
NODE_OPTIONS="--experimental-vm-modules" ./node_modules/.bin/jest --no-color
: '>>>>> End Test Output'
echo "No test files to reset"
