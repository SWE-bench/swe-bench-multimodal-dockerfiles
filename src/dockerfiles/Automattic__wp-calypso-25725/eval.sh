#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout af9cf1f55288ebefb6cd1d796df3893db41f2292 client/state/data-layer/wpcom/sites/plan-transfer/test/index.js
git apply --verbose --reject - <<'EOF_b919f9fc1df3'
diff --git a/client/state/data-layer/wpcom/sites/plan-transfer/test/index.js b/client/state/data-layer/wpcom/sites/plan-transfer/test/index.js
index 721f23a365e14..f6d08b02557ac 100644
--- a/client/state/data-layer/wpcom/sites/plan-transfer/test/index.js
+++ b/client/state/data-layer/wpcom/sites/plan-transfer/test/index.js
@@ -33,15 +33,17 @@ describe( 'requestPlanOwnershipTransfer()', () => {
 } );
 
 describe( 'handleTransferSuccess()', () => {
-	test( 'should return a success notice action', () => {
-		const action = handleTransferSuccess( { siteId } );
+	test( 'should return a success notice action and a function', () => {
+		const actions = handleTransferSuccess( { siteId } );
 
-		expect( action ).toMatchObject(
+		expect( actions ).toHaveLength( 2 );
+		expect( actions[ 0 ] ).toMatchObject(
 			successNotice( 'Plan purchaser has been changed successfully.', {
 				duration: 8000,
 				id: `sites-plan-transfer-notice-${ siteId }`,
 			} )
 		);
+		expect( actions[ 1 ] ).toBeInstanceOf( Function );
 	} );
 } );
 

EOF_b919f9fc1df3
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/state/data-layer/wpcom/sites/plan-transfer/test/index.js'
: '>>>>> End Test Output'
git checkout af9cf1f55288ebefb6cd1d796df3893db41f2292 client/state/data-layer/wpcom/sites/plan-transfer/test/index.js
