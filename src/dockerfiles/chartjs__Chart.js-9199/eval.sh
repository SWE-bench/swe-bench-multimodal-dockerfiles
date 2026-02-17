#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 599e23abfd1bb3545e350d62647f19911125872b test/fixtures/plugin.legend/label-textAlign/rtl-left.png test/fixtures/plugin.legend/label-textAlign/rtl-right.png
mkdir -p test/fixtures/plugin.legend/label-textAlign
curl -o test/fixtures/plugin.legend/label-textAlign/horizontal-left.png https://raw.githubusercontent.com/chartjs/Chart.js/063c62693f5f0e73a5882bd4f9b25bcb7ce54f40/test/fixtures/plugin.legend/label-textAlign/horizontal-left.png
chmod 777 test/fixtures/plugin.legend/label-textAlign/horizontal-left.png
mkdir -p test/fixtures/plugin.legend/label-textAlign
curl -o test/fixtures/plugin.legend/label-textAlign/horizontal-right.png https://raw.githubusercontent.com/chartjs/Chart.js/063c62693f5f0e73a5882bd4f9b25bcb7ce54f40/test/fixtures/plugin.legend/label-textAlign/horizontal-right.png
chmod 777 test/fixtures/plugin.legend/label-textAlign/horizontal-right.png
mkdir -p test/fixtures/plugin.legend/label-textAlign
curl -o test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-left.png https://raw.githubusercontent.com/chartjs/Chart.js/063c62693f5f0e73a5882bd4f9b25bcb7ce54f40/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-left.png
chmod 777 test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-left.png
mkdir -p test/fixtures/plugin.legend/label-textAlign
curl -o test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-right.png https://raw.githubusercontent.com/chartjs/Chart.js/063c62693f5f0e73a5882bd4f9b25bcb7ce54f40/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-right.png
chmod 777 test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-right.png
mkdir -p test/fixtures/plugin.legend/label-textAlign
curl -o test/fixtures/plugin.legend/label-textAlign/rtl-left.png https://raw.githubusercontent.com/chartjs/Chart.js/063c62693f5f0e73a5882bd4f9b25bcb7ce54f40/test/fixtures/plugin.legend/label-textAlign/rtl-left.png
chmod 777 test/fixtures/plugin.legend/label-textAlign/rtl-left.png
mkdir -p test/fixtures/plugin.legend/label-textAlign
curl -o test/fixtures/plugin.legend/label-textAlign/rtl-right.png https://raw.githubusercontent.com/chartjs/Chart.js/063c62693f5f0e73a5882bd4f9b25bcb7ce54f40/test/fixtures/plugin.legend/label-textAlign/rtl-right.png
chmod 777 test/fixtures/plugin.legend/label-textAlign/rtl-right.png
git apply --verbose --reject - <<'EOF_7d8df0e3a0cd'
diff --git a/test/fixtures/plugin.legend/label-textAlign/horizontal-left.js b/test/fixtures/plugin.legend/label-textAlign/horizontal-left.js
new file mode 100644
index 00000000000..46458c532e4
--- /dev/null
+++ b/test/fixtures/plugin.legend/label-textAlign/horizontal-left.js
@@ -0,0 +1,30 @@
+module.exports = {
+  config: {
+    type: 'pie',
+    data: {
+      labels: ['aaaa', 'bb', 'c'],
+      datasets: [
+        {
+          data: [1, 2, 3]
+        }
+      ]
+    },
+    options: {
+      plugins: {
+        legend: {
+          position: 'top',
+          labels: {
+            textAlign: 'left'
+          }
+        }
+      }
+    }
+  },
+  options: {
+    spriteText: true,
+    canvas: {
+      width: 256,
+      height: 256
+    }
+  }
+};
diff --git a/test/fixtures/plugin.legend/label-textAlign/horizontal-left.png b/test/fixtures/plugin.legend/label-textAlign/horizontal-left.png
new file mode 100644
index 00000000000..84907658eba
Binary files /dev/null and b/test/fixtures/plugin.legend/label-textAlign/horizontal-left.png differ
diff --git a/test/fixtures/plugin.legend/label-textAlign/horizontal-right.js b/test/fixtures/plugin.legend/label-textAlign/horizontal-right.js
new file mode 100644
index 00000000000..729c663ac0a
--- /dev/null
+++ b/test/fixtures/plugin.legend/label-textAlign/horizontal-right.js
@@ -0,0 +1,30 @@
+module.exports = {
+  config: {
+    type: 'pie',
+    data: {
+      labels: ['aaaa', 'bb', 'c'],
+      datasets: [
+        {
+          data: [1, 2, 3]
+        }
+      ]
+    },
+    options: {
+      plugins: {
+        legend: {
+          position: 'top',
+          labels: {
+            textAlign: 'right'
+          }
+        }
+      }
+    }
+  },
+  options: {
+    spriteText: true,
+    canvas: {
+      width: 256,
+      height: 256
+    }
+  }
+};
diff --git a/test/fixtures/plugin.legend/label-textAlign/horizontal-right.png b/test/fixtures/plugin.legend/label-textAlign/horizontal-right.png
new file mode 100644
index 00000000000..84907658eba
Binary files /dev/null and b/test/fixtures/plugin.legend/label-textAlign/horizontal-right.png differ
diff --git a/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-left.js b/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-left.js
new file mode 100644
index 00000000000..5fff9c72a2b
--- /dev/null
+++ b/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-left.js
@@ -0,0 +1,31 @@
+module.exports = {
+  config: {
+    type: 'pie',
+    data: {
+      labels: ['aaaa', 'bb', 'c'],
+      datasets: [
+        {
+          data: [1, 2, 3]
+        }
+      ]
+    },
+    options: {
+      plugins: {
+        legend: {
+          position: 'top',
+          rtl: true,
+          labels: {
+            textAlign: 'left'
+          }
+        }
+      }
+    }
+  },
+  options: {
+    spriteText: true,
+    canvas: {
+      width: 256,
+      height: 256
+    }
+  }
+};
diff --git a/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-left.png b/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-left.png
new file mode 100644
index 00000000000..79642112e73
Binary files /dev/null and b/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-left.png differ
diff --git a/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-right.js b/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-right.js
new file mode 100644
index 00000000000..ae900510368
--- /dev/null
+++ b/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-right.js
@@ -0,0 +1,31 @@
+module.exports = {
+  config: {
+    type: 'pie',
+    data: {
+      labels: ['aaaa', 'bb', 'c'],
+      datasets: [
+        {
+          data: [1, 2, 3]
+        }
+      ]
+    },
+    options: {
+      plugins: {
+        legend: {
+          rtl: true,
+          position: 'top',
+          labels: {
+            textAlign: 'right'
+          }
+        }
+      }
+    }
+  },
+  options: {
+    spriteText: true,
+    canvas: {
+      width: 256,
+      height: 256
+    }
+  }
+};
diff --git a/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-right.png b/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-right.png
new file mode 100644
index 00000000000..79642112e73
Binary files /dev/null and b/test/fixtures/plugin.legend/label-textAlign/horizontal-rtl-right.png differ
diff --git a/test/fixtures/plugin.legend/label-textAlign/rtl-left.png b/test/fixtures/plugin.legend/label-textAlign/rtl-left.png
index 80789d65f03..294d61dd6fb 100644
Binary files a/test/fixtures/plugin.legend/label-textAlign/rtl-left.png and b/test/fixtures/plugin.legend/label-textAlign/rtl-left.png differ
diff --git a/test/fixtures/plugin.legend/label-textAlign/rtl-right.png b/test/fixtures/plugin.legend/label-textAlign/rtl-right.png
index 294d61dd6fb..80789d65f03 100644
Binary files a/test/fixtures/plugin.legend/label-textAlign/rtl-right.png and b/test/fixtures/plugin.legend/label-textAlign/rtl-right.png differ

EOF_7d8df0e3a0cd
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout 599e23abfd1bb3545e350d62647f19911125872b test/fixtures/plugin.legend/label-textAlign/rtl-left.png test/fixtures/plugin.legend/label-textAlign/rtl-right.png
