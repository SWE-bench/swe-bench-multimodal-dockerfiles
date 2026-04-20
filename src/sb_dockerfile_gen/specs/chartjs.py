"""Chart.js spec."""

from sb_dockerfile_gen.common import (
    TEST_XVFB_PREFIX,
    XVFB_DEPS,
    chromium_preinstall,
    CHROMIUM_85_A, CHROMIUM_90, CHROMIUM_110_A, CHROMIUM_CFT_120,
)
from sb_dockerfile_gen.utils import get_test_paths


# Run karma, then cat the json results file so the parser can read the structured
# output. Writing to file instead of stdout avoids an issue where buffering 580+
# tests x expectations caused Chrome to hang mid-run on v4.2 (instance 11116).
# \\$? / \\$rc are escaped so they're passed literally to su's shell (the outer
# eval.sh runs with `set -u` and would choke trying to expand unset vars).
TEST_CHART_JS_TEMPLATE = (
    "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start {} "
    "--single-run --coverage --grep --auto-watch false --browsers chrome; "
    "rc=\\$?; test -f /testbed/karma-results.json && cat /testbed/karma-results.json; exit \\$rc"
)
# chart.js variant: replace whole reporters list with just karma-json-reporter.
# v3.0 uses ['progress', 'kjhtml']; v3.5+/v4.x use ['spec', 'kjhtml', ...].
# Keeping other reporters alongside caused Chrome to hang at "Executed 0 of 0".
SETUP_KARMA_JSON_REPORTER_CHART = (
    "sed -i -E \"s#reporters: \\['(spec|progress)'[^]]*\\],#reporters: ['json'],"
    "\\n        jsonReporter: {{ outputFile: '/testbed/karma-results.json' }},#\" {0}"
)
# Extend karma timeouts so slow/heavy Chrome startup under xvfb + docker doesn't
# trigger "no message in 30000 ms" disconnects while rollup bundles large suites.
SETUP_KARMA_TIMEOUTS_CHART = (
    "sed -i \"s/frameworks: \\['jasmine'\\],/frameworks: ['jasmine'],"
    "\\n    captureTimeout: 180000,"
    "\\n    browserDisconnectTimeout: 120000,"
    "\\n    browserDisconnectTolerance: 3,"
    "\\n    browserNoActivityTimeout: 180000,/\" {0}"
)
# Add --disable-dev-shm-usage to Chrome launcher flags. Without this, Chrome
# runs out of /dev/shm in Docker and silently disconnects mid-test-suite
# (10806, 9678 fail 100% without it, 0% with it).
SETUP_CHROME_SHM_FIX_CHART = (
    "sed -i \"s/--disable-renderer-backgrounding/"
    "--disable-renderer-backgrounding',"
    "\\n          '--disable-dev-shm-usage/\" {0}"
)
SPECS_CHART_JS = {
    **{
        k: {
            "install": [
                "pnpm install",
                "pnpm run build",
            ],
            "test_cmd": [
                "pnpm install",
                "pnpm run build",
                f'{TEST_XVFB_PREFIX} su chromeuser -c "{TEST_CHART_JS_TEMPLATE.format("./karma.conf.cjs")}"',
            ],
            "docker_specs": {
                "node_version": "21.6.2",
                "pnpm_version": "7.9.0",
                "run_args": {
                    "cap_add": ["SYS_ADMIN"],
                },
            },
        }
        for k in ["4.0", "4.1", "4.2", "4.3", "4.4"]
    },
    **{
        k: {
            "install": ["npm install"],
            "test_cmd": [
                "npm install",
                "npm run build",
                f'{TEST_XVFB_PREFIX} su chromeuser -c "{TEST_CHART_JS_TEMPLATE.format("./karma.conf.js")}"',
            ],
            "docker_specs": {
                "node_version": "21.6.2",
                "run_args": {
                    "cap_add": ["SYS_ADMIN"],
                },
            },
        }
        for k in ["3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8"]
    },
    **{
        k: {
            "install": ["npm install", "npm install -g gulp-cli"],
            "test_cmd": [
                "npm install",
                "gulp build",
                TEST_XVFB_PREFIX + ' su chromeuser -c "gulp test"',
            ],
            "docker_specs": {
                "node_version": "21.6.2",
                "run_args": {
                    "cap_add": ["SYS_ADMIN"],
                },
            },
        }
        for k in ["2.0", "2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9"]
    },
}
for v in SPECS_CHART_JS.keys():
    SPECS_CHART_JS[v]["apt-pkgs"] = XVFB_DEPS
# Install karma-json-reporter and patch karma config for structured JSON output.
# Without this, the karma 'spec' reporter only emits FAILED lines, so passed
# F2P tests can't be detected by the parser.
# Use --save-dev (not --no-save) because the eval_script re-runs `npm install`
# at eval time, which would strip any --no-save package.
for v in ["3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8"]:
    SPECS_CHART_JS[v]["install"].extend([
        "npm install karma-json-reporter@1.2.1 --save-dev --legacy-peer-deps",
        SETUP_KARMA_JSON_REPORTER_CHART.format("karma.conf.js"),
        SETUP_KARMA_TIMEOUTS_CHART.format("karma.conf.js"),
        SETUP_CHROME_SHM_FIX_CHART.format("karma.conf.js"),
    ])
