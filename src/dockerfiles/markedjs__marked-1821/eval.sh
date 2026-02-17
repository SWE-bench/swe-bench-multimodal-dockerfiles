#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
echo "No test files to reset"
git apply --verbose --reject - <<'EOF_3f6ca82df307'
diff --git a/test/specs/new/del_strikethrough.html b/test/specs/new/del_strikethrough.html
new file mode 100644
index 0000000000..980134aa21
--- /dev/null
+++ b/test/specs/new/del_strikethrough.html
@@ -0,0 +1,16 @@
+<p><del>test</del></p>
+
+<p>~~test~</p>
+
+<p>~test~~</p>
+
+<p><del>test</del></p>
+
+<p><del>test
+test</del></p>
+
+<p>~~test</p>
+
+<p>test~~</p>
+
+<pre><code class="language-test~~~"></code></pre>
diff --git a/test/specs/new/del_strikethrough.md b/test/specs/new/del_strikethrough.md
new file mode 100644
index 0000000000..f3d5bca081
--- /dev/null
+++ b/test/specs/new/del_strikethrough.md
@@ -0,0 +1,16 @@
+~~test~~
+
+~~test~
+
+~test~~
+
+~test~
+
+~~test
+test~~
+
+~~test
+
+test~~
+
+~~~test~~~

EOF_3f6ca82df307
: '>>>>> Start Test Output'
./node_modules/.bin/jasmine --no-color --config=jasmine.json
: '>>>>> End Test Output'
echo "No test files to reset"
