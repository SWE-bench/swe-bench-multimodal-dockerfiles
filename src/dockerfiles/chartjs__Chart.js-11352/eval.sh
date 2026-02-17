#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 201ddffa1d0d0bf61a4372ff1386dbcffd606850 test/fixtures/plugin.legend/legend-doughnut-right-center-mulitiline-labels.png
mkdir -p test/fixtures/plugin.legend
curl -o test/fixtures/plugin.legend/legend-doughnut-right-center-mulitiline-labels.png https://raw.githubusercontent.com/chartjs/Chart.js/d922d221ea46d4b240d0b08691d84cb465dbe9e4/test/fixtures/plugin.legend/legend-doughnut-right-center-mulitiline-labels.png
chmod 777 test/fixtures/plugin.legend/legend-doughnut-right-center-mulitiline-labels.png
git apply --verbose --reject - <<'EOF_05903f5f31b3'
diff --git a/test/fixtures/plugin.legend/legend-doughnut-right-center-mulitiline-labels.png b/test/fixtures/plugin.legend/legend-doughnut-right-center-mulitiline-labels.png
index 6be697361c3..1e92045fc06 100644
Binary files a/test/fixtures/plugin.legend/legend-doughnut-right-center-mulitiline-labels.png and b/test/fixtures/plugin.legend/legend-doughnut-right-center-mulitiline-labels.png differ

EOF_05903f5f31b3
: '>>>>> Start Test Output'
pnpm install
pnpm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.cjs --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout 201ddffa1d0d0bf61a4372ff1386dbcffd606850 test/fixtures/plugin.legend/legend-doughnut-right-center-mulitiline-labels.png
