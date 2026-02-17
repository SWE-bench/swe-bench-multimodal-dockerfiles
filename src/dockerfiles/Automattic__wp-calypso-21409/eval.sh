#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 91b73692253827a03cfbd98411a5d809b46a776b client/extensions/woocommerce/state/sites/locations/test/selectors.js
git apply --verbose --reject - <<'EOF_8ba86d66d1f2'
diff --git a/client/extensions/woocommerce/state/sites/locations/test/selectors.js b/client/extensions/woocommerce/state/sites/locations/test/selectors.js
index 32562f41e8db49..947719ee442ee6 100644
--- a/client/extensions/woocommerce/state/sites/locations/test/selectors.js
+++ b/client/extensions/woocommerce/state/sites/locations/test/selectors.js
@@ -14,6 +14,7 @@ import {
 	getContinents,
 	getCountries,
 	getCountryName,
+	getCountriesWithStates,
 	getStates,
 	hasStates,
 } from '../selectors';
@@ -259,4 +260,18 @@ describe( 'selectors', () => {
 			expect( hasStates( loadedState, 'US' ) ).to.be.true;
 		} );
 	} );
+
+	describe( '#getCountriesWithStates', () => {
+		test( 'should return an empty list if the locations are not loaded', () => {
+			expect( getCountriesWithStates( emptyState ) ).to.deep.equal( [] );
+		} );
+
+		test( 'should return an empty list if the locations are being loaded', () => {
+			expect( getCountriesWithStates( loadingState ) ).to.deep.equal( [] );
+		} );
+
+		test( 'should return the countries with states, sorted', () => {
+			expect( getCountriesWithStates( loadedState ) ).to.deep.equal( [ 'CA', 'US' ] );
+		} );
+	} );
 } );

EOF_8ba86d66d1f2
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/extensions/woocommerce/state/sites/locations/test/selectors.js'
: '>>>>> End Test Output'
git checkout 91b73692253827a03cfbd98411a5d809b46a776b client/extensions/woocommerce/state/sites/locations/test/selectors.js
