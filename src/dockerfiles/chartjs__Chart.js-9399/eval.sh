#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 31be6100015fbca3b639bcd63f9d03b52f21e171 test/fixtures/controller.bar/bar-base-value.png test/fixtures/controller.bar/baseLine/bottom.png test/fixtures/controller.bar/baseLine/left.png test/fixtures/controller.bar/baseLine/mid-x.png test/fixtures/controller.bar/baseLine/mid-y.png test/fixtures/controller.bar/baseLine/right.png test/fixtures/controller.bar/baseLine/top.png test/fixtures/controller.bar/baseLine/value-x.png test/fixtures/controller.bar/baseLine/value-y.png test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png test/fixtures/controller.bar/borderRadius/border-radius.png test/fixtures/controller.bar/borderWidth/indexable.png test/fixtures/controller.bar/borderWidth/object.png test/fixtures/controller.bar/borderWidth/value.png test/fixtures/controller.bar/horizontal-borders.png test/fixtures/scale.category/ticks-from-data.js test/fixtures/scale.category/ticks-from-data.png
mkdir -p test/fixtures/controller.bar
curl -o test/fixtures/controller.bar/bar-base-value.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/bar-base-value.png
chmod 777 test/fixtures/controller.bar/bar-base-value.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/bottom.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/baseLine/bottom.png
chmod 777 test/fixtures/controller.bar/baseLine/bottom.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/left.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/baseLine/left.png
chmod 777 test/fixtures/controller.bar/baseLine/left.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/mid-x.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/baseLine/mid-x.png
chmod 777 test/fixtures/controller.bar/baseLine/mid-x.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/mid-y.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/baseLine/mid-y.png
chmod 777 test/fixtures/controller.bar/baseLine/mid-y.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/right.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/baseLine/right.png
chmod 777 test/fixtures/controller.bar/baseLine/right.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/top.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/baseLine/top.png
chmod 777 test/fixtures/controller.bar/baseLine/top.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/value-x.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/baseLine/value-x.png
chmod 777 test/fixtures/controller.bar/baseLine/value-x.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/value-y.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/baseLine/value-y.png
chmod 777 test/fixtures/controller.bar/baseLine/value-y.png
mkdir -p test/fixtures/controller.bar/borderColor
curl -o test/fixtures/controller.bar/borderColor/border+dpr.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/borderColor/border+dpr.png
chmod 777 test/fixtures/controller.bar/borderColor/border+dpr.png
mkdir -p test/fixtures/controller.bar/borderRadius
curl -o test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png
chmod 777 test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png
mkdir -p test/fixtures/controller.bar/borderRadius
curl -o test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png
chmod 777 test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png
mkdir -p test/fixtures/controller.bar/borderRadius
curl -o test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png
chmod 777 test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png
mkdir -p test/fixtures/controller.bar/borderRadius
curl -o test/fixtures/controller.bar/borderRadius/border-radius.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/borderRadius/border-radius.png
chmod 777 test/fixtures/controller.bar/borderRadius/border-radius.png
mkdir -p test/fixtures/controller.bar/borderRadius
curl -o test/fixtures/controller.bar/borderRadius/no-spacing.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/borderRadius/no-spacing.png
chmod 777 test/fixtures/controller.bar/borderRadius/no-spacing.png
mkdir -p test/fixtures/controller.bar/borderWidth
curl -o test/fixtures/controller.bar/borderWidth/indexable.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/borderWidth/indexable.png
chmod 777 test/fixtures/controller.bar/borderWidth/indexable.png
mkdir -p test/fixtures/controller.bar/borderWidth
curl -o test/fixtures/controller.bar/borderWidth/object.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/borderWidth/object.png
chmod 777 test/fixtures/controller.bar/borderWidth/object.png
mkdir -p test/fixtures/controller.bar/borderWidth
curl -o test/fixtures/controller.bar/borderWidth/value.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/borderWidth/value.png
chmod 777 test/fixtures/controller.bar/borderWidth/value.png
mkdir -p test/fixtures/controller.bar
curl -o test/fixtures/controller.bar/horizontal-borders.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/controller.bar/horizontal-borders.png
chmod 777 test/fixtures/controller.bar/horizontal-borders.png
mkdir -p test/fixtures/scale.category
curl -o test/fixtures/scale.category/ticks-from-data.png https://raw.githubusercontent.com/chartjs/Chart.js/266720899fad3f96dc948445e2ea0209eb743b2b/test/fixtures/scale.category/ticks-from-data.png
chmod 777 test/fixtures/scale.category/ticks-from-data.png
git apply --verbose --reject - <<'EOF_586037dcb98e'
diff --git a/test/fixtures/controller.bar/bar-base-value.png b/test/fixtures/controller.bar/bar-base-value.png
index 5d5986bdf86..87219e676a9 100644
Binary files a/test/fixtures/controller.bar/bar-base-value.png and b/test/fixtures/controller.bar/bar-base-value.png differ
diff --git a/test/fixtures/controller.bar/baseLine/bottom.png b/test/fixtures/controller.bar/baseLine/bottom.png
index d7107153bb0..87e982e1e23 100644
Binary files a/test/fixtures/controller.bar/baseLine/bottom.png and b/test/fixtures/controller.bar/baseLine/bottom.png differ
diff --git a/test/fixtures/controller.bar/baseLine/left.png b/test/fixtures/controller.bar/baseLine/left.png
index ca5e1227b5c..19b328c3bee 100644
Binary files a/test/fixtures/controller.bar/baseLine/left.png and b/test/fixtures/controller.bar/baseLine/left.png differ
diff --git a/test/fixtures/controller.bar/baseLine/mid-x.png b/test/fixtures/controller.bar/baseLine/mid-x.png
index 1f4feb2e36b..d6b37767769 100644
Binary files a/test/fixtures/controller.bar/baseLine/mid-x.png and b/test/fixtures/controller.bar/baseLine/mid-x.png differ
diff --git a/test/fixtures/controller.bar/baseLine/mid-y.png b/test/fixtures/controller.bar/baseLine/mid-y.png
index 88c21a15374..646fd805184 100644
Binary files a/test/fixtures/controller.bar/baseLine/mid-y.png and b/test/fixtures/controller.bar/baseLine/mid-y.png differ
diff --git a/test/fixtures/controller.bar/baseLine/right.png b/test/fixtures/controller.bar/baseLine/right.png
index 2ad1dfdb3ea..2f98f893a72 100644
Binary files a/test/fixtures/controller.bar/baseLine/right.png and b/test/fixtures/controller.bar/baseLine/right.png differ
diff --git a/test/fixtures/controller.bar/baseLine/top.png b/test/fixtures/controller.bar/baseLine/top.png
index 8472c0fbf0d..e04b9b0bd7e 100644
Binary files a/test/fixtures/controller.bar/baseLine/top.png and b/test/fixtures/controller.bar/baseLine/top.png differ
diff --git a/test/fixtures/controller.bar/baseLine/value-x.png b/test/fixtures/controller.bar/baseLine/value-x.png
index 1fd0161a55f..23ed06dd6aa 100644
Binary files a/test/fixtures/controller.bar/baseLine/value-x.png and b/test/fixtures/controller.bar/baseLine/value-x.png differ
diff --git a/test/fixtures/controller.bar/baseLine/value-y.png b/test/fixtures/controller.bar/baseLine/value-y.png
index 15fe7871013..7063fd102a1 100644
Binary files a/test/fixtures/controller.bar/baseLine/value-y.png and b/test/fixtures/controller.bar/baseLine/value-y.png differ
diff --git a/test/fixtures/controller.bar/borderColor/border+dpr.js b/test/fixtures/controller.bar/borderColor/border+dpr.js
new file mode 100644
index 00000000000..3fa0b53c017
--- /dev/null
+++ b/test/fixtures/controller.bar/borderColor/border+dpr.js
@@ -0,0 +1,35 @@
+module.exports = {
+  threshold: 0,
+  tolerance: 0,
+  config: {
+    type: 'bar',
+    data: {
+      labels: [0, 1, 2, 3, 4, 5, 6],
+      datasets: [
+        {
+          // option in dataset
+          data: [5, 4, 3, 2, 3, 4, 5],
+        },
+      ]
+    },
+    options: {
+      events: [],
+      devicePixelRatio: 1.5,
+      barPercentage: 1,
+      categoryPercentage: 1,
+      backgroundColor: 'black',
+      borderColor: 'black',
+      borderWidth: 8,
+      scales: {
+        x: {display: false},
+        y: {display: false}
+      }
+    }
+  },
+  options: {
+    canvas: {
+      height: 256,
+      width: 501
+    }
+  }
+};
diff --git a/test/fixtures/controller.bar/borderColor/border+dpr.png b/test/fixtures/controller.bar/borderColor/border+dpr.png
new file mode 100644
index 00000000000..0fae394e8f9
Binary files /dev/null and b/test/fixtures/controller.bar/borderColor/border+dpr.png differ
diff --git a/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png
index 3aff7387b1d..0c96f07f537 100644
Binary files a/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png and b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png differ
diff --git a/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png
index 24eb8e0ea00..2635b2792ab 100644
Binary files a/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png and b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png differ
diff --git a/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png
index 2b8af4bb8d0..13b82c32a89 100644
Binary files a/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png and b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png differ
diff --git a/test/fixtures/controller.bar/borderRadius/border-radius.png b/test/fixtures/controller.bar/borderRadius/border-radius.png
index 68e7c0dd291..ec5e8a63d31 100644
Binary files a/test/fixtures/controller.bar/borderRadius/border-radius.png and b/test/fixtures/controller.bar/borderRadius/border-radius.png differ
diff --git a/test/fixtures/controller.bar/borderRadius/no-spacing.js b/test/fixtures/controller.bar/borderRadius/no-spacing.js
new file mode 100644
index 00000000000..53a0fc47fbe
--- /dev/null
+++ b/test/fixtures/controller.bar/borderRadius/no-spacing.js
@@ -0,0 +1,33 @@
+module.exports = {
+  threshold: 0.01,
+  config: {
+    type: 'bar',
+    data: {
+      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
+      datasets: [
+        {
+          data: [9, 25, 13, 17, 12, 21, 20, 19, 6, 12, 14, 20],
+          categoryPercentage: 1,
+          barPercentage: 1,
+          backgroundColor: '#2E5C76',
+          borderWidth: 2,
+          borderColor: '#377395',
+          borderRadius: 5,
+        },
+      ]
+    },
+    options: {
+      devicePixelRatio: 1.25,
+      scales: {
+        x: {display: false},
+        y: {display: false}
+      }
+    }
+  },
+  options: {
+    canvas: {
+      height: 256,
+      width: 512
+    }
+  }
+};
diff --git a/test/fixtures/controller.bar/borderRadius/no-spacing.png b/test/fixtures/controller.bar/borderRadius/no-spacing.png
new file mode 100644
index 00000000000..b630cf5ca8a
Binary files /dev/null and b/test/fixtures/controller.bar/borderRadius/no-spacing.png differ
diff --git a/test/fixtures/controller.bar/borderWidth/indexable.png b/test/fixtures/controller.bar/borderWidth/indexable.png
index d3f1b85c867..88428927ec1 100644
Binary files a/test/fixtures/controller.bar/borderWidth/indexable.png and b/test/fixtures/controller.bar/borderWidth/indexable.png differ
diff --git a/test/fixtures/controller.bar/borderWidth/object.png b/test/fixtures/controller.bar/borderWidth/object.png
index 04576006af4..3b36d96cb2f 100644
Binary files a/test/fixtures/controller.bar/borderWidth/object.png and b/test/fixtures/controller.bar/borderWidth/object.png differ
diff --git a/test/fixtures/controller.bar/borderWidth/value.png b/test/fixtures/controller.bar/borderWidth/value.png
index af89232e972..58fec25d81b 100644
Binary files a/test/fixtures/controller.bar/borderWidth/value.png and b/test/fixtures/controller.bar/borderWidth/value.png differ
diff --git a/test/fixtures/controller.bar/horizontal-borders.png b/test/fixtures/controller.bar/horizontal-borders.png
index 73adeead561..96f16777ae3 100644
Binary files a/test/fixtures/controller.bar/horizontal-borders.png and b/test/fixtures/controller.bar/horizontal-borders.png differ
diff --git a/test/fixtures/scale.category/ticks-from-data.js b/test/fixtures/scale.category/ticks-from-data.js
index d002927420d..a82f643a332 100644
--- a/test/fixtures/scale.category/ticks-from-data.js
+++ b/test/fixtures/scale.category/ticks-from-data.js
@@ -4,19 +4,13 @@ module.exports = {
     type: 'bar',
     data: {
       datasets: [{
-        data: [10, 5, 0, 25, 78]
+        data: [10, 5, 0, 25, 78],
+        backgroundColor: 'transparent'
       }],
       labels: ['tick1', 'tick2', 'tick3', 'tick4', 'tick5']
     },
     options: {
       indexAxis: 'y',
-      elements: {
-        bar: {
-          backgroundColor: '#AAAAAA80',
-          borderColor: '#80808080',
-          borderWidth: {bottom: 6, left: 15, top: 6, right: 15}
-        }
-      },
       scales: {
         x: {display: false},
         y: {display: true}
@@ -24,6 +18,10 @@ module.exports = {
     }
   },
   options: {
-    spriteText: true
+    spriteText: true,
+    canvas: {
+      width: 128,
+      height: 256
+    }
   }
 };
diff --git a/test/fixtures/scale.category/ticks-from-data.png b/test/fixtures/scale.category/ticks-from-data.png
index 4a65b49fe11..6ce9dc90cec 100644
Binary files a/test/fixtures/scale.category/ticks-from-data.png and b/test/fixtures/scale.category/ticks-from-data.png differ

EOF_586037dcb98e
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout 31be6100015fbca3b639bcd63f9d03b52f21e171 test/fixtures/controller.bar/bar-base-value.png test/fixtures/controller.bar/baseLine/bottom.png test/fixtures/controller.bar/baseLine/left.png test/fixtures/controller.bar/baseLine/mid-x.png test/fixtures/controller.bar/baseLine/mid-y.png test/fixtures/controller.bar/baseLine/right.png test/fixtures/controller.bar/baseLine/top.png test/fixtures/controller.bar/baseLine/value-x.png test/fixtures/controller.bar/baseLine/value-y.png test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png test/fixtures/controller.bar/borderRadius/border-radius.png test/fixtures/controller.bar/borderWidth/indexable.png test/fixtures/controller.bar/borderWidth/object.png test/fixtures/controller.bar/borderWidth/value.png test/fixtures/controller.bar/horizontal-borders.png test/fixtures/scale.category/ticks-from-data.js test/fixtures/scale.category/ticks-from-data.png
