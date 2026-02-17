#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 2a551f4bca5cc25baa9d2ac5cf5b2684ef4ee98c client/lib/purchases/test/data/index.js client/lib/purchases/test/index.js
git apply --verbose --reject - <<'EOF_20f507990e71'
diff --git a/client/lib/purchases/test/data/index.js b/client/lib/purchases/test/data/index.js
index dc85439a09695..64f2424a8ad86 100644
--- a/client/lib/purchases/test/data/index.js
+++ b/client/lib/purchases/test/data/index.js
@@ -74,6 +74,28 @@ const PLAN_PURCHASE = {
 	isDomainRegistration: false,
 };
 
+const PLAN_PURCHASE_WITH_CREDITS = {
+	id: 4002,
+	payment: {
+		type: 'credits',
+		countryCode: 'US',
+		countryName: 'United States',
+	},
+	productId: 2006,
+	productName: 'Personal',
+	productSlug: 'jetpack_personal_monthly',
+};
+
+const PLAN_PURCHASE_WITH_PAYPAL = {
+	id: 4003,
+	payment: {
+		type: 'paypal',
+	},
+	productId: 2006,
+	productName: 'Personal',
+	productSlug: 'jetpack_personal_monthly',
+};
+
 export default {
 	DOMAIN_PURCHASE,
 	DOMAIN_PURCHASE_PENDING_TRANSFER,
@@ -84,4 +106,6 @@ export default {
 	PLAN_PURCHASE,
 	SITE_REDIRECT_PURCHASE,
 	SITE_REDIRECT_PURCHASE_EXPIRED,
+	PLAN_PURCHASE_WITH_CREDITS,
+	PLAN_PURCHASE_WITH_PAYPAL,
 };
diff --git a/client/lib/purchases/test/index.js b/client/lib/purchases/test/index.js
index efab55d27a38e..78e3c1048b68e 100644
--- a/client/lib/purchases/test/index.js
+++ b/client/lib/purchases/test/index.js
@@ -4,11 +4,13 @@
  * External dependencies
  */
 import { expect } from 'chai';
+import moment from 'moment';
 
 /**
  * Internal dependencies
  */
-import { isRemovable, isCancelable } from '../index';
+import { isRemovable, isCancelable, isPaidWithCredits, subscribedWithinPastWeek } from '../index';
+
 import {
 	DOMAIN_PURCHASE,
 	DOMAIN_PURCHASE_PENDING_TRANSFER,
@@ -19,6 +21,8 @@ import {
 	PLAN_PURCHASE,
 	SITE_REDIRECT_PURCHASE,
 	SITE_REDIRECT_PURCHASE_EXPIRED,
+	PLAN_PURCHASE_WITH_CREDITS,
+	PLAN_PURCHASE_WITH_PAYPAL,
 } from './data';
 
 describe( 'index', () => {
@@ -68,4 +72,38 @@ describe( 'index', () => {
 			expect( isCancelable( DOMAIN_PURCHASE_PENDING_TRANSFER ) ).to.be.false;
 		} );
 	} );
+	describe( '#isPaidWithCredits', () => {
+		test( 'should be true when paid with credits', () => {
+			expect( isPaidWithCredits( PLAN_PURCHASE_WITH_CREDITS ) ).to.be.true;
+		} );
+		test( 'should false when not paid with credits', () => {
+			expect( isPaidWithCredits( PLAN_PURCHASE_WITH_PAYPAL ) ).to.be.false;
+		} );
+		test( 'should be false when payment not set on purchase', () => {
+			expect( isPaidWithCredits( {} ) ).to.be.false;
+		} );
+	} );
+	describe( '#subscribedWithinPastWeek', () => {
+		test( 'should return false when no subscribed date', () => {
+			expect( subscribedWithinPastWeek( {} ) ).to.be.false;
+		} );
+		test( 'should return false when subscribed more than 1 week ago', () => {
+			expect(
+				subscribedWithinPastWeek( {
+					subscribedDate: moment()
+						.subtract( 8, 'days' )
+						.format(),
+				} )
+			).to.be.false;
+		} );
+		test( 'should return true when subscribed less than 1 week ago', () => {
+			expect(
+				subscribedWithinPastWeek( {
+					subscribedDate: moment()
+						.subtract( 3, 'days' )
+						.format(),
+				} )
+			).to.be.true;
+		} );
+	} );
 } );

EOF_20f507990e71
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/lib/purchases/test/data/index.js'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.json 'client/lib/purchases/test/index.js'
: '>>>>> End Test Output'
git checkout 2a551f4bca5cc25baa9d2ac5cf5b2684ef4ee98c client/lib/purchases/test/data/index.js client/lib/purchases/test/index.js
