#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 30b6c1b8d322efcd61485fd28f57364640d831c6 client/jetpack-connect/test/main.js
git apply --verbose --reject - <<'EOF_39367a171427'
diff --git a/client/jetpack-connect/test/main.js b/client/jetpack-connect/test/main.js
index 36a23f8c8f3803..d8a8af238ccc00 100644
--- a/client/jetpack-connect/test/main.js
+++ b/client/jetpack-connect/test/main.js
@@ -34,6 +34,23 @@ jest.mock( 'lib/route/path', () => ( {
 } ) );
 
 describe( 'JetpackConnectMain', () => {
+	describe( 'cleanUrl', () => {
+		test( 'should prepare entered urls for network access', () => {
+			const cleanUrl = new JetpackConnectMain( REQUIRED_PROPS ).cleanUrl;
+			const results = [
+				{ input: '', expected: '' },
+				{ input: 'a', expected: 'http://a' },
+				{ input: 'example.com', expected: 'http://example.com' },
+				{ input: '  example.com   ', expected: 'http://example.com' },
+				{ input: 'http://example.com/', expected: 'http://example.com' },
+				{ input: 'eXAmple.com', expected: 'http://example.com' },
+				{ input: 'example.com/wp-admin', expected: 'http://example.com' },
+			];
+
+			results.forEach( ( { input, expected } ) => expect( cleanUrl( input ) ).toBe( expected ) );
+		} );
+	} );
+
 	describe( 'makeSafeRedirectionFunction', () => {
 		const component = new JetpackConnectMain( REQUIRED_PROPS );
 

EOF_39367a171427
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/jetpack-connect/test/main.js'
: '>>>>> End Test Output'
git checkout 30b6c1b8d322efcd61485fd28f57364640d831c6 client/jetpack-connect/test/main.js
