#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 52151068bdc7e95150a189392fbd5ec0a48318f0 test/unit/io/files_input.js
git apply --verbose --reject - <<'EOF_c1e90ef1021a'
diff --git a/test/unit/assets/empty_lines.txt b/test/unit/assets/empty_lines.txt
new file mode 100644
index 0000000000..5a3b131ad7
--- /dev/null
+++ b/test/unit/assets/empty_lines.txt
@@ -0,0 +1,5 @@
+some of these
+
+lines
+
+are empty
diff --git a/test/unit/io/files_input.js b/test/unit/io/files_input.js
index 9b596c5b00..a351a1db70 100644
--- a/test/unit/io/files_input.js
+++ b/test/unit/io/files_input.js
@@ -240,6 +240,15 @@ suite('Files', function() {
       });
     });
 
+    test('should include empty strings', function() {
+      return new Promise(function(resolve, reject) {
+        myp5.loadStrings('unit/assets/empty_lines.txt', resolve, reject);
+      }).then(function(data) {
+        assert.isArray(data, 'Array passed to callback function');
+        assert.lengthOf(data, 6, 'length of data is 6');
+      });
+    });
+
     test('should call error callback function if provided', function() {
       return new Promise(function(resolve, reject) {
         myp5.loadStrings(

EOF_c1e90ef1021a
: '>>>>> Start Test Output'
sed -i 's/concurrency:[[:space:]]*[0-9][0-9]*/concurrency: 1/g' Gruntfile.js
stdbuf -o 1M ./node_modules/.bin/grunt test --quiet --force
: '>>>>> End Test Output'
git checkout 52151068bdc7e95150a189392fbd5ec0a48318f0 test/unit/io/files_input.js
