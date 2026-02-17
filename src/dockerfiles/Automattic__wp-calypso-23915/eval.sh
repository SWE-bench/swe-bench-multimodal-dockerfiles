#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 24d762a0fe3a92500f92323b038a2389cb6ecae5 client/lib/posts/test/utils.js
git apply --verbose --reject - <<'EOF_c12233eb9448'
diff --git a/client/lib/posts/test/utils.js b/client/lib/posts/test/utils.js
index af04eeea8cd37..26139b25c11b1 100644
--- a/client/lib/posts/test/utils.js
+++ b/client/lib/posts/test/utils.js
@@ -22,7 +22,7 @@ describe( 'utils', () => {
 				{ ID: 123, type: 'post' },
 				{ slug: 'en.blog.wordpress.com' }
 			);
-			assert( url === '/post/en.blog.wordpress.com/123' );
+			expect( url ).toEqual( '/post/en.blog.wordpress.com/123' );
 		} );
 
 		test( 'should return correct path type=page is supplied', () => {
@@ -30,7 +30,7 @@ describe( 'utils', () => {
 				{ ID: 123, type: 'page' },
 				{ slug: 'en.blog.wordpress.com' }
 			);
-			assert( url === '/page/en.blog.wordpress.com/123' );
+			expect( url ).toEqual( '/page/en.blog.wordpress.com/123' );
 		} );
 
 		test( 'should return correct path when custom post type is supplied', () => {
@@ -38,7 +38,12 @@ describe( 'utils', () => {
 				{ ID: 123, type: 'jetpack-portfolio' },
 				{ slug: 'en.blog.wordpress.com' }
 			);
-			assert( url === '/edit/jetpack-portfolio/en.blog.wordpress.com/123' );
+			expect( url ).toEqual( '/edit/jetpack-portfolio/en.blog.wordpress.com/123' );
+		} );
+
+		test( 'should default to type=post if no post type is supplied', () => {
+			const url = postUtils.getEditURL( { ID: 123, type: '' }, { slug: 'en.blog.wordpress.com' } );
+			expect( url ).toEqual( '/post/en.blog.wordpress.com/123' );
 		} );
 	} );
 

EOF_c12233eb9448
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/lib/posts/test/utils.js'
: '>>>>> End Test Output'
git checkout 24d762a0fe3a92500f92323b038a2389cb6ecae5 client/lib/posts/test/utils.js
