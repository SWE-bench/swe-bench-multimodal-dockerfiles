#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 8e68481ec4e29599660332f58967f439fb2ef17c test/fixtures/controller.bar/bar-base-value.png test/fixtures/controller.bar/bar-thickness-flex-offset.png test/fixtures/controller.bar/bar-thickness-flex.png test/fixtures/controller.bar/bar-thickness-offset.png test/fixtures/controller.bar/bar-thickness-reverse.png test/fixtures/controller.bar/bar-thickness-stacked.png test/fixtures/controller.bar/baseLine/bottom.png test/fixtures/controller.bar/baseLine/left.png test/fixtures/controller.bar/baseLine/mid-x.png test/fixtures/controller.bar/baseLine/mid-y.png test/fixtures/controller.bar/baseLine/right.png test/fixtures/controller.bar/baseLine/top.png test/fixtures/controller.bar/baseLine/value-x.png test/fixtures/controller.bar/baseLine/value-y.png test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png test/fixtures/controller.bar/borderRadius/border-radius.png test/fixtures/controller.bar/borderSkipped/middle.png test/fixtures/controller.bar/borderWidth/indexable.png test/fixtures/controller.bar/borderWidth/object.png test/fixtures/controller.bar/borderWidth/value.png test/fixtures/controller.bar/horizontal-borders.png test/fixtures/controller.bar/minBarLength/vertical.png
mkdir -p test/fixtures/controller.bar
curl -o test/fixtures/controller.bar/bar-base-value.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/bar-base-value.png
chmod 777 test/fixtures/controller.bar/bar-base-value.png
mkdir -p test/fixtures/controller.bar
curl -o test/fixtures/controller.bar/bar-thickness-flex-offset.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/bar-thickness-flex-offset.png
chmod 777 test/fixtures/controller.bar/bar-thickness-flex-offset.png
mkdir -p test/fixtures/controller.bar
curl -o test/fixtures/controller.bar/bar-thickness-flex.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/bar-thickness-flex.png
chmod 777 test/fixtures/controller.bar/bar-thickness-flex.png
mkdir -p test/fixtures/controller.bar
curl -o test/fixtures/controller.bar/bar-thickness-offset.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/bar-thickness-offset.png
chmod 777 test/fixtures/controller.bar/bar-thickness-offset.png
mkdir -p test/fixtures/controller.bar
curl -o test/fixtures/controller.bar/bar-thickness-reverse.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/bar-thickness-reverse.png
chmod 777 test/fixtures/controller.bar/bar-thickness-reverse.png
mkdir -p test/fixtures/controller.bar
curl -o test/fixtures/controller.bar/bar-thickness-stacked.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/bar-thickness-stacked.png
chmod 777 test/fixtures/controller.bar/bar-thickness-stacked.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/bottom.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/baseLine/bottom.png
chmod 777 test/fixtures/controller.bar/baseLine/bottom.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/left.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/baseLine/left.png
chmod 777 test/fixtures/controller.bar/baseLine/left.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/mid-x.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/baseLine/mid-x.png
chmod 777 test/fixtures/controller.bar/baseLine/mid-x.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/mid-y.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/baseLine/mid-y.png
chmod 777 test/fixtures/controller.bar/baseLine/mid-y.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/right.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/baseLine/right.png
chmod 777 test/fixtures/controller.bar/baseLine/right.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/top.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/baseLine/top.png
chmod 777 test/fixtures/controller.bar/baseLine/top.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/value-x.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/baseLine/value-x.png
chmod 777 test/fixtures/controller.bar/baseLine/value-x.png
mkdir -p test/fixtures/controller.bar/baseLine
curl -o test/fixtures/controller.bar/baseLine/value-y.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/baseLine/value-y.png
chmod 777 test/fixtures/controller.bar/baseLine/value-y.png
mkdir -p test/fixtures/controller.bar/borderRadius
curl -o test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png
chmod 777 test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png
mkdir -p test/fixtures/controller.bar/borderRadius
curl -o test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png
chmod 777 test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png
mkdir -p test/fixtures/controller.bar/borderRadius
curl -o test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png
chmod 777 test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png
mkdir -p test/fixtures/controller.bar/borderRadius
curl -o test/fixtures/controller.bar/borderRadius/border-radius.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/borderRadius/border-radius.png
chmod 777 test/fixtures/controller.bar/borderRadius/border-radius.png
mkdir -p test/fixtures/controller.bar/borderSkipped
curl -o test/fixtures/controller.bar/borderSkipped/middle.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/borderSkipped/middle.png
chmod 777 test/fixtures/controller.bar/borderSkipped/middle.png
mkdir -p test/fixtures/controller.bar/borderWidth
curl -o test/fixtures/controller.bar/borderWidth/indexable.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/borderWidth/indexable.png
chmod 777 test/fixtures/controller.bar/borderWidth/indexable.png
mkdir -p test/fixtures/controller.bar/borderWidth
curl -o test/fixtures/controller.bar/borderWidth/object.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/borderWidth/object.png
chmod 777 test/fixtures/controller.bar/borderWidth/object.png
mkdir -p test/fixtures/controller.bar/borderWidth
curl -o test/fixtures/controller.bar/borderWidth/value.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/borderWidth/value.png
chmod 777 test/fixtures/controller.bar/borderWidth/value.png
mkdir -p test/fixtures/controller.bar
curl -o test/fixtures/controller.bar/horizontal-borders.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/horizontal-borders.png
chmod 777 test/fixtures/controller.bar/horizontal-borders.png
mkdir -p test/fixtures/controller.bar/minBarLength
curl -o test/fixtures/controller.bar/minBarLength/vertical.png https://raw.githubusercontent.com/chartjs/Chart.js/2502cd581070c91d080a4c6d042b3fa7ce90d2f7/test/fixtures/controller.bar/minBarLength/vertical.png
chmod 777 test/fixtures/controller.bar/minBarLength/vertical.png
git apply --verbose --reject - <<'EOF_ee0af219783e'
diff --git a/test/fixtures/controller.bar/bar-base-value.png b/test/fixtures/controller.bar/bar-base-value.png
index 87219e676a9..98c6797511e 100644
Binary files a/test/fixtures/controller.bar/bar-base-value.png and b/test/fixtures/controller.bar/bar-base-value.png differ
diff --git a/test/fixtures/controller.bar/bar-thickness-flex-offset.png b/test/fixtures/controller.bar/bar-thickness-flex-offset.png
index 59171e08cf3..14491751df7 100644
Binary files a/test/fixtures/controller.bar/bar-thickness-flex-offset.png and b/test/fixtures/controller.bar/bar-thickness-flex-offset.png differ
diff --git a/test/fixtures/controller.bar/bar-thickness-flex.png b/test/fixtures/controller.bar/bar-thickness-flex.png
index 791a29d25d3..62fb2307db9 100644
Binary files a/test/fixtures/controller.bar/bar-thickness-flex.png and b/test/fixtures/controller.bar/bar-thickness-flex.png differ
diff --git a/test/fixtures/controller.bar/bar-thickness-offset.png b/test/fixtures/controller.bar/bar-thickness-offset.png
index 8dcecac88a4..6b35e925708 100644
Binary files a/test/fixtures/controller.bar/bar-thickness-offset.png and b/test/fixtures/controller.bar/bar-thickness-offset.png differ
diff --git a/test/fixtures/controller.bar/bar-thickness-reverse.png b/test/fixtures/controller.bar/bar-thickness-reverse.png
index cf6d621cc55..0913be22e00 100644
Binary files a/test/fixtures/controller.bar/bar-thickness-reverse.png and b/test/fixtures/controller.bar/bar-thickness-reverse.png differ
diff --git a/test/fixtures/controller.bar/bar-thickness-stacked.png b/test/fixtures/controller.bar/bar-thickness-stacked.png
index 696829ee39b..7392dd57c6a 100644
Binary files a/test/fixtures/controller.bar/bar-thickness-stacked.png and b/test/fixtures/controller.bar/bar-thickness-stacked.png differ
diff --git a/test/fixtures/controller.bar/baseLine/bottom.png b/test/fixtures/controller.bar/baseLine/bottom.png
index 87e982e1e23..c689dd3c689 100644
Binary files a/test/fixtures/controller.bar/baseLine/bottom.png and b/test/fixtures/controller.bar/baseLine/bottom.png differ
diff --git a/test/fixtures/controller.bar/baseLine/left.png b/test/fixtures/controller.bar/baseLine/left.png
index 19b328c3bee..340f71e7e86 100644
Binary files a/test/fixtures/controller.bar/baseLine/left.png and b/test/fixtures/controller.bar/baseLine/left.png differ
diff --git a/test/fixtures/controller.bar/baseLine/mid-x.png b/test/fixtures/controller.bar/baseLine/mid-x.png
index d6b37767769..e12c967d25a 100644
Binary files a/test/fixtures/controller.bar/baseLine/mid-x.png and b/test/fixtures/controller.bar/baseLine/mid-x.png differ
diff --git a/test/fixtures/controller.bar/baseLine/mid-y.png b/test/fixtures/controller.bar/baseLine/mid-y.png
index 646fd805184..eca057a6366 100644
Binary files a/test/fixtures/controller.bar/baseLine/mid-y.png and b/test/fixtures/controller.bar/baseLine/mid-y.png differ
diff --git a/test/fixtures/controller.bar/baseLine/right.png b/test/fixtures/controller.bar/baseLine/right.png
index 2f98f893a72..9de9a9e58ba 100644
Binary files a/test/fixtures/controller.bar/baseLine/right.png and b/test/fixtures/controller.bar/baseLine/right.png differ
diff --git a/test/fixtures/controller.bar/baseLine/top.png b/test/fixtures/controller.bar/baseLine/top.png
index e04b9b0bd7e..efe34e9186f 100644
Binary files a/test/fixtures/controller.bar/baseLine/top.png and b/test/fixtures/controller.bar/baseLine/top.png differ
diff --git a/test/fixtures/controller.bar/baseLine/value-x.png b/test/fixtures/controller.bar/baseLine/value-x.png
index 23ed06dd6aa..bb8407e9396 100644
Binary files a/test/fixtures/controller.bar/baseLine/value-x.png and b/test/fixtures/controller.bar/baseLine/value-x.png differ
diff --git a/test/fixtures/controller.bar/baseLine/value-y.png b/test/fixtures/controller.bar/baseLine/value-y.png
index 7063fd102a1..f0de922650f 100644
Binary files a/test/fixtures/controller.bar/baseLine/value-y.png and b/test/fixtures/controller.bar/baseLine/value-y.png differ
diff --git a/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png
index 0c96f07f537..7449d7fa4a1 100644
Binary files a/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png and b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png differ
diff --git a/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png
index 2635b2792ab..fa769073c5c 100644
Binary files a/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png and b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png differ
diff --git a/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png
index 13b82c32a89..951b2eb634a 100644
Binary files a/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png and b/test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png differ
diff --git a/test/fixtures/controller.bar/borderRadius/border-radius.png b/test/fixtures/controller.bar/borderRadius/border-radius.png
index ec5e8a63d31..196b00db5f5 100644
Binary files a/test/fixtures/controller.bar/borderRadius/border-radius.png and b/test/fixtures/controller.bar/borderRadius/border-radius.png differ
diff --git a/test/fixtures/controller.bar/borderSkipped/middle.png b/test/fixtures/controller.bar/borderSkipped/middle.png
index 89796e0ca51..41fd2019597 100644
Binary files a/test/fixtures/controller.bar/borderSkipped/middle.png and b/test/fixtures/controller.bar/borderSkipped/middle.png differ
diff --git a/test/fixtures/controller.bar/borderWidth/indexable.png b/test/fixtures/controller.bar/borderWidth/indexable.png
index 88428927ec1..0929ef0e61f 100644
Binary files a/test/fixtures/controller.bar/borderWidth/indexable.png and b/test/fixtures/controller.bar/borderWidth/indexable.png differ
diff --git a/test/fixtures/controller.bar/borderWidth/object.png b/test/fixtures/controller.bar/borderWidth/object.png
index 3b36d96cb2f..ed251dfa77d 100644
Binary files a/test/fixtures/controller.bar/borderWidth/object.png and b/test/fixtures/controller.bar/borderWidth/object.png differ
diff --git a/test/fixtures/controller.bar/borderWidth/value.png b/test/fixtures/controller.bar/borderWidth/value.png
index 58fec25d81b..4f6aca6142f 100644
Binary files a/test/fixtures/controller.bar/borderWidth/value.png and b/test/fixtures/controller.bar/borderWidth/value.png differ
diff --git a/test/fixtures/controller.bar/horizontal-borders.png b/test/fixtures/controller.bar/horizontal-borders.png
index 96f16777ae3..8398645351f 100644
Binary files a/test/fixtures/controller.bar/horizontal-borders.png and b/test/fixtures/controller.bar/horizontal-borders.png differ
diff --git a/test/fixtures/controller.bar/minBarLength/vertical.png b/test/fixtures/controller.bar/minBarLength/vertical.png
index 2074397ea0f..0595425bcfc 100644
Binary files a/test/fixtures/controller.bar/minBarLength/vertical.png and b/test/fixtures/controller.bar/minBarLength/vertical.png differ

