#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout ba84cc5c2aaf500739b202702fac24da74ede50d test/fixtures/core.scale/ticks-mirror.png
mkdir -p test/fixtures/core.scale
curl -o test/fixtures/core.scale/ticks-mirror-x.png https://raw.githubusercontent.com/chartjs/Chart.js/fbd999d4ec922713155cbb7b2c91a72281673c76/test/fixtures/core.scale/ticks-mirror-x.png
chmod 777 test/fixtures/core.scale/ticks-mirror-x.png
mkdir -p test/fixtures/core.scale
curl -o test/fixtures/core.scale/ticks-mirror.png https://raw.githubusercontent.com/chartjs/Chart.js/fbd999d4ec922713155cbb7b2c91a72281673c76/test/fixtures/core.scale/ticks-mirror.png
chmod 777 test/fixtures/core.scale/ticks-mirror.png
git apply --verbose --reject - <<'EOF_5d375aa9c1f5'
diff --git a/test/fixtures/core.scale/ticks-mirror-x.js b/test/fixtures/core.scale/ticks-mirror-x.js
new file mode 100644
index 00000000000..ec151e58031
--- /dev/null
+++ b/test/fixtures/core.scale/ticks-mirror-x.js
@@ -0,0 +1,30 @@
+module.exports = {
+  config: {
+    type: 'line',
+    data: {
+      datasets: [{
+        data: [1, -1, 3],
+      }],
+      labels: ['Label1', 'Label2', 'Label3']
+    },
+    options: {
+      scales: {
+        x: {
+          ticks: {
+            mirror: true
+          }
+        },
+        y: {
+          display: false
+        }
+      }
+    }
+  },
+  options: {
+    spriteText: true,
+    canvas: {
+      height: 256,
+      width: 512
+    }
+  }
+};
diff --git a/test/fixtures/core.scale/ticks-mirror-x.png b/test/fixtures/core.scale/ticks-mirror-x.png
new file mode 100644
index 00000000000..e9fe6537c47
Binary files /dev/null and b/test/fixtures/core.scale/ticks-mirror-x.png differ
diff --git a/test/fixtures/core.scale/ticks-mirror.png b/test/fixtures/core.scale/ticks-mirror.png
index dc483b51637..35fba6e5218 100644
Binary files a/test/fixtures/core.scale/ticks-mirror.png and b/test/fixtures/core.scale/ticks-mirror.png differ

EOF_5d375aa9c1f5
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout ba84cc5c2aaf500739b202702fac24da74ede50d test/fixtures/core.scale/ticks-mirror.png
