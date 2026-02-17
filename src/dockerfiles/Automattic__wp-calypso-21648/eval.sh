#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 9dc9380527d54dcc2e0679c8f092ec9d55037f29 client/extensions/woocommerce/state/sites/settings/email/test/actions.js client/extensions/woocommerce/state/sites/settings/email/test/reducer.js
git apply --verbose --reject - <<'EOF_0e5ba9dd6e4d'
diff --git a/client/extensions/woocommerce/state/sites/settings/email/test/actions.js b/client/extensions/woocommerce/state/sites/settings/email/test/actions.js
index c26a6f66726a77..1ff0fca1d971cf 100644
--- a/client/extensions/woocommerce/state/sites/settings/email/test/actions.js
+++ b/client/extensions/woocommerce/state/sites/settings/email/test/actions.js
@@ -253,7 +253,7 @@ describe( 'actions', () => {
 				expect( dispatch ).to.have.been.calledWith( {
 					type: WOOCOMMERCE_EMAIL_SETTINGS_SUBMIT_SUCCESS,
 					siteId,
-					settings: data,
+					update: data,
 				} );
 			} );
 		} );
diff --git a/client/extensions/woocommerce/state/sites/settings/email/test/reducer.js b/client/extensions/woocommerce/state/sites/settings/email/test/reducer.js
index 8ef0f5a6a13037..bbe8bedb3b20e9 100644
--- a/client/extensions/woocommerce/state/sites/settings/email/test/reducer.js
+++ b/client/extensions/woocommerce/state/sites/settings/email/test/reducer.js
@@ -92,7 +92,7 @@ describe( 'reducer', () => {
 		expect( newState[ siteId ].settings.email ).to.deep.equal( expectedResult );
 	} );
 
-	test( 'should use default value from woocommerce_email_from_address for settings with no value or default.', () => {
+	test( 'should not use default value for settings with no value or default if option is disabled', () => {
 		const siteId = 123;
 		const settings = [
 			{
@@ -119,9 +119,63 @@ describe( 'reducer', () => {
 			email_new_order: {
 				recipient: {
 					value: '',
+					default: '',
+				},
+			},
+		};
+
+		const action = {
+			type: WOOCOMMERCE_EMAIL_SETTINGS_REQUEST_SUCCESS,
+			siteId,
+			data: settings,
+		};
+
+		const newState = reducer( {}, action );
+		expect( newState[ siteId ] ).to.exist;
+		expect( newState[ siteId ].settings ).to.exist;
+		expect( newState[ siteId ].settings.email ).to.deep.equal( expectedResult );
+	} );
+
+	test( 'should use default value for settings with no value or default if option is enabled', () => {
+		const siteId = 123;
+		const settings = [
+			{
+				id: 'woocommerce_email_from_address',
+				value: 'test@test.com',
+				group_id: 'email',
+				default: 'd@e.f',
+			},
+			{
+				id: 'recipient',
+				value: '',
+				group_id: 'email_new_order',
+				default: '',
+			},
+			{
+				id: 'enabled',
+				value: 'yes',
+				group_id: 'email_new_order',
+				default: 'yes',
+			},
+		];
+
+		const expectedResult = {
+			email: {
+				woocommerce_email_from_address: {
+					value: 'test@test.com',
 					default: 'd@e.f',
 				},
 			},
+			email_new_order: {
+				recipient: {
+					value: 'd@e.f',
+					default: 'd@e.f',
+				},
+				enabled: {
+					value: 'yes',
+					default: 'yes',
+				},
+			},
 		};
 
 		const action = {

EOF_0e5ba9dd6e4d
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/extensions/woocommerce/state/sites/settings/email/test/actions.js'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/extensions/woocommerce/state/sites/settings/email/test/reducer.js'
: '>>>>> End Test Output'
git checkout 9dc9380527d54dcc2e0679c8f092ec9d55037f29 client/extensions/woocommerce/state/sites/settings/email/test/actions.js client/extensions/woocommerce/state/sites/settings/email/test/reducer.js