EOF_ee0af219783e
: '>>>>> Start Test Output'
npm install
npm run build
xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" su chromeuser -c "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start ./karma.conf.js --single-run --coverage --grep --auto-watch false"
: '>>>>> End Test Output'
git checkout 8e68481ec4e29599660332f58967f439fb2ef17c test/fixtures/controller.bar/bar-base-value.png test/fixtures/controller.bar/bar-thickness-flex-offset.png test/fixtures/controller.bar/bar-thickness-flex.png test/fixtures/controller.bar/bar-thickness-offset.png test/fixtures/controller.bar/bar-thickness-reverse.png test/fixtures/controller.bar/bar-thickness-stacked.png test/fixtures/controller.bar/baseLine/bottom.png test/fixtures/controller.bar/baseLine/left.png test/fixtures/controller.bar/baseLine/mid-x.png test/fixtures/controller.bar/baseLine/mid-y.png test/fixtures/controller.bar/baseLine/right.png test/fixtures/controller.bar/baseLine/top.png test/fixtures/controller.bar/baseLine/value-x.png test/fixtures/controller.bar/baseLine/value-y.png test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-mixed-chart.png test/fixtures/controller.bar/borderRadius/border-radius-stacked-number-with-order.png test/fixtures/controller.bar/borderRadius/border-radius-stacked-number.png test/fixtures/controller.bar/borderRadius/border-radius.png test/fixtures/controller.bar/borderSkipped/middle.png test/fixtures/controller.bar/borderWidth/indexable.png test/fixtures/controller.bar/borderWidth/object.png test/fixtures/controller.bar/borderWidth/value.png test/fixtures/controller.bar/horizontal-borders.png test/fixtures/controller.bar/minBarLength/vertical.png
