#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout fe332f6e041fa5949a5062cf818f66fc6cb1f0e1 client/lib/post-normalizer/test/index.js
git apply --verbose --reject - <<'EOF_91080273bc70'
diff --git a/client/lib/post-normalizer/test/index.js b/client/lib/post-normalizer/test/index.js
index 7d9d8c520ebb9..8d1743d4f4a20 100644
--- a/client/lib/post-normalizer/test/index.js
+++ b/client/lib/post-normalizer/test/index.js
@@ -1092,6 +1092,24 @@ describe( 'index', () => {
 				}
 			);
 		} );
+		test( 'links to embedded Polldaddy surveys', done => {
+			normalizer(
+				{
+					content:
+						'<div class="embed-polldaddy">' +
+						'<div class="pd-embed" data-settings="{&quot;type&quot;:&quot;iframe&quot;,&quot;auto&quot;:true,&quot;domain&quot;:&quot;bluefuton.polldaddy.com/s/&quot;,&quot;id&quot;:&quot;what-s-your-favourite-bird&quot;}">' +
+						'</div>',
+				},
+				[ normalizer.withContentDOM( [ normalizer.content.detectSurveys ] ) ],
+				function( err, normalized ) {
+					assert.include(
+						normalized.content,
+						'<p><a target="_blank" rel="external noopener noreferrer" href="https://bluefuton.polldaddy.com/s/what-s-your-favourite-bird">Take our survey</a></p>'
+					);
+					done( err );
+				}
+			);
+		} );
 
 		test( 'removes elements by selector', done => {
 			normalizer(

EOF_91080273bc70
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/lib/post-normalizer/test/index.js'
: '>>>>> End Test Output'
git checkout fe332f6e041fa5949a5062cf818f66fc6cb1f0e1 client/lib/post-normalizer/test/index.js
