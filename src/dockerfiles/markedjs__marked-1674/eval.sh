#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 0cd85983ce810c5f833c939cdf66b341dc2d6825 test/specs/new/list_loose_tasks.html test/specs/new/list_loose_tasks.md
git apply --verbose --reject - <<'EOF_0a81fa3000d2'
diff --git a/test/specs/new/list_loose_tasks.html b/test/specs/new/list_loose_tasks.html
index ae4e8c58b2..f7bc47eb1b 100644
--- a/test/specs/new/list_loose_tasks.html
+++ b/test/specs/new/list_loose_tasks.html
@@ -9,4 +9,7 @@
 <p><input type="checkbox" disabled=""></p>
 <pre>Task2</pre>
 </li>
+<li>
+<p><input type="checkbox" disabled=""></p>
+</li>
 </ul>
diff --git a/test/specs/new/list_loose_tasks.md b/test/specs/new/list_loose_tasks.md
index cb1cab5b0d..7ed70e1b6c 100644
--- a/test/specs/new/list_loose_tasks.md
+++ b/test/specs/new/list_loose_tasks.md
@@ -2,3 +2,5 @@
 - [x] Task1
 
 - [ ] <pre>Task2</pre>
+
+- [ ] 

EOF_0a81fa3000d2
: '>>>>> Start Test Output'
./node_modules/.bin/jasmine --no-color --config=jasmine.json
: '>>>>> End Test Output'
git checkout 0cd85983ce810c5f833c939cdf66b341dc2d6825 test/specs/new/list_loose_tasks.html test/specs/new/list_loose_tasks.md
