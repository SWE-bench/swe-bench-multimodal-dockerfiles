#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 6324c6d30d4ece27eeb00faa3e7cc0aa1f817f83 client/blocks/post-share/test/nudges.jsx client/blocks/upgrade-nudge/test/index.js
git apply --verbose --reject - <<'EOF_fe72202a7478'
diff --git a/client/blocks/post-share/test/nudges.jsx b/client/blocks/post-share/test/nudges.jsx
index 5ce7ac8843d61..1b49df00877a8 100644
--- a/client/blocks/post-share/test/nudges.jsx
+++ b/client/blocks/post-share/test/nudges.jsx
@@ -57,6 +57,7 @@ import {
 
 const props = {
 	translate: x => x,
+	canUserUpgrade: true,
 };
 
 describe( 'UpgradeToPremiumNudgePure basic tests', () => {
@@ -64,6 +65,15 @@ describe( 'UpgradeToPremiumNudgePure basic tests', () => {
 		const comp = shallow( <UpgradeToPremiumNudgePure { ...props } /> );
 		expect( comp.find( 'Banner' ).length ).toBe( 1 );
 	} );
+	
+	test( 'hide when user cannot upgrade', () => {
+		const props = {
+			translate: x => x,
+			canUserUpgrade: false,
+		};
+		const comp = shallow( <UpgradeToPremiumNudgePure { ...props } /> );
+		expect( comp.find( 'Banner' ).length ).toBe( 0 );
+	} );
 } );
 
 describe( 'UpgradeToPremiumNudgePure.render()', () => {
diff --git a/client/blocks/upgrade-nudge/test/index.js b/client/blocks/upgrade-nudge/test/index.js
index a850c6da1187c..4e6b1450b2f80 100644
--- a/client/blocks/upgrade-nudge/test/index.js
+++ b/client/blocks/upgrade-nudge/test/index.js
@@ -1,4 +1,3 @@
-/** @format */
 /**
  * External dependencies
  */
@@ -26,12 +25,12 @@ describe( 'UpgradeNudge', () => {
 		return merge( {}, defaultProps, overrideProps );
 	};
 
-	describe( '#shouldDisplay()', () => {
+	describe( 'wrapper', () => {
 		test( 'should display with default props', () => {
 			const props = createProps();
 			const wrapper = shallow( <UpgradeNudge { ...props } /> );
 
-			expect( wrapper.instance().shouldDisplay() ).toBe( true );
+			expect( wrapper.find( '.upgrade-nudge' ) ).toHaveLength( 1 );
 		} );
 
 		test( 'should not display without a site', () => {
@@ -39,7 +38,7 @@ describe( 'UpgradeNudge', () => {
 			delete props.site;
 			const wrapper = shallow( <UpgradeNudge { ...props } /> );
 
-			expect( wrapper.instance().shouldDisplay() ).toBe( false );
+			expect( wrapper.find( '.upgrade-nudge' ) ).toHaveLength( 0 );
 		} );
 
 		test( 'should not display for paid plans without feature prop (personal)', () => {
@@ -53,7 +52,7 @@ describe( 'UpgradeNudge', () => {
 			delete props.feature;
 			const wrapper = shallow( <UpgradeNudge { ...props } /> );
 
-			expect( wrapper.instance().shouldDisplay() ).toBe( false );
+			expect( wrapper.find( '.upgrade-nudge' ) ).toHaveLength( 0 );
 		} );
 
 		test( 'should not display for paid plans without feature prop (blogger)', () => {
@@ -67,32 +66,16 @@ describe( 'UpgradeNudge', () => {
 			delete props.feature;
 			const wrapper = shallow( <UpgradeNudge { ...props } /> );
 
-			expect( wrapper.instance().shouldDisplay() ).toBe( false );
+			expect( wrapper.find( '.upgrade-nudge' ) ).toHaveLength( 0 );
 		} );
 
 		test( "should not display when user can't manage site", () => {
 			const props = createProps( { canManageSite: false } );
 			const wrapper = shallow( <UpgradeNudge { ...props } /> );
 
-			expect( wrapper.instance().shouldDisplay() ).toBe( false );
+			expect( wrapper.find( '.upgrade-nudge' ) ).toHaveLength( 0 );
 		} );
-
-		describe( 'with shouldDisplay prop', () => {
-			test( 'should display when shouldDisplay returns true', () => {
-				const props = createProps( { shouldDisplay: () => true } );
-				const wrapper = shallow( <UpgradeNudge { ...props } /> );
-
-				expect( wrapper.instance().shouldDisplay() ).toBe( true );
-			} );
-
-			test( 'should not display when shouldDisplay returns false', () => {
-				const props = createProps( { shouldDisplay: () => false } );
-				const wrapper = shallow( <UpgradeNudge { ...props } /> );
-
-				expect( wrapper.instance().shouldDisplay() ).toBe( false );
-			} );
-		} );
-
+		
 		describe( 'with feature prop', () => {
 			test( 'should not display when plan has feature', () => {
 				const props = createProps( {
@@ -101,7 +84,7 @@ describe( 'UpgradeNudge', () => {
 				} );
 				const wrapper = shallow( <UpgradeNudge { ...props } /> );
 
-				expect( wrapper.instance().shouldDisplay() ).toBe( false );
+				expect( wrapper.find( '.upgrade-nudge' ) ).toHaveLength( 0 );
 			} );
 
 			test( "should display when plan doesn't have feature", () => {
@@ -111,7 +94,7 @@ describe( 'UpgradeNudge', () => {
 				} );
 				const wrapper = shallow( <UpgradeNudge { ...props } /> );
 
-				expect( wrapper.instance().shouldDisplay() ).toBe( true );
+				expect( wrapper.find( '.upgrade-nudge' ) ).toHaveLength( 1 );
 			} );
 		} );
 
@@ -125,7 +108,7 @@ describe( 'UpgradeNudge', () => {
 				} );
 				const wrapper = shallow( <UpgradeNudge { ...props } /> );
 
-				expect( wrapper.instance().shouldDisplay() ).toBe( false );
+				expect( wrapper.find( '.upgrade-nudge' ) ).toHaveLength( 0 );
 			} );
 
 			test( 'should not display when non-jetpack feature for jetpack sites', () => {
@@ -137,7 +120,7 @@ describe( 'UpgradeNudge', () => {
 				} );
 				const wrapper = shallow( <UpgradeNudge { ...props } /> );
 
-				expect( wrapper.instance().shouldDisplay() ).toBe( false );
+				expect( wrapper.find( '.upgrade-nudge' ) ).toHaveLength( 0 );
 			} );
 		} );
 	} );

EOF_fe72202a7478
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.js 'client/blocks/post-share/test/nudges.jsx'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.js 'client/blocks/upgrade-nudge/test/index.js'
: '>>>>> End Test Output'
git checkout 6324c6d30d4ece27eeb00faa3e7cc0aa1f817f83 client/blocks/post-share/test/nudges.jsx client/blocks/upgrade-nudge/test/index.js
