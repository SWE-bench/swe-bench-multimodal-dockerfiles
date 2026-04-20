"""
SPECS_* dicts for the SWE-bench Multimodal *dev split* repos.

Each SPECS_X dict maps a repo version → eval/build/test config consumed by
__init__.py via MAP_REPO_VERSION_TO_SPECS_JS. A spec's "test_cmd" entry may
be a string, list of strings, or a callable(instance) -> list[str] for
per-instance test command derivation.
"""

import re

from sb_dockerfile_gen.common import (
    TEST_XVFB_PREFIX,
    XVFB_DEPS,
    X11_DEPS,
    chromium_preinstall,
    CHROMIUM_62, CHROMIUM_72_A, CHROMIUM_76_B, CHROMIUM_76_P5,
    CHROMIUM_85_A, CHROMIUM_88_A, CHROMIUM_90, CHROMIUM_93, CHROMIUM_107_B,
    CHROMIUM_110_A, CHROMIUM_CFT_120,
)
from sb_dockerfile_gen.utils import get_test_paths


# ============================================================
# wp-calypso
# ============================================================
SPECS_CALYPSO = {
    **{
        k: {
            "apt-pkgs": ["libsass-dev", "sassc"],
            "install": ["npm install --unsafe-perm"],
            "test_cmd": "npm run test-client -- --verbose",
            "docker_specs": {
                "node_version": k,
            },
        }
        for k in [
            "0.8",
            "4.2.3",
            "4.3.0",
            "5.10.1",
            "5.11.1",
            "6.1.0",
            "6.7.0",
            "6.9.0",
            "6.9.1",
            "6.9.4",
            "6.10.0",
            "6.10.2",
            "6.10.3",
            "6.11.1",
            "6.11.2",
            "6.11.5",
            "8.9.1",
            "8.9.3",
            "8.9.4",
            "8.11.0",
            "8.11.2",
            "10.4.1",
            "10.5.0",
            "10.6.0",
            "10.9.0",
            "10.10.0",
            "10.12.0",
            "10.13.0",
            "10.16.3",
        ]
    },
    # color-studio@1.0.5 was unpublished from npm; replace with the scoped
    # successor @automattic/color-studio@1.0.6 before npm install.
    # Internal monorepo code does require('color-studio/...'), so we also
    # symlink the scoped package back to the unscoped name.
    # Also run `lerna bootstrap` at image-build time so workspace packages like
    # `i18n-calypso` are linked into node_modules/ before tests run. Eval-time
    # pretest re-runs bootstrap but it becomes a no-op once pre-populated.
    # Patch jest.config with a moduleNameMapper for @automattic/* so jest
    # doesn't lose track of workspace symlinks mid-run (33948).
    **{
        k: {
            "apt-pkgs": ["libsass-dev", "sassc"],
            "install": [
                "sed -i 's/\"color-studio\": \"1.0.5\"/\"@automattic\\/color-studio\": \"1.0.6\"/' package.json",
                "npm install --unsafe-perm --ignore-scripts",
                "npm rebuild node-sass",
                "ln -sf $(pwd)/node_modules/@automattic/color-studio node_modules/color-studio",
                "npm run build-packages",
                "./node_modules/.bin/lerna bootstrap || true",
                # Replace workspace symlinks with real copies so jest 24's resolver
                # (which sometimes loses track of symlinked packages) can find
                # them via standard node_modules traversal.
                "for d in /testbed/node_modules/@automattic/* /testbed/node_modules/i18n-calypso /testbed/node_modules/photon; do"
                "  [ -L \"$d\" ] && target=$(readlink -f \"$d\") && rm \"$d\" && cp -a \"$target\" \"$d\";"
                " done",
            ],
            # --maxWorkers=2 sidesteps a jest module-resolver race seen on
            # v10.15.2 (33948) where many workers intermittently lose track of
            # @automattic/* workspace symlinks in node_modules and fail with
            # "Cannot find module '@automattic/format-currency'" mid-suite.
            # NODE_OPTIONS bumps heap so the 12k-test run doesn't OOM with
            # low worker counts.
            # `npm run test-client` triggers pretest → lerna clean → wipes dist/
            # from workspace packages. Invoke jest directly to skip pretest.
            "test_cmd": (
                "NODE_OPTIONS='--max-old-space-size=8192' "
                "./node_modules/.bin/jest -c=test/client/jest.config.js --verbose"
            ),
            "docker_specs": {
                "node_version": k,
            },
        }
        for k in ["10.14.0", "10.15.2"]
    },
}
# v8.9.3 test suite imports optional deps (`cpf`, `hoek`) at runtime that were
# pruned from package.json. Install them explicitly so Ebanx / hoek tests run.
for _v in ["8.9.3"]:
    # Test imports `cpf.isValid` (available since cpf@1.0.0) and `hoek`.
    # Single install call with --no-prune preserves both despite --no-save.
    SPECS_CALYPSO[_v]["install"].append(
        "npm install cpf@1.0.1 hoek@6.1.3 --no-save --no-prune --legacy-peer-deps || true"
    )


# ============================================================
# Chart.js
# ============================================================
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


