#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
echo "No test files to reset"
git apply --verbose --reject - <<'EOF_720495a867c9'
diff --git a/test/specs/new/list_loose_tasks.html b/test/specs/new/list_loose_tasks.html
new file mode 100644
index 0000000000..ae4e8c58b2
--- /dev/null
+++ b/test/specs/new/list_loose_tasks.html
@@ -0,0 +1,12 @@
+<ul>
+<li>
+<p>Tasks</p>
+</li>
+<li>
+<p><input type="checkbox" checked="" disabled=""> Task1</p>
+</li>
+<li>
+<p><input type="checkbox" disabled=""></p>
+<pre>Task2</pre>
+</li>
+</ul>
diff --git a/test/specs/new/list_loose_tasks.md b/test/specs/new/list_loose_tasks.md
new file mode 100644
index 0000000000..cb1cab5b0d
--- /dev/null
+++ b/test/specs/new/list_loose_tasks.md
@@ -0,0 +1,4 @@
+- Tasks
+- [x] Task1
+
+- [ ] <pre>Task2</pre>

EOF_720495a867c9
: '>>>>> Start Test Output'
./node_modules/.bin/jasmine --no-color --config=jasmine.json
: '>>>>> End Test Output'
echo "No test files to reset"
