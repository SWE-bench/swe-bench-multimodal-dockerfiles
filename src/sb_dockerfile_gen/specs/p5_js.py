"""p5.js spec."""

import re

from sb_dockerfile_gen.common import (
    X11_DEPS,
    chromium_preinstall,
    CHROMIUM_62, CHROMIUM_72_A, CHROMIUM_76_B, CHROMIUM_76_P5,
    CHROMIUM_88_A, CHROMIUM_93, CHROMIUM_107_B,
)
from sb_dockerfile_gen.utils import get_test_paths


# Structured test output. Mocha's spec reporter loses describe() levels that
# have no direct tests (e.g. `describe('random()', ...)` containing only
# nested describes), so parse_log_p5js drifts when P2P keys reference those
# levels. Emit per-test JSON events with an explicit suite-stack array so the
# parser can reconstruct `suite1:suite2:...:test` keys exactly.
_P5_REPORTER_SETUP = (
    "cat > /testbed/p5-suite-reporter.js << 'P5REPEOF'\n"
    "module.exports = function (runner) {\n"
    "  const stack = [];\n"
    "  runner.on('suite', s => { if (s.title) stack.push(s.title); });\n"
    "  runner.on('suite end', s => { if (s.title) stack.pop(); });\n"
    "  runner.on('pass', t => { console.log('P5JSON ' + JSON.stringify({t:'pass', s: stack.slice(), n: t.title})); });\n"
    "  runner.on('fail', (t, err) => { console.log('P5JSON ' + JSON.stringify({t:'fail', s: stack.slice(), n: t.title, err: err && err.message})); });\n"
    "};\n"
    "P5REPEOF\n"
    # Route node-side mochaTest at the custom reporter (two Gruntfile patterns)
    "sed -i \"s|const reporter = quietReport ? 'spec' : 'Nyan';|const reporter = '/testbed/p5-suite-reporter.js';|\" Gruntfile.js\n"
    "sed -i \"s|reporter: 'spec',|reporter: '/testbed/p5-suite-reporter.js',|g\" Gruntfile.js\n"
    # Inline reporter for browser-side mochaChrome (runs in puppeteer page context)
    "sed -i \"s|mocha.reporter('spec');|mocha.reporter(function(r){var st=[];r.on('suite',function(s){if(s.title)st.push(s.title);});r.on('suite end',function(s){if(s.title)st.pop();});r.on('pass',function(t){console.log('P5JSON '+JSON.stringify({t:'pass',s:st.slice(),n:t.title}));});r.on('fail',function(t,e){console.log('P5JSON '+JSON.stringify({t:'fail',s:st.slice(),n:t.title,err:e\\&\\&e.message}));});});|\" tasks/test/mocha-chrome.js\n"
    # Replace page.on('console') handler with msg.text() — the default
    # jsonValue() round-trip per arg overwhelms puppeteer's async pipeline on
    # older versions (v0.7 / mocha 5.x / puppeteer 1.12) once we emit thousands
    # of P5JSON console.log calls per suite, hanging the yui→test transition.
    # text() is sync and preserves the already-formatted P5JSON payload.
    "sed -i \"s|const args = await mapSeries(msg.args(), v => v.jsonValue());|const args = [msg.text()];|\" tasks/test/mocha-chrome.js\n"
)


SPECS_P5_JS = {
    **{
        k: {
            "apt-pkgs": X11_DEPS,
            "install": [
                "npm install",
                "./node_modules/.bin/grunt yui",
            ],
            # Pre-baked Chromium at /opt/chromium/chrome (see _P5_CHROMIUM_PINS).
            # PUPPETEER_EXECUTABLE_PATH routes puppeteer at it; CHROME_BIN routes
            # karma-chrome-launcher at it (v0.4–v0.6 path).
            "test_cmd": (
                _P5_REPORTER_SETUP
                + "sed -i 's/concurrency:[[:space:]]*[0-9][0-9]*/concurrency: 1/g' Gruntfile.js\n"
                "PUPPETEER_EXECUTABLE_PATH=/opt/chromium/chrome "
                "CHROME_BIN=/opt/chromium/chrome "
                "stdbuf -o 1M ./node_modules/.bin/grunt test --quiet --force"
            ),
            "docker_specs": {
                "node_version": "14.17.3",
            },
        }
        for k in [
            "0.10",
            "0.2",
            "0.4",
            "0.5",
            "0.6",
            "0.7",
            "0.8",
            "0.9",
            "1.0",
            "1.1",
            "1.2",
            "1.3",
            "1.4",
            "1.5",
            "1.6",
            "1.7",
            "1.8",
            "1.9",
        ]
    },
}
# Per-puppeteer-version Chromium pins. Constants in common.py. v0.6 has no
# puppeteer dep; uses a karma-chrome-launcher era snapshot.
P5_JS_PINS = {
    "0.6":  CHROMIUM_62,
    "0.7":  CHROMIUM_72_A,
    "0.8":  CHROMIUM_72_A,
    "0.10": CHROMIUM_76_B,
    "1.0":  CHROMIUM_76_P5,
    "1.3":  CHROMIUM_88_A,
    "1.4":  CHROMIUM_93,
    "1.5":  CHROMIUM_107_B,
    "1.6":  CHROMIUM_107_B,
}
for _v, (_kind, _rev) in P5_JS_PINS.items():
    SPECS_P5_JS[_v]["pre_install"] = chromium_preinstall(_kind, _rev)


_SPECS_P5_JS_STATIC_TEST_CMD = {v: SPECS_P5_JS[v]["test_cmd"] for v in SPECS_P5_JS}

# Versions whose bundled mocha+puppeteer can't handle our custom json
# reporter cleanly. On v0.6/v0.7 (mocha 5.2 + puppeteer 1.12), the
# hundreds of console.log('P5JSON ...') calls emitted by our in-page
# reporter overwhelm puppeteer's console-message pipeline during the
# mochaChrome:yui→mochaChrome:test transition and the runner never
# completes. Strip the reporter-setup prelude for those versions and
# let parse_log_p5js fall back to spec-scraping (the describe nesting
# on those older p5.js releases is shallow enough for spec-scraping to
# work).
_REPORTER_INCOMPATIBLE_VERSIONS = {"0.6", "0.7"}


def _p5js_test_cmds(instance: dict) -> list:
    """Conditionally re-run yuidoc before tests.

    Only needed when the gold patch touches docs/preprocessor.js (e.g. 4561
    adds parameterData.json generation). Running yuidoc unconditionally
    regenerates doc data and changes which doc-example tests exist, causing
    spurious P2P drift on other instances.
    """
    version = instance["version"]
    test_cmd = _SPECS_P5_JS_STATIC_TEST_CMD[version]
    if version in _REPORTER_INCOMPATIBLE_VERSIONS and isinstance(test_cmd, str):
        test_cmd = test_cmd.replace(_P5_REPORTER_SETUP, "")
    cmds = list(test_cmd) if isinstance(test_cmd, list) else [test_cmd]
    all_paths = get_test_paths(instance) + re.findall(
        r"diff --git a/.* b/(.*)", instance.get("patch", "")
    )
    if any("docs/preprocessor" in p for p in all_paths):
        # Need PUPPETEER_EXECUTABLE_PATH for the mochaChrome:yui subtask
        cmds.insert(0,
            "PUPPETEER_EXECUTABLE_PATH=/opt/chromium/chrome "
            "./node_modules/.bin/grunt yui --force || true"
        )
    return cmds


for v in SPECS_P5_JS:
    SPECS_P5_JS[v]["test_cmd"] = _p5js_test_cmds
