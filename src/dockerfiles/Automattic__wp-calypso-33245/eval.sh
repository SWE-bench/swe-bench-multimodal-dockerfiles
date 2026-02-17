#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout 5d0969c7b7f1eb23d74e6b25cf3a8751ab36be05 client/components/happiness-support/test/index.jsx
git apply --verbose --reject - <<'EOF_51fff1710732'
diff --git a/client/components/happiness-support/test/index.jsx b/client/components/happiness-support/test/index.jsx
index eed82dc973393..88e53b4f12b81 100644
--- a/client/components/happiness-support/test/index.jsx
+++ b/client/components/happiness-support/test/index.jsx
@@ -36,7 +36,7 @@ describe( 'HappinessSupport', () => {
 	} );
 
 	test( 'should render translated help content', () => {
-		const content = wrapper.find( 'p.happiness-support__text' );
+		const content = wrapper.find( 'p.happiness-support__description' );
 		expect( content ).to.have.length( 1 );
 		expect( content.props().children ).to.equal(
 			'Translated: {{strong}}Need help?{{/strong}} A Happiness Engineer can answer questions about your site and your account.'

EOF_51fff1710732
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.js 'client/components/happiness-support/test/index.jsx'
: '>>>>> End Test Output'
git checkout 5d0969c7b7f1eb23d74e6b25cf3a8751ab36be05 client/components/happiness-support/test/index.jsx
