#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout f6bd966b656c4c84ea0aebcdd341f601cd8cc292 client/me/pending-payments/test/index.js
git apply --verbose --reject - <<'EOF_69664881259a'
diff --git a/client/me/pending-payments/test/index.js b/client/me/pending-payments/test/index.js
index 54ab098378f16..9fa744a59f2fe 100644
--- a/client/me/pending-payments/test/index.js
+++ b/client/me/pending-payments/test/index.js
@@ -41,7 +41,7 @@ describe( 'PendingPayments', () => {
 
 		const rules = [
 			'Main.pending-payments Localized(MeSidebarNavigation)',
-			'Main.pending-payments PurchasesHeader[section="pending"]',
+			'Main.pending-payments Connect(Localized(PurchasesHeader))[section="pending"]',
 			'Connect(PurchasesSite)[isPlaceholder=true]',
 		];
 
@@ -59,7 +59,7 @@ describe( 'PendingPayments', () => {
 
 		const rules = [
 			'Main.pending-payments Localized(MeSidebarNavigation)',
-			'Main.pending-payments PurchasesHeader[section="pending"]',
+			'Main.pending-payments Connect(Localized(PurchasesHeader))[section="pending"]',
 			'.pending-payments .pending-payments__no-content EmptyContent',
 		];
 
@@ -84,7 +84,7 @@ describe( 'PendingPayments', () => {
 
 		const rules = [
 			'Main.pending-payments Localized(MeSidebarNavigation)',
-			'Main.pending-payments PurchasesHeader[section="pending"]',
+			'Main.pending-payments Connect(Localized(PurchasesHeader))[section="pending"]',
 			'Main.pending-payments Connect(Localized(PendingListItem))',
 		];
 

EOF_69664881259a
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.js 'client/me/pending-payments/test/index.js'
: '>>>>> End Test Output'
git checkout f6bd966b656c4c84ea0aebcdd341f601cd8cc292 client/me/pending-payments/test/index.js
