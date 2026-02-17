#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout e9d12f1585da7f7bd4ee03f47f43bfd7a2247ab8 client/blocks/app-banner/test/app-banner.jsx
git apply --verbose --reject - <<'EOF_7c0f570147c9'
diff --git a/client/blocks/app-banner/test/app-banner.jsx b/client/blocks/app-banner/test/app-banner.jsx
index 3fe0afb547bb7..e3712bee181cc 100644
--- a/client/blocks/app-banner/test/app-banner.jsx
+++ b/client/blocks/app-banner/test/app-banner.jsx
@@ -7,7 +7,7 @@
  * Internal dependencies
  */
 import { getiOSDeepLink, buildDeepLinkFragment } from 'blocks/app-banner';
-import { EDITOR, NOTES, READER, STATS } from 'blocks/app-banner/utils';
+import { EDITOR, NOTES, READER, STATS, getCurrentSection } from 'blocks/app-banner/utils';
 
 describe( 'iOS deep link fragments', () => {
 	test( 'properly encodes tricky fragments', () => {
@@ -62,3 +62,29 @@ describe( 'iOS deep links', () => {
 		expect( getiOSDeepLink( '/test', STATS ).split( '#' )[ 1 ].length ).toBeTruthy();
 	} );
 } );
+
+describe( 'getCurrentSection', () => {
+	test( 'returns stats if in stats section', () => {
+		expect( getCurrentSection( STATS, false, '/stats/123' ) ).toBe( STATS );
+	} );
+
+	test( 'returns null for activity log page', () => {
+		expect( getCurrentSection( STATS, false, '/stats/activity/123' ) ).toBe( null );
+	} );
+
+	test( 'returns notes if notes is open', () => {
+		expect( getCurrentSection( STATS, true, '/stats/123' ) ).toBe( NOTES );
+	} );
+
+	test( 'returns reader if in reader section', () => {
+		expect( getCurrentSection( READER, false, '/' ) ).toBe( READER );
+	} );
+
+	test( 'returns editor if in editor section', () => {
+		expect( getCurrentSection( EDITOR, false, '/post/123' ) ).toBe( EDITOR );
+	} );
+
+	test( 'returns null if in a disallowed section', () => {
+		expect( getCurrentSection( 'plugins', false, '/plugins/123' ) ).toBe( null );
+	} );
+} );

EOF_7c0f570147c9
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/blocks/app-banner/test/app-banner.jsx'
: '>>>>> End Test Output'
git checkout e9d12f1585da7f7bd4ee03f47f43bfd7a2247ab8 client/blocks/app-banner/test/app-banner.jsx
