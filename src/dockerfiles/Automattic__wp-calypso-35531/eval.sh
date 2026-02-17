#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 9e445e13dd96de61e7b7c5c98ad98e12268a4d12 client/blocks/plan-storage/test/plan-storage.jsx
git apply --verbose --reject - <<'EOF_00490b766fb5'
diff --git a/client/blocks/plan-storage/test/plan-storage.jsx b/client/blocks/plan-storage/test/plan-storage.jsx
index 6c5dd301fc10b5..d2f1b6bbdd242a 100644
--- a/client/blocks/plan-storage/test/plan-storage.jsx
+++ b/client/blocks/plan-storage/test/plan-storage.jsx
@@ -29,6 +29,7 @@ import { PlanStorage } from '../index';
 
 describe( 'PlanStorage basic tests', () => {
 	const props = {
+		canViewBar: true,
 		mediaStorage: {
 			max_storage_bytes: 1000,
 		},
@@ -90,6 +91,11 @@ describe( 'PlanStorage basic tests', () => {
 		const storage = shallow( <PlanStorage { ...props } jetpackSite={ true } /> );
 		assert.lengthOf( storage.find( '.plan-storage' ), 0 );
 	} );
+	
+	test( 'should not render for contributors', () => {
+		const storage = shallow( <PlanStorage { ...props } canViewBar={ false } /> );
+		assert.lengthOf( storage.find( '.plan-storage' ), 0 );
+	} );
 
 	test( 'should not render when site plan slug is empty', () => {
 		const storage = shallow( <PlanStorage { ...props } sitePlanSlug={ null } /> );

EOF_00490b766fb5
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.js 'client/blocks/plan-storage/test/plan-storage.jsx'
: '>>>>> End Test Output'
git checkout 9e445e13dd96de61e7b7c5c98ad98e12268a4d12 client/blocks/plan-storage/test/plan-storage.jsx
