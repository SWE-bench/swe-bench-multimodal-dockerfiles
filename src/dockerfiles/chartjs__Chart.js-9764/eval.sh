#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 12c5f9a8396f2a472f331ef772d6c7ba5cd62513 test/fixtures/controller.bubble/clip.png test/fixtures/controller.bubble/padding.png test/fixtures/controller.bubble/point-style.png test/fixtures/controller.bubble/radius-data.png test/fixtures/core.scale/border-behind-elements.png
mkdir -p test/fixtures/controller.bubble
curl -o test/fixtures/controller.bubble/clip.png https://raw.githubusercontent.com/chartjs/Chart.js/658bc3cc37171d98880fa315eccbbe21be69cdc6/test/fixtures/controller.bubble/clip.png
chmod 777 test/fixtures/controller.bubble/clip.png
mkdir -p test/fixtures/controller.bubble
curl -o test/fixtures/controller.bubble/hover-radius-zero.png https://raw.githubusercontent.com/chartjs/Chart.js/658bc3cc37171d98880fa315eccbbe21be69cdc6/test/fixtures/controller.bubble/hover-radius-zero.png
chmod 777 test/fixtures/controller.bubble/hover-radius-zero.png
mkdir -p test/fixtures/controller.bubble
curl -o test/fixtures/controller.bubble/padding.png https://raw.githubusercontent.com/chartjs/Chart.js/658bc3cc37171d98880fa315eccbbe21be69cdc6/test/fixtures/controller.bubble/padding.png
chmod 777 test/fixtures/controller.bubble/padding.png
mkdir -p test/fixtures/controller.bubble
curl -o test/fixtures/controller.bubble/point-style.png https://raw.githubusercontent.com/chartjs/Chart.js/658bc3cc37171d98880fa315eccbbe21be69cdc6/test/fixtures/controller.bubble/point-style.png
chmod 777 test/fixtures/controller.bubble/point-style.png
mkdir -p test/fixtures/controller.bubble
curl -o test/fixtures/controller.bubble/radius-data.png https://raw.githubusercontent.com/chartjs/Chart.js/658bc3cc37171d98880fa315eccbbe21be69cdc6/test/fixtures/controller.bubble/radius-data.png
chmod 777 test/fixtures/controller.bubble/radius-data.png
mkdir -p test/fixtures/core.scale
curl -o test/fixtures/core.scale/border-behind-elements.png https://raw.githubusercontent.com/chartjs/Chart.js/658bc3cc37171d98880fa315eccbbe21be69cdc6/test/fixtures/core.scale/border-behind-elements.png
chmod 777 test/fixtures/core.scale/border-behind-elements.png
git apply --verbose --reject - <<'EOF_f1477764a514'
diff --git a/test/fixtures/controller.bubble/clip.png b/test/fixtures/controller.bubble/clip.png
index 6ce0ce1247c..7214e4e209c 100644
Binary files a/test/fixtures/controller.bubble/clip.png and b/test/fixtures/controller.bubble/clip.png differ
diff --git a/test/fixtures/controller.bubble/hover-radius-zero.js b/test/fixtures/controller.bubble/hover-radius-zero.js
new file mode 100644
index 00000000000..3628577710b
--- /dev/null
+++ b/test/fixtures/controller.bubble/hover-radius-zero.js
@@ -0,0 +1,48 @@
+module.exports = {
+  config: {
+    type: 'bubble',
+    data: {
+      labels: [2, 2, 2, 2],
+      datasets: [{
+        data: [
+          [1, 1],
+          [1, 2],
+          [1, 3, 20],
+          [1, 4, 20]
+        ]
+      }, {
+        data: [1, 2, 3, 4]
+      }, {
+        data: [{x: 3, y: 1}, {x: 3, y: 2}, {x: 3, y: 3, r: 15}, {x: 3, y: 4, r: 15}]
+      }]
+    },
+    options: {
+      events: [],
+      radius: 10,
+      hoverRadius: 0,
+      backgroundColor: 'blue',
+      hoverBackgroundColor: 'red',
+      scales: {
+        x: {display: false, bounds: 'data'},
+        y: {display: false}
+      },
+      layout: {
+        padding: 24
+      }
+    }
+  },
+  options: {
+    canvas: {
+      height: 256,
+      width: 256
+    },
+    run(chart) {
+      chart.setActiveElements([
+        {datasetIndex: 0, index: 1}, {datasetIndex: 0, index: 2},
+        {datasetIndex: 1, index: 1}, {datasetIndex: 1, index: 2},
+        {datasetIndex: 2, index: 1}, {datasetIndex: 2, index: 2},
+      ]);
+      chart.update();
+    }
+  }
+};
diff --git a/test/fixtures/controller.bubble/hover-radius-zero.png b/test/fixtures/controller.bubble/hover-radius-zero.png
new file mode 100644
index 00000000000..d86d7ddcaee
Binary files /dev/null and b/test/fixtures/controller.bubble/hover-radius-zero.png differ
diff --git a/test/fixtures/controller.bubble/padding.png b/test/fixtures/controller.bubble/padding.png
index 6a03d5c08dc..583120e4819 100644
Binary files a/test/fixtures/controller.bubble/padding.png and b/test/fixtures/controller.bubble/padding.png differ
diff --git a/test/fixtures/controller.bubble/point-style.png b/test/fixtures/controller.bubble/point-style.png
index d949141d81d..1957aba0956 100644
Binary files a/test/fixtures/controller.bubble/point-style.png and b/test/fixtures/controller.bubble/point-style.png differ
diff --git a/test/fixtures/controller.bubble/radius-data.png b/test/fixtures/controller.bubble/radius-data.png
index ac819c21e45..d565dbdcffa 100644
Binary files a/test/fixtures/controller.bubble/radius-data.png and b/test/fixtures/controller.bubble/radius-data.png differ
diff --git a/test/fixtures/core.scale/border-behind-elements.png b/test/fixtures/core.scale/border-behind-elements.png
index d3f37719d7e..f4a9e019b53 100644
Binary files a/test/fixtures/core.scale/border-behind-elements.png and b/test/fixtures/core.scale/border-behind-elements.png differ

EOF_f1477764a514
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout 12c5f9a8396f2a472f331ef772d6c7ba5cd62513 test/fixtures/controller.bubble/clip.png test/fixtures/controller.bubble/padding.png test/fixtures/controller.bubble/point-style.png test/fixtures/controller.bubble/radius-data.png test/fixtures/core.scale/border-behind-elements.png
