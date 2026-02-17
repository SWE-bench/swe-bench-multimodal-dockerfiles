#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 4be8bc55357f68a51c2d0aeabe9b87820625aff8 client/lib/paths/login/test/index.js
git apply --verbose --reject - <<'EOF_9b69ae290a28'
diff --git a/client/lib/paths/login/test/index.js b/client/lib/paths/login/test/index.js
index 393fd9ddc64ef..ca7bc6d480f1c 100644
--- a/client/lib/paths/login/test/index.js
+++ b/client/lib/paths/login/test/index.js
@@ -63,5 +63,11 @@ describe( 'index', () => {
 
 			expect( url ).to.equal( '/log-in?email_address=foo%40bar.com' );
 		} );
+
+		test( 'should return the login url with encoded OAuth2 client ID param', () => {
+			const url = login( { isNative: true, oauth2ClientId: 12345 } );
+
+			expect( url ).to.equal( '/log-in?client_id=12345' );
+		} );
 	} );
 } );

EOF_9b69ae290a28
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/lib/paths/login/test/index.js'
: '>>>>> End Test Output'
git checkout 4be8bc55357f68a51c2d0aeabe9b87820625aff8 client/lib/paths/login/test/index.js
