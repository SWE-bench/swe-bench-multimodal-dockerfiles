#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 01c60033934bb2c7df5ac14e1153f7739696042e client/state/notices/test/middleware.js
git apply --verbose --reject - <<'EOF_7b1eb47e181c'
diff --git a/client/state/notices/test/middleware.js b/client/state/notices/test/middleware.js
index 180459d92ca2e..4e1fce7efd6e9 100644
--- a/client/state/notices/test/middleware.js
+++ b/client/state/notices/test/middleware.js
@@ -200,27 +200,30 @@ describe( 'middleware', () => {
 			} );
 
 			test( 'should dispatch success notice for trash', () => {
-				const noticeAction = onPostSaveSuccess( {
+				onPostSaveSuccess( {
 					type: POST_SAVE_SUCCESS,
 					post: { status: 'trash' },
-				} );
+					savedPost: { global_ID: 'asdfjkl' },
+				} )( dispatch );
 
-				expect( noticeAction ).toMatchObject( {
+				sinon.assert.calledWithMatch( dispatch, {
 					type: NOTICE_CREATE,
 					notice: {
 						status: 'is-success',
-						text: 'Post successfully moved to trash',
+						noticeId: 'trash_asdfjkl',
+						text: 'Post successfully moved to trash.',
+						button: 'Undo',
 					},
 				} );
 			} );
 
 			test( 'should dispatch success notice for publish', () => {
-				const noticeAction = onPostSaveSuccess( {
+				onPostSaveSuccess( {
 					type: POST_SAVE_SUCCESS,
 					post: { status: 'publish' },
-				} );
+				} )( dispatch );
 
-				expect( noticeAction ).toMatchObject( {
+				sinon.assert.calledWithMatch( dispatch, {
 					type: NOTICE_CREATE,
 					notice: {
 						status: 'is-success',

EOF_7b1eb47e181c
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/state/notices/test/middleware.js'
: '>>>>> End Test Output'
git checkout 01c60033934bb2c7df5ac14e1153f7739696042e client/state/notices/test/middleware.js