# ============================================================
# marked
# ============================================================
# Jasmine's default reporter only emits dots for passing tests. Install a
# tiny custom reporter that logs `JASMINE_TEST: <status> :: <fullName>` per
# spec so the parser can detect passes (not just failures).
MARKED_JASMINE_REPORTER_SETUP = (
    "mkdir -p test/helpers && "
    "printf '%s\\n' "
    "\"jasmine.getEnv().addReporter({ specDone: function(r){ "
    "console.log('JASMINE_TEST: ' + r.status + ' :: ' + r.fullName); } });\" "
    "> test/helpers/jasmine_names.js && "
    "python3 -c \"import json; p='jasmine.json'; d=json.load(open(p)); "
    "h=d.get('helpers', []); "
    "(h.append('helpers/jasmine_names.js') if 'helpers/jasmine_names.js' not in h else None); "
    "d['helpers']=h; json.dump(d, open(p,'w'), indent=2)\""
)
SPECS_MARKED = {
    **{
        k: {
            "install": ["npm install", MARKED_JASMINE_REPORTER_SETUP],
            "test_cmd": "./node_modules/.bin/jasmine --no-color --config=jasmine.json",
            "docker_specs": {
                "node_version": "12.22.12",
            },
        }
        for k in [
            "0.3",
            "0.5",
            "0.6",
            "0.7",
            "1.0",
            "1.1",
            "1.2",
            "2.0",
            "3.9",
            "4.0",
            "4.1",
            "5.0",
        ]
    }
}
for v in ["4.0", "4.1", "5.0"]:
    SPECS_MARKED[v]["docker_specs"]["node_version"] = "20.16.0"


# ============================================================
# p5.js
# ============================================================
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
                """sed -i 's/concurrency:[[:space:]]*[0-9][0-9]*/concurrency: 1/g' Gruntfile.js\n"""
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


# ============================================================
# react-pdf
# ============================================================
SPECS_REACT_PDF = {
    **{
        k: {
            "apt-pkgs": [
                "pkg-config",
                "build-essential",
                "libpixman-1-0",
                "libpixman-1-dev",
                "libcairo2-dev",
                "libpango1.0-dev",
                "libjpeg-dev",
                "libgif-dev",
                "librsvg2-dev",
            ]
            + X11_DEPS,
            "pre_install": ["npm i -g yarn"],
            "install": ["yarn install"],
            "test_cmd": 'NODE_OPTIONS="--experimental-vm-modules" ./node_modules/.bin/jest --no-color',
            "docker_specs": {"node_version": "18.20.4"},
        }
        for k in ["1.0", "1.1", "1.2", "2.0"]
    }
}
for v in ["1.0", "1.1", "1.2"]:
    SPECS_REACT_PDF[v]["docker_specs"]["node_version"] = "8.17.0"
    SPECS_REACT_PDF[v]["pre_install"] = []  # v1.x uses npm, not yarn
    SPECS_REACT_PDF[v]["install"] = ["npm install", "npm install cheerio@1.0.0-rc.3"]
    SPECS_REACT_PDF[v]["test_cmd"] = "./node_modules/.bin/jest --no-color"


# ============================================================
# Per-instance test-command callables
# ============================================================
# Each callable takes the instance dict and returns list[str] of shell
# commands. Assigned to SPECS_X[v]["test_cmd"] AFTER the static value is
# established (so the callable can read the static template via specs_dict).

_CHART_JS_AUTO_LOADED_STEMS = {
    "controller.bar", "controller.bubble", "controller.doughnut",
    "controller.line", "controller.polarArea", "controller.radar",
    "controller.scatter", "core.animation", "core.animations",
    "core.animator", "core.controller", "core.datasetController",
    "core.defaults", "core.element",
}


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


def _p5js_test_cmds(instance: dict) -> list:
    """Conditionally re-run yuidoc before tests.

    Only needed when the gold patch touches docs/preprocessor.js (e.g. 4561
    adds parameterData.json generation). Running yuidoc unconditionally
    regenerates doc data and changes which doc-example tests exist, causing
    spurious P2P drift on other instances.
    """
    test_cmd = _SPECS_P5_JS_STATIC_TEST_CMD[instance["version"]]
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


def _react_pdf_test_cmds(instance: dict) -> list:
    # Run the full test suite (not narrowed to the test_patch's package) so
    # P2P entries in other packages (textkit, image, stylesheet, ...) are
    # actually evaluated. Previously: jest was passed "packages/<name>" which
    # made jest skip the rest of the monorepo.
    return [_SPECS_REACT_PDF_STATIC_TEST_CMD[instance["version"]]]


# Snapshot the static test_cmd values BEFORE we replace them with callables,
# so the callables can read them when invoked.
_SPECS_CHART_JS_STATIC_TEST_CMD = {v: SPECS_CHART_JS[v]["test_cmd"] for v in SPECS_CHART_JS}
_SPECS_P5_JS_STATIC_TEST_CMD = {v: SPECS_P5_JS[v]["test_cmd"] for v in SPECS_P5_JS}
_SPECS_REACT_PDF_STATIC_TEST_CMD = {v: SPECS_REACT_PDF[v]["test_cmd"] for v in SPECS_REACT_PDF}

for v in SPECS_CHART_JS:
    SPECS_CHART_JS[v]["test_cmd"] = _chart_js_test_cmds
for v in SPECS_P5_JS:
    SPECS_P5_JS[v]["test_cmd"] = _p5js_test_cmds
for v in SPECS_REACT_PDF:
    SPECS_REACT_PDF[v]["test_cmd"] = _react_pdf_test_cmds
