#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
echo "No test files to reset"
git apply --verbose --reject - <<'EOF_1f9c76cdce01'
diff --git a/test/specs/new/unicode_punctuation.html b/test/specs/new/unicode_punctuation.html
new file mode 100644
index 0000000000..f59ff116fd
--- /dev/null
+++ b/test/specs/new/unicode_punctuation.html
@@ -0,0 +1,28 @@
+<p>Ideographic comma:</p>
+
+<ul>
+  <li>
+    <p>
+      ×: あれ、<strong><code>foo</code>これ</strong>、それ
+    </p>
+  </li>
+  <li>
+    <p>
+      ○: あれ、 <strong><code>foo</code>これ</strong>、それ
+    </p>
+  </li>
+  <li>
+    <p>
+      ×: あれ、<strong><code>foo</code>これ</strong> 、それ
+    </p>
+  </li>
+  <li><p>○: あれ、<strong>fooこれ</strong>、それ</p></li>
+  <li>
+    <p>○: あれ、 <strong>fooこれ</strong>、それ</p>
+  </li>
+  <li>
+    <p>○: あれ、<strong>fooこれ</strong> 、それ</p>
+  </li>
+</ul>
+
+<p><strong>Fullwidth colon</strong>：\uFF1A</p>
diff --git a/test/specs/new/unicode_punctuation.md b/test/specs/new/unicode_punctuation.md
new file mode 100644
index 0000000000..502843b5c8
--- /dev/null
+++ b/test/specs/new/unicode_punctuation.md
@@ -0,0 +1,11 @@
+Ideographic comma:
+
+* ×: あれ、**`foo`これ**、それ
+* ○: あれ、 **`foo`これ**、それ
+* ×: あれ、**`foo`これ** 、それ
+
+* ○: あれ、**fooこれ**、それ
+* ○: あれ、 **fooこれ**、それ
+* ○: あれ、**fooこれ** 、それ
+
+__Fullwidth colon__：\uFF1A

EOF_1f9c76cdce01
: '>>>>> Start Test Output'
./node_modules/.bin/jasmine --no-color --config=jasmine.json
: '>>>>> End Test Output'
echo "No test files to reset"
