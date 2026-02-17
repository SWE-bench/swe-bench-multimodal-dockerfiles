#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
echo "No test files to reset"
git apply --verbose --reject - <<'EOF_7c77a7d295ee'
diff --git a/test/specs/new/list_tasks_non_gfm.html b/test/specs/new/list_tasks_non_gfm.html
new file mode 100644
index 0000000000..dfa23220e1
--- /dev/null
+++ b/test/specs/new/list_tasks_non_gfm.html
@@ -0,0 +1,5 @@
+<ul>
+<li>[ ] A</li>
+<li>[x] B</li>
+<li>[ ] C</li>
+</ul>
diff --git a/test/specs/new/list_tasks_non_gfm.md b/test/specs/new/list_tasks_non_gfm.md
new file mode 100644
index 0000000000..b75875a679
--- /dev/null
+++ b/test/specs/new/list_tasks_non_gfm.md
@@ -0,0 +1,7 @@
+---
+gfm: false
+description: Task lists are ignored when not using GFM
+---
+- [ ] A
+- [x] B
+- [ ] C
\ No newline at end of file

EOF_7c77a7d295ee
: '>>>>> Start Test Output'
./node_modules/.bin/jasmine --no-color --config=jasmine.json
: '>>>>> End Test Output'
echo "No test files to reset"
