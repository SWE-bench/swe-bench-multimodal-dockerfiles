"""bpmn-js spec."""

from sb_dockerfile_gen.common import (
    INSTALL_PRETTY_KARMA_JSON,
    SET_OPENSSL_TO_LEGACY,
    SET_PUPPETEER_PATH_OPT,
    chromium_preinstall,
    CHROMIUM_73, CHROMIUM_76_A, CHROMIUM_76_B,
    CHROMIUM_85_A, CHROMIUM_88_A, CHROMIUM_90, CHROMIUM_92,
    CHROMIUM_110_A, CHROMIUM_112_A, CHROMIUM_CFT_117_A,
)


# karma-json-reporter@1.2.1 emits JSON to stdout via `--reporters json`. Large
# runs (bpmn-js-1607/-1720/-1802/-1640) produce 160–460KB single-line JSON
# which Docker's log pipe truncates at 64KB boundaries. Capture to a file
# inside the container, then pretty-print so the JSON spans multiple lines
# and each line is well under the chunk size. Parser handles both layouts.
#
# `|| true` after pretty-karma-json so a non-zero karma rc (e.g. partial
# test failures) doesn't trip pipefail and short-circuit the rest of the
# eval_script — we need the End-Test-Output marker to fire so the grader
# knows where the test region ends. Test outcomes are read from the JSON,
# not the exit code, so swallowing it here is safe.
TEST_CMD_BPMN_JS = (
    "./node_modules/.bin/karma start test/config/karma.unit.js --no-colors --reporters json > /testbed/karma-raw.log 2>&1 || true ; "
    "pretty-karma-json /testbed/karma-raw.log"
)
_BPMN_PUPPETEER_ENV = "PUPPETEER_EXECUTABLE_PATH=/opt/chromium/chrome"
SPECS_BPMN_JS = {
    **{k: {
        "install": ["npm install"],
        "test_cmd": [
            SET_PUPPETEER_PATH_OPT.format("test/config/karma.unit.js"),
            "sed -i \"/module.exports = function(karma) {/i \\\\\n"
            "var customLaunchers = { \\\\\n"
            "  ChromeNoSandbox: { \\\\\n"
            "    base: 'ChromeHeadless', \\\\\n"
            "    flags: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'] \\\\\n"
            "  } \\\\\n"
            "}; \\\\\n"
            "browsers = ['ChromeNoSandbox']; \\\\\n"
            "\" test/config/karma.unit.js",
            "sed -i \"/browsers,/a \\\\    customLaunchers,\" test/config/karma.unit.js",
            f'{_BPMN_PUPPETEER_ENV} su chromeuser -c "{TEST_CMD_BPMN_JS}"',
        ],
        "docker_specs": {
            "node_version": "21.6.2",
        }
    } for k in [
        '3.4', '4.0', '5.0', '5.1', '6.0', '6.3', '7.2', '7.3',
        '7.4', '8.3', '8.8', '8.9', '9.0', '9.1', '9.2', '9.3',
        '11.1', '11.3', '13.2', '15.2'
    ]},
}
for v in ['6.0', '6.3', '7.2', '7.3', '7.4', '8.3', '8.8', '8.9', '9.0', '9.1', '9.2', '9.3']:
    SPECS_BPMN_JS[v]["docker_specs"]["node_version"] = "16.20.2"
# Set OpenSSL to legacy provider for certain versions
for v in ['3.4', '4.0', '5.1']:
    SPECS_BPMN_JS[v]["test_cmd"][-1] = f'{SET_OPENSSL_TO_LEGACY} {SPECS_BPMN_JS[v]["test_cmd"][-1]}'
# Per-version Chromium pins. Constants live in common.py. v5.0 intentionally
# absent — stays on Firefox (see Firefox block below; Chrome 76 regresses
# bpmn-js-1203's copy-paste reattach F2P). v9.0 pinned to CHROMIUM_85_A because
# puppeteer 10.0.0's Chrome 92 regresses bpmn-js-1570 (pre-existing F2P name
# format issue unrelated to rev). Non-dataset versions (0.27, 0.9, 2.3–2.5,
# 3.0, 3.3, 14.0) keep the legacy era buckets (not exercised by any dataset).
BPMN_PINS = {
    '3.4':  CHROMIUM_73,
    '4.0':  CHROMIUM_76_A,
    '5.1':  CHROMIUM_76_B,
    '6.0':  CHROMIUM_76_B,
    '6.3':  CHROMIUM_76_B,
    '7.2':  CHROMIUM_76_B,
    '7.3':  CHROMIUM_76_B,
    '7.4':  CHROMIUM_88_A,
    '8.3':  CHROMIUM_90,
    '8.8':  CHROMIUM_92,
    '8.9':  CHROMIUM_92,
    '9.0':  CHROMIUM_85_A,
    '9.1':  CHROMIUM_92,
    '9.2':  CHROMIUM_92,
    '9.3':  CHROMIUM_92,
    '11.1': CHROMIUM_110_A,
    '11.3': CHROMIUM_110_A,
    '13.2': CHROMIUM_112_A,
    '15.2': CHROMIUM_CFT_117_A,
}
for _v, (_kind, _rev) in BPMN_PINS.items():
    SPECS_BPMN_JS[_v]['pre_install'] = chromium_preinstall(_kind, _rev)

# v5.0 Firefox fallback: Chrome 76 (rev 672088) handles 11/12 v5.0 instances but
# consistently fails bpmn-js-1203's "copy/paste and reattach" F2P. Firefox +
# Node 10 (matching upstream .travis.yml at commit 59de7598b1) resolves all 12.
SPECS_BPMN_JS['5.0']['docker_specs']['node_version'] = '10.24.1'
SPECS_BPMN_JS['5.0']['pre_install'] = [
    "add-apt-repository -y ppa:mozillateam/ppa",
    "apt-get update && apt-get install -y -t 'o=LP-PPA-mozillateam' firefox",
]
SPECS_BPMN_JS['5.0']['install'] = [
    "npm install",
    "npm install karma-firefox-launcher@2.1.3 --no-save",
    "npm install karma-json-reporter@1.2.1 --no-save",
]
SPECS_BPMN_JS['5.0']['test_cmd'] = [
    "sed -i \"s/browsers: .*/browsers: ['FirefoxHeadless'],/\" test/config/karma.unit.js",
    "./node_modules/.bin/karma start test/config/karma.unit.js --no-colors --reporters json > /testbed/karma-raw.log 2>&1 || true ; pretty-karma-json /testbed/karma-raw.log",
]
# Install karma-json-reporter — auto-discovered by karma at test time, structured
# JSON emitted via `--reporters json` CLI flag (see TEST_CMD_BPMN_JS).
for v in SPECS_BPMN_JS:
    SPECS_BPMN_JS[v]['install'].append(
        "npm install karma-json-reporter@1.2.1 --no-save --legacy-peer-deps"
    )
    # pretty-karma-json helper — installed once per image. See common.py.
    SPECS_BPMN_JS[v].setdefault('pre_install', [])
    SPECS_BPMN_JS[v]['pre_install'] = list(SPECS_BPMN_JS[v]['pre_install']) + list(INSTALL_PRETTY_KARMA_JSON)
