#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout ba84cc5c2aaf500739b202702fac24da74ede50d test/fixtures/core.scale/x-axis-position-dynamic.png
mkdir -p test/fixtures/core.scale
curl -o test/fixtures/core.scale/x-axis-position-dynamic-margin.png https://raw.githubusercontent.com/chartjs/Chart.js/2f88e1b010c40c86aa93c67f91cb8b1c7f260195/test/fixtures/core.scale/x-axis-position-dynamic-margin.png
chmod 777 test/fixtures/core.scale/x-axis-position-dynamic-margin.png
mkdir -p test/fixtures/core.scale
curl -o test/fixtures/core.scale/x-axis-position-dynamic.png https://raw.githubusercontent.com/chartjs/Chart.js/2f88e1b010c40c86aa93c67f91cb8b1c7f260195/test/fixtures/core.scale/x-axis-position-dynamic.png
chmod 777 test/fixtures/core.scale/x-axis-position-dynamic.png
git apply --verbose --reject - <<'EOF_7e3ab62fe08d'
diff --git a/test/fixtures/core.scale/x-axis-position-dynamic-margin.js b/test/fixtures/core.scale/x-axis-position-dynamic-margin.js
new file mode 100644
index 00000000000..7e8bf6e6e79
--- /dev/null
+++ b/test/fixtures/core.scale/x-axis-position-dynamic-margin.js
@@ -0,0 +1,27 @@
+module.exports = {
+  config: {
+    type: 'line',
+    options: {
+      scales: {
+        x: {
+          labels: ['Left Label', 'Center Label', 'Right Label'],
+          position: {
+            y: 30
+          },
+        },
+        y: {
+          display: false,
+          min: -100,
+          max: 100,
+        }
+      }
+    }
+  },
+  options: {
+    canvas: {
+      height: 256,
+      width: 512
+    },
+    spriteText: true
+  }
+};
diff --git a/test/fixtures/core.scale/x-axis-position-dynamic-margin.png b/test/fixtures/core.scale/x-axis-position-dynamic-margin.png
new file mode 100644
index 00000000000..3dffa316dd7
Binary files /dev/null and b/test/fixtures/core.scale/x-axis-position-dynamic-margin.png differ
diff --git a/test/fixtures/core.scale/x-axis-position-dynamic.png b/test/fixtures/core.scale/x-axis-position-dynamic.png
index 62fc3ec86e7..bbebdd33b7e 100644
Binary files a/test/fixtures/core.scale/x-axis-position-dynamic.png and b/test/fixtures/core.scale/x-axis-position-dynamic.png differ

EOF_7e3ab62fe08d
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout ba84cc5c2aaf500739b202702fac24da74ede50d test/fixtures/core.scale/x-axis-position-dynamic.png
