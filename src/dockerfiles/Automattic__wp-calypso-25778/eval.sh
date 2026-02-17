#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 54d626a276373d45ffddd2cf4f7099733c8e43de client/state/data-layer/wpcom/comments/test/index.js
git apply --verbose --reject - <<'EOF_cda93aed085d'
diff --git a/client/state/data-layer/wpcom/comments/test/index.js b/client/state/data-layer/wpcom/comments/test/index.js
index 139947cb8d4bf8..de235c9ec31c9b 100644
--- a/client/state/data-layer/wpcom/comments/test/index.js
+++ b/client/state/data-layer/wpcom/comments/test/index.js
@@ -177,6 +177,7 @@ describe( 'wpcom-api', () => {
 						notice: expect.objectContaining( {
 							status: 'is-error',
 							text: 'Could not retrieve comments for requested post',
+							duration: 5000,
 						} ),
 					} )
 				);

EOF_cda93aed085d
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/state/data-layer/wpcom/comments/test/index.js'
: '>>>>> End Test Output'
git checkout 54d626a276373d45ffddd2cf4f7099733c8e43de client/state/data-layer/wpcom/comments/test/index.js
