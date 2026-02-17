#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 91628c144944029505de093c43733961ab4f420f test/fixtures/core.layouts/long-labels.png test/fixtures/scale.time/invalid-data.png test/specs/core.controller.tests.js
mkdir -p test/fixtures/core.layouts
curl -o test/fixtures/core.layouts/long-labels.png https://raw.githubusercontent.com/chartjs/Chart.js/15613ba048b1440f34032c8a5d9a0c8d1eb73e2e/test/fixtures/core.layouts/long-labels.png
chmod 777 test/fixtures/core.layouts/long-labels.png
mkdir -p test/fixtures/core.layouts
curl -o test/fixtures/core.layouts/refit-vertical-boxes.png https://raw.githubusercontent.com/chartjs/Chart.js/15613ba048b1440f34032c8a5d9a0c8d1eb73e2e/test/fixtures/core.layouts/refit-vertical-boxes.png
chmod 777 test/fixtures/core.layouts/refit-vertical-boxes.png
mkdir -p test/fixtures/scale.time
curl -o test/fixtures/scale.time/invalid-data.png https://raw.githubusercontent.com/chartjs/Chart.js/15613ba048b1440f34032c8a5d9a0c8d1eb73e2e/test/fixtures/scale.time/invalid-data.png
chmod 777 test/fixtures/scale.time/invalid-data.png
git apply --verbose --reject - <<'EOF_ab8cafaebf00'
diff --git a/test/fixtures/core.layouts/long-labels.png b/test/fixtures/core.layouts/long-labels.png
index ed33676753e..c12a70a8711 100644
Binary files a/test/fixtures/core.layouts/long-labels.png and b/test/fixtures/core.layouts/long-labels.png differ
diff --git a/test/fixtures/core.layouts/refit-vertical-boxes.js b/test/fixtures/core.layouts/refit-vertical-boxes.js
new file mode 100644
index 00000000000..b49d7885bdc
--- /dev/null
+++ b/test/fixtures/core.layouts/refit-vertical-boxes.js
@@ -0,0 +1,52 @@
+module.exports = {
+  config: {
+    type: 'line',
+    data: {
+      labels: [
+        'Aaron',
+        'Adam',
+        'Albert',
+        'Alex',
+        'Allan',
+        'Aman',
+        'Anthony',
+        'Autoenrolment',
+        'Avril',
+        'Bernard'
+      ],
+      datasets: [{
+        backgroundColor: 'rgba(252,233,79,0.5)',
+        borderColor: 'rgba(252,233,79,1)',
+        borderWidth: 1,
+        data: [101,
+          185,
+          24,
+          311,
+          17,
+          21,
+          462,
+          340,
+          140,
+          24
+        ]
+      }]
+    },
+    options: {
+      maintainAspectRatio: false,
+      plugins: {
+        legend: true,
+        title: {
+          display: true,
+          text: 'test'
+        }
+      }
+    }
+  },
+  options: {
+    spriteText: true,
+    canvas: {
+      height: 185,
+      width: 185
+    }
+  }
+};
diff --git a/test/fixtures/core.layouts/refit-vertical-boxes.png b/test/fixtures/core.layouts/refit-vertical-boxes.png
new file mode 100644
index 00000000000..f45a406342a
Binary files /dev/null and b/test/fixtures/core.layouts/refit-vertical-boxes.png differ
diff --git a/test/fixtures/scale.time/invalid-data.png b/test/fixtures/scale.time/invalid-data.png
index 1cdd9b95d95..2257064a271 100644
Binary files a/test/fixtures/scale.time/invalid-data.png and b/test/fixtures/scale.time/invalid-data.png differ
diff --git a/test/specs/core.controller.tests.js b/test/specs/core.controller.tests.js
index 2fb13eb4bae..c0f1b2ba850 100644
--- a/test/specs/core.controller.tests.js
+++ b/test/specs/core.controller.tests.js
@@ -1430,14 +1430,16 @@ describe('Chart', function() {
       update: [
         'beforeUpdate',
         'beforeLayout',
-        'beforeDataLimits',
+        'beforeDataLimits', // y-axis fit
         'afterDataLimits',
         'beforeBuildTicks',
         'afterBuildTicks',
-        'beforeDataLimits',
+        'beforeDataLimits', // x-axis fit
         'afterDataLimits',
         'beforeBuildTicks',
         'afterBuildTicks',
+        'beforeBuildTicks', // y-axis re-fit
+        'afterBuildTicks',
         'afterLayout',
         'beforeDatasetsUpdate',
         'beforeDatasetUpdate',

EOF_ab8cafaebf00
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout 91628c144944029505de093c43733961ab4f420f test/fixtures/core.layouts/long-labels.png test/fixtures/scale.time/invalid-data.png test/specs/core.controller.tests.js
