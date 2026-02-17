#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
echo "No test files to reset"
git apply --verbose --reject - <<'EOF_bb1390faa3d6'
diff --git a/test/specs/new/image_links.html b/test/specs/new/image_links.html
new file mode 100644
index 0000000000..3f2828c536
--- /dev/null
+++ b/test/specs/new/image_links.html
@@ -0,0 +1,11 @@
+<p>
+	<a href="https://example.com/">
+		<img src="https://example.com/image.jpg" alt="test" title="title" />
+	</a>
+</p>
+
+<p>
+	<a href="https://example.com/">
+		<img src="https://example.com/image.jpg" alt="[test]" title="[title]" />
+	</a>
+</p>
diff --git a/test/specs/new/image_links.md b/test/specs/new/image_links.md
new file mode 100644
index 0000000000..109603266e
--- /dev/null
+++ b/test/specs/new/image_links.md
@@ -0,0 +1,3 @@
+[![test](https://example.com/image.jpg "title")](https://example.com/)
+
+[![\[test\]](https://example.com/image.jpg "[title]")](https://example.com/)

EOF_bb1390faa3d6
: '>>>>> Start Test Output'
./node_modules/.bin/jasmine --no-color --config=jasmine.json
: '>>>>> End Test Output'
echo "No test files to reset"
