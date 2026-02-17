#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 97d16987f9b4897e3e71ab9d3688ad59d4c57e3d client/jetpack-connect/test/utils.js
git apply --verbose --reject - <<'EOF_fef4cbbe899b'
diff --git a/client/jetpack-connect/test/utils.js b/client/jetpack-connect/test/utils.js
index 032f1eeb91e55..acaf551dd7946 100644
--- a/client/jetpack-connect/test/utils.js
+++ b/client/jetpack-connect/test/utils.js
@@ -3,7 +3,7 @@
 /**
  * Internal dependencies
  */
-import { addCalypsoEnvQueryArg } from '../utils';
+import { addCalypsoEnvQueryArg, getRoleFromScope } from '../utils';
 
 jest.mock( 'config', () => input => {
 	const lookupTable = {
@@ -22,3 +22,25 @@ describe( 'addCalypsoEnvQueryArg', () => {
 		);
 	} );
 } );
+
+describe( 'getRoleFromScope', () => {
+	test( 'should return role from scope', () => {
+		const result = getRoleFromScope( 'role:e8ae7346d1a0f800b64e' );
+		expect( result ).toBe( 'role' );
+	} );
+
+	test( 'should return null if no role is found', () => {
+		const result = getRoleFromScope( ':e8ae7346d1a0f800b64e' );
+		expect( result ).toBe( null );
+	} );
+
+	test( 'should return null if no hash is found', () => {
+		const result = getRoleFromScope( 'role' );
+		expect( result ).toBe( null );
+	} );
+
+	test( 'should return null if scope is malformed', () => {
+		const result = getRoleFromScope( 'rolee8ae7346d1a0f800b64e' );
+		expect( result ).toBe( null );
+	} );
+} );

EOF_fef4cbbe899b
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/jetpack-connect/test/utils.js'
: '>>>>> End Test Output'
git checkout 97d16987f9b4897e3e71ab9d3688ad59d4c57e3d client/jetpack-connect/test/utils.js
