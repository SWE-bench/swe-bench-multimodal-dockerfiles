#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout c35d0c6e48ece06b2f420e3804c5f7267820d129 test/fixtures/controller.doughnut/single-slice-circumference-405.png
mkdir -p test/fixtures/controller.doughnut
curl -o test/fixtures/controller.doughnut/single-slice-circumference-405.png https://raw.githubusercontent.com/chartjs/Chart.js/ec852acd62f04c73dd38afd13cbce117737b2f75/test/fixtures/controller.doughnut/single-slice-circumference-405.png
chmod 777 test/fixtures/controller.doughnut/single-slice-circumference-405.png
mkdir -p test/fixtures/controller.doughnut
curl -o test/fixtures/controller.doughnut/single-slice-offset.png https://raw.githubusercontent.com/chartjs/Chart.js/ec852acd62f04c73dd38afd13cbce117737b2f75/test/fixtures/controller.doughnut/single-slice-offset.png
chmod 777 test/fixtures/controller.doughnut/single-slice-offset.png
git apply --verbose --reject - <<'EOF_64c159a8f417'
diff --git a/test/fixtures/controller.doughnut/single-slice-circumference-405.png b/test/fixtures/controller.doughnut/single-slice-circumference-405.png
index 0591cca9425..db4e2523509 100644
Binary files a/test/fixtures/controller.doughnut/single-slice-circumference-405.png and b/test/fixtures/controller.doughnut/single-slice-circumference-405.png differ
diff --git a/test/fixtures/controller.doughnut/single-slice-offset.js b/test/fixtures/controller.doughnut/single-slice-offset.js
new file mode 100644
index 00000000000..d2a9ace0c27
--- /dev/null
+++ b/test/fixtures/controller.doughnut/single-slice-offset.js
@@ -0,0 +1,16 @@
+module.exports = {
+  config: {
+    type: 'doughnut',
+    data: {
+      labels: ['A'],
+      datasets: [{
+        data: [385],
+        backgroundColor: 'rgba(0,0,0,0.3)',
+        borderColor: 'rgba(0,0,0,0.5)',
+      }]
+    },
+    options: {
+      offset: 20
+    }
+  }
+};
diff --git a/test/fixtures/controller.doughnut/single-slice-offset.png b/test/fixtures/controller.doughnut/single-slice-offset.png
new file mode 100644
index 00000000000..b38c18b8033
Binary files /dev/null and b/test/fixtures/controller.doughnut/single-slice-offset.png differ

EOF_64c159a8f417
: '>>>>> Start Test Output'
pnpm install
pnpm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.cjs --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout c35d0c6e48ece06b2f420e3804c5f7267820d129 test/fixtures/controller.doughnut/single-slice-circumference-405.png
