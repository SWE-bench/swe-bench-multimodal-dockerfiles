#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 73ff0f9af67b31202eadf17fa93be4d406d418ab client/blocks/product-purchase-features-list/test/video-audio-posts.jsx
git apply --verbose --reject - <<'EOF_500b565a8a39'
diff --git a/client/blocks/product-purchase-features-list/test/video-audio-posts.jsx b/client/blocks/product-purchase-features-list/test/video-audio-posts.jsx
index ff6476954a9db..90d95b99253c5 100644
--- a/client/blocks/product-purchase-features-list/test/video-audio-posts.jsx
+++ b/client/blocks/product-purchase-features-list/test/video-audio-posts.jsx
@@ -72,7 +72,7 @@ describe( 'VideoAudioPosts should use proper description', () => {
 	[ PLAN_PREMIUM, PLAN_PREMIUM_2_YEARS ].forEach( plan => {
 		test( `for premium plan ${ plan }`, () => {
 			const comp = shallow( <VideoAudioPosts { ...props } plan={ plan } /> );
-			expect( comp.find( 'PurchaseDetail' ).props().description ).toContain( '10GB of media' );
+			expect( comp.find( 'PurchaseDetail' ).props().description ).toContain( '13GB of media' );
 		} );
 	} );
 

EOF_500b565a8a39
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.js 'client/blocks/product-purchase-features-list/test/video-audio-posts.jsx'
: '>>>>> End Test Output'
git checkout 73ff0f9af67b31202eadf17fa93be4d406d418ab client/blocks/product-purchase-features-list/test/video-audio-posts.jsx
