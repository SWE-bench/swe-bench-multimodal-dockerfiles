#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
echo "No test files to reset"
git apply --verbose --reject - <<'EOF_c757b40defcb'
diff --git a/test/specs/new/fences_following_list.html b/test/specs/new/fences_following_list.html
new file mode 100644
index 0000000000..e5b2a9f9e7
--- /dev/null
+++ b/test/specs/new/fences_following_list.html
@@ -0,0 +1,7 @@
+<ol>
+<li>abcd</li>
+</ol>
+<pre><code>if {
+
+}
+</code></pre>
diff --git a/test/specs/new/fences_following_list.md b/test/specs/new/fences_following_list.md
new file mode 100644
index 0000000000..f306891f9c
--- /dev/null
+++ b/test/specs/new/fences_following_list.md
@@ -0,0 +1,5 @@
+1. abcd
+```
+if {
+}
+```
diff --git a/test/specs/new/fences_with_blankline_following_list_0.html b/test/specs/new/fences_with_blankline_following_list_0.html
new file mode 100644
index 0000000000..cc77e8b936
--- /dev/null
+++ b/test/specs/new/fences_with_blankline_following_list_0.html
@@ -0,0 +1,23 @@
+<ol>
+<li>code with blankline</li>
+</ol>
+<pre><code>if {
+
+}
+</code></pre>
+<ol start="2">
+<li>code and text</li>
+</ol>
+<pre><code>if {
+
+}
+</code></pre>
+<p>text after fenced code block.</p>
+<ol start="3">
+<li>tilde</li>
+</ol>
+<pre><code>if {
+
+
+}
+</code></pre>
diff --git a/test/specs/new/fences_with_blankline_following_list_0.md b/test/specs/new/fences_with_blankline_following_list_0.md
new file mode 100644
index 0000000000..2ea9a26285
--- /dev/null
+++ b/test/specs/new/fences_with_blankline_following_list_0.md
@@ -0,0 +1,22 @@
+1. code with blankline
+```
+if {
+
+}
+```
+
+2. code and text
+```
+if {
+
+
+}
+```
+text after fenced code block.
+
+3. tilde
+~~~
+if {
+
+}
+~~~
diff --git a/test/specs/new/fences_with_blankline_following_list_1.html b/test/specs/new/fences_with_blankline_following_list_1.html
new file mode 100644
index 0000000000..31e59331ef
--- /dev/null
+++ b/test/specs/new/fences_with_blankline_following_list_1.html
@@ -0,0 +1,22 @@
+<ol>
+<li><p>code with blankline</p>
+<pre><code>if {
+
+}
+</code></pre>
+</li>
+<li><p>code and text</p>
+<pre><code>if {
+
+}
+</code></pre>
+<p>text after fenced code block.</p>
+</li>
+<li><p>tilde</p>
+<pre><code>if {
+
+
+}
+</code></pre>
+</li>
+</ol>
diff --git a/test/specs/new/fences_with_blankline_following_list_1.md b/test/specs/new/fences_with_blankline_following_list_1.md
new file mode 100644
index 0000000000..5f356a8aa8
--- /dev/null
+++ b/test/specs/new/fences_with_blankline_following_list_1.md
@@ -0,0 +1,23 @@
+1. code with blankline
+   ```
+   if {
+   
+   }
+   ```
+
+2. code and text
+   ```
+   if {
+   
+   
+   }
+   ```
+   text after fenced code block.
+
+3. tilde
+   ~~~
+   if {
+   
+   }
+   ~~~
+
diff --git a/test/specs/new/heading_following_list.html b/test/specs/new/heading_following_list.html
new file mode 100644
index 0000000000..b022d175ea
--- /dev/null
+++ b/test/specs/new/heading_following_list.html
@@ -0,0 +1,8 @@
+<h1 id="level1">level1</h1>
+<h2 id="level2">level2</h2>
+<h3 id="level3">level3</h3>
+<ul>
+  <li>foo=bar</li>
+  <li>foo2=bar2</li>
+</ul>
+<h3 id="level3-1">level3</h3>
diff --git a/test/specs/new/heading_following_list.md b/test/specs/new/heading_following_list.md
new file mode 100644
index 0000000000..215e308800
--- /dev/null
+++ b/test/specs/new/heading_following_list.md
@@ -0,0 +1,6 @@
+# level1
+## level2
+### level3
+- foo=bar
+- foo2=bar2
+### level3

EOF_c757b40defcb
: '>>>>> Start Test Output'
./node_modules/.bin/jasmine --no-color --config=jasmine.json
: '>>>>> End Test Output'
echo "No test files to reset"
