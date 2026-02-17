#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout c80b1450f55189a03bf3781e04559eb9b68f2129 test/fixtures/controller.bar/minBarLength/horizontal-neg.png test/fixtures/controller.bar/minBarLength/horizontal-pos.png test/fixtures/controller.bar/minBarLength/vertical-neg.png test/fixtures/controller.bar/minBarLength/vertical-pos.png
mkdir -p test/fixtures/controller.bar/minBarLength
curl -o test/fixtures/controller.bar/minBarLength/horizontal-neg.png https://raw.githubusercontent.com/chartjs/Chart.js/368ad3cf70414de7769852cf52693c08aaf9e05c/test/fixtures/controller.bar/minBarLength/horizontal-neg.png
chmod 777 test/fixtures/controller.bar/minBarLength/horizontal-neg.png
mkdir -p test/fixtures/controller.bar/minBarLength
curl -o test/fixtures/controller.bar/minBarLength/horizontal-pos.png https://raw.githubusercontent.com/chartjs/Chart.js/368ad3cf70414de7769852cf52693c08aaf9e05c/test/fixtures/controller.bar/minBarLength/horizontal-pos.png
chmod 777 test/fixtures/controller.bar/minBarLength/horizontal-pos.png
mkdir -p test/fixtures/controller.bar/minBarLength
curl -o test/fixtures/controller.bar/minBarLength/horizontal-stacked.png https://raw.githubusercontent.com/chartjs/Chart.js/368ad3cf70414de7769852cf52693c08aaf9e05c/test/fixtures/controller.bar/minBarLength/horizontal-stacked.png
chmod 777 test/fixtures/controller.bar/minBarLength/horizontal-stacked.png
mkdir -p test/fixtures/controller.bar/minBarLength
curl -o test/fixtures/controller.bar/minBarLength/vertical-neg.png https://raw.githubusercontent.com/chartjs/Chart.js/368ad3cf70414de7769852cf52693c08aaf9e05c/test/fixtures/controller.bar/minBarLength/vertical-neg.png
chmod 777 test/fixtures/controller.bar/minBarLength/vertical-neg.png
mkdir -p test/fixtures/controller.bar/minBarLength
curl -o test/fixtures/controller.bar/minBarLength/vertical-pos.png https://raw.githubusercontent.com/chartjs/Chart.js/368ad3cf70414de7769852cf52693c08aaf9e05c/test/fixtures/controller.bar/minBarLength/vertical-pos.png
chmod 777 test/fixtures/controller.bar/minBarLength/vertical-pos.png
mkdir -p test/fixtures/controller.bar/minBarLength
curl -o test/fixtures/controller.bar/minBarLength/vertical-stacked.png https://raw.githubusercontent.com/chartjs/Chart.js/368ad3cf70414de7769852cf52693c08aaf9e05c/test/fixtures/controller.bar/minBarLength/vertical-stacked.png
chmod 777 test/fixtures/controller.bar/minBarLength/vertical-stacked.png
git apply --verbose --reject - <<'EOF_b6feb4b8f1d5'
diff --git a/test/fixtures/controller.bar/minBarLength/horizontal-neg.png b/test/fixtures/controller.bar/minBarLength/horizontal-neg.png
index f012c82b6fb..16c6cabd522 100644
Binary files a/test/fixtures/controller.bar/minBarLength/horizontal-neg.png and b/test/fixtures/controller.bar/minBarLength/horizontal-neg.png differ
diff --git a/test/fixtures/controller.bar/minBarLength/horizontal-pos.png b/test/fixtures/controller.bar/minBarLength/horizontal-pos.png
index 0f89b8676ed..8d8b4724e9f 100644
Binary files a/test/fixtures/controller.bar/minBarLength/horizontal-pos.png and b/test/fixtures/controller.bar/minBarLength/horizontal-pos.png differ
diff --git a/test/fixtures/controller.bar/minBarLength/horizontal-stacked.js b/test/fixtures/controller.bar/minBarLength/horizontal-stacked.js
new file mode 100644
index 00000000000..8452ed6c8d6
--- /dev/null
+++ b/test/fixtures/controller.bar/minBarLength/horizontal-stacked.js
@@ -0,0 +1,43 @@
+module.exports = {
+  config: {
+    type: 'bar',
+    data: {
+      labels: [0, 1, 2, 3, 4],
+      datasets: [{
+        data: [0, 0.01, 30],
+        backgroundColor: '#00ff00',
+        borderColor: '#000',
+        borderWidth: 4,
+        minBarLength: 20,
+        xAxisID: 'x2',
+      }]
+    },
+    options: {
+      indexAxis: 'y',
+      scales: {
+        x: {
+          stack: 'demo',
+          ticks: {
+            display: false
+          }
+        },
+        x2: {
+          type: 'linear',
+          position: 'bottom',
+          stack: 'demo',
+          stackWeight: 1,
+          ticks: {
+            display: false
+          }
+        },
+        y: {display: false},
+      }
+    }
+  },
+  options: {
+    canvas: {
+      height: 512,
+      width: 512
+    }
+  }
+};
diff --git a/test/fixtures/controller.bar/minBarLength/horizontal-stacked.png b/test/fixtures/controller.bar/minBarLength/horizontal-stacked.png
new file mode 100644
index 00000000000..87da74832c7
Binary files /dev/null and b/test/fixtures/controller.bar/minBarLength/horizontal-stacked.png differ
diff --git a/test/fixtures/controller.bar/minBarLength/vertical-neg.png b/test/fixtures/controller.bar/minBarLength/vertical-neg.png
index 4d75f1cb238..debb97ee7d1 100644
Binary files a/test/fixtures/controller.bar/minBarLength/vertical-neg.png and b/test/fixtures/controller.bar/minBarLength/vertical-neg.png differ
diff --git a/test/fixtures/controller.bar/minBarLength/vertical-pos.png b/test/fixtures/controller.bar/minBarLength/vertical-pos.png
index 5561b4f3b3d..9a7b49e9cd9 100644
Binary files a/test/fixtures/controller.bar/minBarLength/vertical-pos.png and b/test/fixtures/controller.bar/minBarLength/vertical-pos.png differ
diff --git a/test/fixtures/controller.bar/minBarLength/vertical-stacked.js b/test/fixtures/controller.bar/minBarLength/vertical-stacked.js
new file mode 100644
index 00000000000..e09f12cd6ab
--- /dev/null
+++ b/test/fixtures/controller.bar/minBarLength/vertical-stacked.js
@@ -0,0 +1,42 @@
+module.exports = {
+  config: {
+    type: 'bar',
+    data: {
+      labels: [0, 1, 2, 3, 4],
+      datasets: [{
+        data: [0, 0.01, 30],
+        backgroundColor: '#00ff00',
+        borderColor: '#000',
+        borderWidth: 4,
+        minBarLength: 20,
+        yAxisID: 'y2',
+      }]
+    },
+    options: {
+      scales: {
+        x: {display: false},
+        y: {
+          stack: 'demo',
+          ticks: {
+            display: false
+          }
+        },
+        y2: {
+          type: 'linear',
+          position: 'left',
+          stack: 'demo',
+          stackWeight: 1,
+          ticks: {
+            display: false
+          }
+        }
+      }
+    }
+  },
+  options: {
+    canvas: {
+      height: 512,
+      width: 512
+    }
+  }
+};
diff --git a/test/fixtures/controller.bar/minBarLength/vertical-stacked.png b/test/fixtures/controller.bar/minBarLength/vertical-stacked.png
new file mode 100644
index 00000000000..ecef74b4430
Binary files /dev/null and b/test/fixtures/controller.bar/minBarLength/vertical-stacked.png differ

EOF_b6feb4b8f1d5
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout c80b1450f55189a03bf3781e04559eb9b68f2129 test/fixtures/controller.bar/minBarLength/horizontal-neg.png test/fixtures/controller.bar/minBarLength/horizontal-pos.png test/fixtures/controller.bar/minBarLength/vertical-neg.png test/fixtures/controller.bar/minBarLength/vertical-pos.png
