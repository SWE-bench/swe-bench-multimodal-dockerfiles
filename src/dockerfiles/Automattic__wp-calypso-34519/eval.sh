#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 9231480516c5a3eed1d400baceca5b7169eba4cb client/me/get-apps/test/__snapshots__/apps-badge.js.snap client/me/get-apps/test/apps-badge.js
git apply --verbose --reject - <<'EOF_a3ab66fccd70'
diff --git a/client/me/get-apps/test/__snapshots__/apps-badge.js.snap b/client/blocks/get-apps/test/__snapshots__/apps-badge.js.snap
similarity index 100%
rename from client/me/get-apps/test/__snapshots__/apps-badge.js.snap
rename to client/blocks/get-apps/test/__snapshots__/apps-badge.js.snap
diff --git a/client/me/get-apps/test/apps-badge.js b/client/blocks/get-apps/test/apps-badge.js
similarity index 100%
rename from client/me/get-apps/test/apps-badge.js
rename to client/blocks/get-apps/test/apps-badge.js

EOF_a3ab66fccd70
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.js 'client/blocks/get-apps/test'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.js 'client/blocks/get-apps/test/apps-badge.js'
: '>>>>> End Test Output'
git checkout 9231480516c5a3eed1d400baceca5b7169eba4cb client/me/get-apps/test/__snapshots__/apps-badge.js.snap client/me/get-apps/test/apps-badge.js