for v in ["4.0", "4.1", "4.2", "4.3", "4.4"]:
    SPECS_CHART_JS[v]["install"].extend([
        "pnpm add karma-json-reporter@1.2.1 --save-dev -w",
        SETUP_KARMA_JSON_REPORTER_CHART.format("karma.conf.cjs"),
        SETUP_KARMA_TIMEOUTS_CHART.format("karma.conf.cjs"),
        SETUP_CHROME_SHM_FIX_CHART.format("karma.conf.cjs"),
    ])
# Pin era-appropriate Chrome versions for chart.js. Constants in common.py.
# System Chrome (147+) breaks xhr fixture loading in karma's file server; visual
# tests also fail on Chrome version drift. Chart.js has no puppeteer dep so pins
# are picked era-appropriate rather than derived (empirically tuned: rev 97
# disconnected under xvfb for v3.5-3.8, rev 107 likewise for v4.0-4.1, CfT 113
# disconnects for v4.3/4.4 — so we land on 110/CfT120 for those).
_CHART_JS_CHROME_PINS = {
    # v2.x, v3.0-3.3 -> Chromium 85/90 era
    "2.0": CHROMIUM_85_A, "2.1": CHROMIUM_85_A,
    "2.2": CHROMIUM_85_A, "2.3": CHROMIUM_85_A,
    "2.4": CHROMIUM_85_A, "2.5": CHROMIUM_85_A,
    "2.6": CHROMIUM_85_A, "2.7": CHROMIUM_85_A,
    "2.8": CHROMIUM_85_A, "2.9": CHROMIUM_85_A,
    "3.0": CHROMIUM_90,   "3.1": CHROMIUM_90,
    "3.2": CHROMIUM_90,   "3.3": CHROMIUM_90,
    "3.4": CHROMIUM_90,
    # v3.5-3.8 -> Chromium 110 (was 97; 97 disconnected under xvfb)
    "3.5": CHROMIUM_110_A, "3.6": CHROMIUM_110_A,
    "3.7": CHROMIUM_110_A, "3.8": CHROMIUM_110_A,
    # v4.0-4.1 -> Chromium 110 (was 107; 107 disconnected instantly)
    "4.0": CHROMIUM_110_A, "4.1": CHROMIUM_110_A,
    # v4.2 -> Chrome 110, v4.3-4.4 -> CfT 120 (was CfT 113; 113 disconnects)
    "4.2": CHROMIUM_110_A,
    "4.3": CHROMIUM_CFT_120, "4.4": CHROMIUM_CFT_120,
}
for _v, (_kind, _rev) in _CHART_JS_CHROME_PINS.items():
    SPECS_CHART_JS[_v]["pre_install"] = chromium_preinstall(_kind, _rev)


_CHART_JS_AUTO_LOADED_STEMS = {
    "controller.bar", "controller.bubble", "controller.doughnut",
    "controller.line", "controller.polarArea", "controller.radar",
    "controller.scatter", "core.animation", "core.animations",
    "core.animator", "core.controller", "core.datasetController",
    "core.defaults", "core.element",
}


_SPECS_CHART_JS_STATIC_TEST_CMD = {v: SPECS_CHART_JS[v]["test_cmd"] for v in SPECS_CHART_JS}


def _chart_js_test_cmds(instance: dict) -> list:
    """Conditionally narrow karma via --grep for spec files not auto-loaded.

    Karma's rollup bundle only executes the alphabetically first ~14 spec
    files. If the test_patch only touches files in that set, the default
    (no --grep) run works and is more reliable (fixture auto-tests load).
    Only add --grep runs for spec stems OUTSIDE the auto-loaded set.
    """
    test_cmd_list = _SPECS_CHART_JS_STATIC_TEST_CMD[instance["version"]]
    greps = set()
    for path in get_test_paths(instance):
        if path.startswith("test/specs/") and path.endswith(".tests.js"):
            greps.add(path[len("test/specs/"):-len(".tests.js")])
        elif path.startswith("test/fixtures/"):
            stem = path[len("test/fixtures/"):].split("/", 1)[0]
            if stem:
                greps.add(stem)
    extra_greps = greps - _CHART_JS_AUTO_LOADED_STEMS
    if not extra_greps:
        return test_cmd_list
    karma_cmds = [c for c in test_cmd_list if "karma start" in c]
    result = list(test_cmd_list)
    for grep in sorted(extra_greps):
        for cmd in karma_cmds:
            result.append(cmd.replace("--grep ", f"--grep {grep} "))
    return result


for v in SPECS_CHART_JS:
    SPECS_CHART_JS[v]["test_cmd"] = _chart_js_test_cmds
