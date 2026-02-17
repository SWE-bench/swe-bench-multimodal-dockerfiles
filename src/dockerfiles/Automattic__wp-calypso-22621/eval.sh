#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 7e634d48378bf52ad659e902d3a4b82e579cc6cd client/state/selectors/test/get-jetpack-onboarding-pending-steps.js client/state/selectors/test/is-jetpack-onboarding-step-completed.js
git apply --verbose --reject - <<'EOF_9eab1df680d3'
diff --git a/client/state/selectors/test/get-jetpack-onboarding-pending-steps.js b/client/state/selectors/test/get-jetpack-onboarding-pending-steps.js
index 8a7df38d99ba0..0f57610de2955 100644
--- a/client/state/selectors/test/get-jetpack-onboarding-pending-steps.js
+++ b/client/state/selectors/test/get-jetpack-onboarding-pending-steps.js
@@ -9,9 +9,11 @@ import { getRequestKey } from 'state/data-layer/wpcom-http/utils';
 import { saveJetpackOnboardingSettings } from 'state/jetpack-onboarding/actions';
 
 describe( 'getJetpackOnboardingPendingSteps()', () => {
-	test( 'should return pending status for the specified steps', () => {
+	test( 'should return pending status for the woocommerce step', () => {
 		const siteId = 2916284;
-		const action = saveJetpackOnboardingSettings( siteId, { installWooCommerce: true } );
+		const action = saveJetpackOnboardingSettings( siteId, {
+			installWooCommerce: true,
+		} );
 		const state = {
 			dataRequests: {
 				[ getRequestKey( action ) ]: {
@@ -20,11 +22,36 @@ describe( 'getJetpackOnboardingPendingSteps()', () => {
 			},
 		};
 
-		const steps = [ STEPS.SITE_TITLE, STEPS.SITE_TYPE, STEPS.WOOCOMMERCE ];
+		const steps = [ STEPS.SITE_TITLE, STEPS.SITE_TYPE, STEPS.WOOCOMMERCE, STEPS.STATS ];
 		const expected = {
 			[ STEPS.SITE_TITLE ]: false,
 			[ STEPS.SITE_TYPE ]: false,
 			[ STEPS.WOOCOMMERCE ]: true,
+			[ STEPS.STATS ]: false,
+		};
+		const pending = getJetpackOnboardingPendingSteps( state, siteId, steps );
+		expect( pending ).toEqual( expected );
+	} );
+
+	test( 'should return pending status for the stats step', () => {
+		const siteId = 2916284;
+		const action = saveJetpackOnboardingSettings( siteId, {
+			stats: true,
+		} );
+		const state = {
+			dataRequests: {
+				[ getRequestKey( action ) ]: {
+					status: 'pending',
+				},
+			},
+		};
+
+		const steps = [ STEPS.SITE_TITLE, STEPS.SITE_TYPE, STEPS.WOOCOMMERCE, STEPS.STATS ];
+		const expected = {
+			[ STEPS.SITE_TITLE ]: false,
+			[ STEPS.SITE_TYPE ]: false,
+			[ STEPS.WOOCOMMERCE ]: false,
+			[ STEPS.STATS ]: true,
 		};
 		const pending = getJetpackOnboardingPendingSteps( state, siteId, steps );
 		expect( pending ).toEqual( expected );
diff --git a/client/state/selectors/test/is-jetpack-onboarding-step-completed.js b/client/state/selectors/test/is-jetpack-onboarding-step-completed.js
index f0b082494d587..d54001641200f 100644
--- a/client/state/selectors/test/is-jetpack-onboarding-step-completed.js
+++ b/client/state/selectors/test/is-jetpack-onboarding-step-completed.js
@@ -325,4 +325,49 @@ describe( 'isJetpackOnboardingStepCompleted()', () => {
 
 		expect( completed ).toBe( false );
 	} );
+
+	test( 'should return true for stats step if we have chosen to activate stats', () => {
+		const state = {
+			jetpackOnboarding: {
+				settings: {
+					2916284: {
+						stats: true,
+					},
+				},
+			},
+		};
+		const completed = isJetpackOnboardingStepCompleted( state, 2916284, STEPS.STATS );
+
+		expect( completed ).toBe( true );
+	} );
+
+	test( 'should return false for stats step if we have not activated stats', () => {
+		const state = {
+			jetpackOnboarding: {
+				settings: {
+					2916284: {
+						siteTitle: 'My awesome site',
+					},
+				},
+			},
+		};
+		const completed = isJetpackOnboardingStepCompleted( state, 2916284, STEPS.STATS );
+
+		expect( completed ).toBe( false );
+	} );
+
+	test( 'should return false for stats step if it is specified as not activated', () => {
+		const state = {
+			jetpackOnboarding: {
+				settings: {
+					2916284: {
+						stats: false,
+					},
+				},
+			},
+		};
+		const completed = isJetpackOnboardingStepCompleted( state, 2916284, STEPS.STATS );
+
+		expect( completed ).toBe( false );
+	} );
 } );

EOF_9eab1df680d3
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/state/selectors/test/get-jetpack-onboarding-pending-steps.js'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/state/selectors/test/is-jetpack-onboarding-step-completed.js'
: '>>>>> End Test Output'
git checkout 7e634d48378bf52ad659e902d3a4b82e579cc6cd client/state/selectors/test/get-jetpack-onboarding-pending-steps.js client/state/selectors/test/is-jetpack-onboarding-step-completed.js
