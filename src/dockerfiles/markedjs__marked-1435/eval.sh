#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout ae9484d35939d2bf72e038c0977cb2eeab4495f7 test/specs/marked/marked.json
git apply --verbose --reject - <<'EOF_b4fc3b39e458'
diff --git a/test/specs/marked/marked.json b/test/specs/marked/marked.json
index 5f46f53640..5dd1a065c8 100644
--- a/test/specs/marked/marked.json
+++ b/test/specs/marked/marked.json
@@ -113,10 +113,16 @@
     "html": "<p><strong><a href=\"mailto:test@test.com\">test@test.com</a></strong></p>",
     "example": 1347
   },
-  {  
+  {
     "section": "Emphasis extra tests",
     "markdown": "_test_. _test_: _test_! _test_? _test_-",
     "html": "<p><em>test</em>. <em>test</em>: <em>test</em>! <em>test</em>? <em>test</em>-</p>",
     "example": 15
+  },
+  {
+    "section": "Links",
+    "markdown": "[One](https://example.com/1) ([Two](https://example.com/2)) [Three](https://example.com/3)",
+    "html": "<p><a href=\"https://example.com/1\">One</a> (<a href=\"https://example.com/2\">Two</a>) <a href=\"https://example.com/3\">Three</a></p>",
+    "example": 16
   }
 ]

EOF_b4fc3b39e458
: '>>>>> Start Test Output'
./node_modules/.bin/jasmine --no-color --config=jasmine.json
: '>>>>> End Test Output'
git checkout ae9484d35939d2bf72e038c0977cb2eeab4495f7 test/specs/marked/marked.json
