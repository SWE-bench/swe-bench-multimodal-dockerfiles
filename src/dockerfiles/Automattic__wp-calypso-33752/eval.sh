#!/bin/bash
set -uxo pipefail
cd /testbed
git config --global --add safe.directory /testbed
cd /testbed
git checkout a8b6633f060ab38130c363009b8e6aa10fa4055a client/components/happiness-support/test/index.jsx
git apply --verbose --reject - <<'EOF_1b92bcd5c806'
diff --git a/client/components/happiness-support/test/index.jsx b/client/components/happiness-support/test/index.jsx
index 88e53b4f12b81..409eb51748ab6 100644
--- a/client/components/happiness-support/test/index.jsx
+++ b/client/components/happiness-support/test/index.jsx
@@ -39,7 +39,7 @@ describe( 'HappinessSupport', () => {
 		const content = wrapper.find( 'p.happiness-support__description' );
 		expect( content ).to.have.length( 1 );
 		expect( content.props().children ).to.equal(
-			'Translated: {{strong}}Need help?{{/strong}} A Happiness Engineer can answer questions about your site and your account.'
+			'Translated: {{strong}}Need help?{{/strong}} A Happiness Engineer can answer questions about your site and your\xA0account.'
 		);
 	} );
 

EOF_1b92bcd5c806
: '>>>>> Start Test Output'
./node_modules/.bin/jest --verbose -c=test/client/jest.config.js 'client/components/happiness-support/test/index.jsx'
: '>>>>> End Test Output'
git checkout a8b6633f060ab38130c363009b8e6aa10fa4055a client/components/happiness-support/test/index.jsx
