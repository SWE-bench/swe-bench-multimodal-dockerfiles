#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 58478c529c2ea594a96c89a8c8daa3f7d22c2dda client/state/selectors/test/get-jetpack-onboarding-pending-steps.js
git apply --verbose --reject - <<'EOF_233e7c8534e7'
diff --git a/client/state/selectors/test/get-jetpack-onboarding-pending-steps.js b/client/state/selectors/test/get-jetpack-onboarding-pending-steps.js
index 0f57610de2955..8f51d44f5fca7 100644
--- a/client/state/selectors/test/get-jetpack-onboarding-pending-steps.js
+++ b/client/state/selectors/test/get-jetpack-onboarding-pending-steps.js
@@ -9,6 +9,37 @@ import { getRequestKey } from 'state/data-layer/wpcom-http/utils';
 import { saveJetpackOnboardingSettings } from 'state/jetpack-onboarding/actions';
 
 describe( 'getJetpackOnboardingPendingSteps()', () => {
+	test( 'should return pending status for the contact form step', () => {
+		const siteId = 2916284;
+		const action = saveJetpackOnboardingSettings( siteId, {
+			addContactForm: true,
+		} );
+		const state = {
+			dataRequests: {
+				[ getRequestKey( action ) ]: {
+					status: 'pending',
+				},
+			},
+		};
+
+		const steps = [
+			STEPS.SITE_TITLE,
+			STEPS.SITE_TYPE,
+			STEPS.CONTACT_FORM,
+			STEPS.WOOCOMMERCE,
+			STEPS.STATS,
+		];
+		const expected = {
+			[ STEPS.SITE_TITLE ]: false,
+			[ STEPS.SITE_TYPE ]: false,
+			[ STEPS.CONTACT_FORM ]: true,
+			[ STEPS.WOOCOMMERCE ]: false,
+			[ STEPS.STATS ]: false,
+		};
+		const pending = getJetpackOnboardingPendingSteps( state, siteId, steps );
+		expect( pending ).toEqual( expected );
+	} );
+
 	test( 'should return pending status for the woocommerce step', () => {
 		const siteId = 2916284;
 		const action = saveJetpackOnboardingSettings( siteId, {
@@ -22,10 +53,17 @@ describe( 'getJetpackOnboardingPendingSteps()', () => {
 			},
 		};
 
-		const steps = [ STEPS.SITE_TITLE, STEPS.SITE_TYPE, STEPS.WOOCOMMERCE, STEPS.STATS ];
+		const steps = [
+			STEPS.SITE_TITLE,
+			STEPS.SITE_TYPE,
+			STEPS.CONTACT_FORM,
+			STEPS.WOOCOMMERCE,
+			STEPS.STATS,
+		];
 		const expected = {
 			[ STEPS.SITE_TITLE ]: false,
 			[ STEPS.SITE_TYPE ]: false,
+			[ STEPS.CONTACT_FORM ]: false,
 			[ STEPS.WOOCOMMERCE ]: true,
 			[ STEPS.STATS ]: false,
 		};
@@ -46,10 +84,17 @@ describe( 'getJetpackOnboardingPendingSteps()', () => {
 			},
 		};
 
-		const steps = [ STEPS.SITE_TITLE, STEPS.SITE_TYPE, STEPS.WOOCOMMERCE, STEPS.STATS ];
+		const steps = [
+			STEPS.SITE_TITLE,
+			STEPS.SITE_TYPE,
+			STEPS.CONTACT_FORM,
+			STEPS.WOOCOMMERCE,
+			STEPS.STATS,
+		];
 		const expected = {
 			[ STEPS.SITE_TITLE ]: false,
 			[ STEPS.SITE_TYPE ]: false,
+			[ STEPS.CONTACT_FORM ]: false,
 			[ STEPS.WOOCOMMERCE ]: false,
 			[ STEPS.STATS ]: true,
 		};

EOF_233e7c8534e7
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/state/selectors/test/get-jetpack-onboarding-pending-steps.js'
: '>>>>> End Test Output'
git checkout 58478c529c2ea594a96c89a8c8daa3f7d22c2dda client/state/selectors/test/get-jetpack-onboarding-pending-steps.js
