#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout adc68ed44a6cb224a1dcfa0642284e2bf0fe4f77 client/extensions/woocommerce/state/sites/settings/general/test/selectors.js
git apply --verbose --reject - <<'EOF_87ade2acceaf'
diff --git a/client/extensions/woocommerce/state/sites/settings/general/test/selectors.js b/client/extensions/woocommerce/state/sites/settings/general/test/selectors.js
index 3eca19e2a3e44..f381191f9c8ef 100644
--- a/client/extensions/woocommerce/state/sites/settings/general/test/selectors.js
+++ b/client/extensions/woocommerce/state/sites/settings/general/test/selectors.js
@@ -12,6 +12,7 @@ import {
 	areSettingsGeneralLoaded,
 	areSettingsGeneralLoading,
 	getPaymentCurrencySettings,
+	getShipToCountrySetting,
 } from '../selectors';
 import { LOADING } from 'woocommerce/state/constants';
 
@@ -48,13 +49,22 @@ const currencySetting = {
 	default: 'GBP',
 	value: 'USD',
 };
+
+const shipToCountrySetting = {
+	id: 'woocommerce_ship_to_countries',
+	label: 'Shipping location(s)',
+	type: 'select',
+	default: '',
+	value: 'disabled',
+};
+
 const loadedState = {
 	extensions: {
 		woocommerce: {
 			sites: {
 				123: {
 					settings: {
-						general: [ currencySetting ],
+						general: [ currencySetting, shipToCountrySetting ],
 					},
 				},
 			},
@@ -119,4 +129,14 @@ describe( 'selectors', () => {
 			expect( getPaymentCurrencySettings( loadedStateWithUi ) ).to.eql( currencySetting );
 		} );
 	} );
+
+	describe( 'getShipToCountrySetting', () => {
+		test( 'should get the setting from state.', () => {
+			expect( getShipToCountrySetting( loadedState, 123 ) ).to.eql( shipToCountrySetting );
+		} );
+
+		test( 'should get the siteId from the UI tree if not provided.', () => {
+			expect( getShipToCountrySetting( loadedStateWithUi ) ).to.eql( shipToCountrySetting );
+		} );
+	} );
 } );

EOF_87ade2acceaf
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/extensions/woocommerce/state/sites/settings/general/test/selectors.js'
: '>>>>> End Test Output'
git checkout adc68ed44a6cb224a1dcfa0642284e2bf0fe4f77 client/extensions/woocommerce/state/sites/settings/general/test/selectors.js
