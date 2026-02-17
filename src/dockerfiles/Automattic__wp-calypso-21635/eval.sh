#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 0bab036290b284735a7b5043cc11d194bd8ec37d client/lib/credit-card-details/test/ebanx.js
git apply --verbose --reject - <<'EOF_ab1602a41eba'
diff --git a/client/lib/credit-card-details/test/ebanx.js b/client/lib/credit-card-details/test/ebanx.js
index f9d63d0c4a37b8..12a87218d63965 100644
--- a/client/lib/credit-card-details/test/ebanx.js
+++ b/client/lib/credit-card-details/test/ebanx.js
@@ -40,11 +40,12 @@ describe( 'Ebanx payment processing methods', () => {
 
 	describe( 'isValidCPF', () => {
 		test( 'should return true for valid CPF (Brazilian tax identification number)', () => {
+			expect( isValidCPF( '85384484632' ) ).toEqual( true );
 			expect( isValidCPF( '853.513.468-93' ) ).toEqual( true );
 		} );
 		test( 'should return false for invalid CPF', () => {
-			expect( isValidCPF( '85384484632' ) ).toEqual( false );
-			expect( isValidCPF( '853.844.846.32' ) ).toEqual( false );
+			expect( isValidCPF( '85384484612' ) ).toEqual( false );
+			expect( isValidCPF( '853.844.846.12' ) ).toEqual( false );
 		} );
 	} );
 } );

EOF_ab1602a41eba
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/lib/credit-card-details/test/ebanx.js'
: '>>>>> End Test Output'
git checkout 0bab036290b284735a7b5043cc11d194bd8ec37d client/lib/credit-card-details/test/ebanx.js
