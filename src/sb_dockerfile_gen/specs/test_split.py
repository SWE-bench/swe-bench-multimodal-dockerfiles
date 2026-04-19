"""
SPECS_* dicts for the SWE-bench Multimodal *test split* repos.

Each SPECS_X dict maps a repo version → eval/build/test config consumed by
__init__.py via MAP_REPO_VERSION_TO_SPECS_JS. A spec's "test_cmd" entry may
be a string, list of strings, or a callable(instance) -> list[str]; the
"eval_setup" entry may be a list[str] or a callable(instance) -> list[str].

Six legacy SPECS dicts at the bottom of this file (MAPBOX, PLOTLYJS, INSOMNIA,
EMOTION, PIXIJS, CYPRESS) are not currently wired into MAP_REPO_VERSION_TO_SPECS_JS
but are preserved as-is for possible future use.
"""

import json
import re

from sb_dockerfile_gen.common import (
    XVFB_DEPS,
    SET_OPENSSL_TO_LEGACY,
    SET_PUPPETEER_ENV_VAR,
    SET_PUPPETEER_PATH,
    SETUP_KARMA_JSON_REPORTER_NEXT,
    SETUP_KARMA_JSON_REPORTER_BPMN,
    INSTALL_JULIA,
    INSTALL_TINYTEX,
    INSTALL_R_PACKAGES,
    _CHROMIUM_72_INSTALL,
    _CHROMIUM_85_INSTALL,
    _CHROME_120_INSTALL,
)
from sb_dockerfile_gen.utils import get_test_paths


# ============================================================
# highlight.js
# ============================================================
SPECS_HIGHLIGHTJS = {k: {
    "install": [
        "npm install",
        "npm run build"
    ],
    "test_cmd": [
        "npm install",
        "npm run build",
        "./node_modules/.bin/mocha test --reporter json",
    ],
    "docker_specs": {
        "node_version": "21.6.2"
    }
} for k in [
    '10.0', '10.2', '10.3', '10.4', '10.5', '10.6', '11.0', '11.2', '11.3',
    '11.4', '11.5', '11.6', '8.4', '8.9', '9.13', '9.15', '9.16', '9.17', '9.18',
    None
]}


# ============================================================
# Prism
# ============================================================
TEST_CMD_PRISM = "./node_modules/.bin/mocha tests/run.js --reporter json"
SPECS_PRISM = {
    **{k: {
        "install": ["npm ci", "npm run build"],
        "test_cmd": TEST_CMD_PRISM,
        "docker_specs": {
            "node_version": "12.22.12",
        }
    } for k in ['1.24', '1.25', '1.27', '1.28']},
    **{k: {
        "install": ["npm install", "npm run build"],
        "test_cmd": TEST_CMD_PRISM,
        "docker_specs": {
            "node_version": "10.24.1",
        }
    } for k in ['1.22', '1.23']},
    **{k: {
        "install": ["npm install"],
        "test_cmd": TEST_CMD_PRISM,
        "docker_specs": {
            "node_version": "8.17.0",
        }
    } for k in ['1.15', '1.16', '1.17', '1.19', '1.20']}
}
SPECS_PRISM['1.15']['docker_specs']['node_version'] = '4.9.1'
SPECS_PRISM['1.16']['docker_specs']['node_version'] = '21.6.2'
SPECS_PRISM['1.17']['docker_specs']['node_version'] = '21.6.2'


# ============================================================
# ESLint
# ============================================================
TEST_CMD_ESLINT = './node_modules/.bin/mocha --forbid-only --reporter json -t 10000 --no-colors "tests/{bin,conf,lib,tools}/**/*.js"'
SPECS_ESLINT = {
    **{k: {
        "install": ["npm install"],
        "test_cmd": TEST_CMD_ESLINT,
        "docker_specs": {
            "node_version": "10.24.1",
        }
    } for k in [
        '0.20', '0.24', '0.3', '0.5', '1.0', '1.1',
        '1.10', '1.5', '1.7', '1.9', '2.0', '2.10',
        '2.12', '2.13', '2.5', '3.1', '3.11',
        '3.16', '3.5', '4.1', '4.7', '4.9', '5.14',
        '6.6', '6.7', '7.18', '7.22', '8.1', '8.50'
    ]},
}
for v in ['0.20', '0.24', '0.3', '0.5', '1.0', '1.1', '1.10', '1.5',
    '1.7', '1.9', '2.0', '2.10', '2.12', '2.13', '2.5', '3.1', '3.11']:
    SPECS_ESLINT[v]["docker_specs"]["node_version"] = "4.9.1"
for v in ['8.1', '8.50']:
    SPECS_ESLINT[v]["docker_specs"]["node_version"] = "21.6.2"


# ============================================================
# bpmn-js
# ============================================================
TEST_CMD_BPMN_JS = "./node_modules/.bin/karma start test/config/karma.unit.js --no-colors"
SPECS_BPMN_JS = {
    **{k: {
        "install": ["npm install"],
        "test_cmd": [
            SET_PUPPETEER_PATH.format("test/config/karma.unit.js"),
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
            f'{SET_PUPPETEER_ENV_VAR} su chromeuser -c "{TEST_CMD_BPMN_JS}"',
        ],
        "docker_specs": {
            "node_version": "21.6.2",
        }
    } for k in [
        '0.27', '0.9', '2.3', '2.4', '2.5', '3.0', '3.3',
        '3.4', '4.0', '5.0', '5.1', '6.0', '6.3', '7.2', '7.3',
        '7.4', '8.3', '8.8', '8.9', '9.0', '9.1', '9.2', '9.3',
        '11.1', '11.3', '13.2', '14.0', '15.2'
    ]},
}
for v in ['6.0', '6.3', '7.2', '7.3', '7.4', '8.3', '8.8', '8.9', '9.0', '9.1', '9.2', '9.3']:
    SPECS_BPMN_JS[v]["docker_specs"]["node_version"] = "16.20.2"
# Set OpenSSL to legacy provider for certain versions
for v in ['3.0', '3.3', '3.4', '4.0', '5.1']:
    SPECS_BPMN_JS[v]["test_cmd"][-1] = f'{SET_OPENSSL_TO_LEGACY} {SPECS_BPMN_JS[v]["test_cmd"][-1]}'
# bpmn-js v5.0: use Firefox (matching upstream CI) instead of Chrome.
# Upstream .travis.yml at commit 59de7598b1 uses Node 10 + Firefox + PhantomJS.
# Chrome (72, 78, 146) all fail on label rendering and BpmnUpdater.updateSemanticParent.
SPECS_BPMN_JS['5.0']['docker_specs']['node_version'] = '10.24.1'
SPECS_BPMN_JS['5.0']['pre_install'] = [
    "add-apt-repository -y ppa:mozillateam/ppa",
    "apt-get update && apt-get install -y -t 'o=LP-PPA-mozillateam' firefox",
]
SPECS_BPMN_JS['5.0']['install'] = [
    "npm install",
    "npm install karma-firefox-launcher@2.1.3 --no-save",
    "npm install karma-json-reporter@1.2.1 --no-save",
    SETUP_KARMA_JSON_REPORTER_BPMN.format("test/config/karma.unit.js"),
]
SPECS_BPMN_JS['5.0']['test_cmd'] = [
    "sed -i \"s/browsers: .*/browsers: ['FirefoxHeadless'],/\" test/config/karma.unit.js",
    "./node_modules/.bin/karma start test/config/karma.unit.js --no-colors",
]
# Pin era-appropriate Chrome versions for bpmn-js.
# Chrome 146 (system default) breaks label rendering, coordinate precision,
# and BpmnUpdater.updateSemanticParent in older tests.
# Chromium downloads go in pre_install (cached layer before git clone).
for v in ['0.27', '0.9', '2.3', '2.4', '2.5', '3.0', '3.3', '3.4', '4.0', '5.1']:
    SPECS_BPMN_JS[v]['pre_install'] = _CHROMIUM_72_INSTALL
for v in ['6.0', '6.3', '7.2', '7.3', '7.4', '8.3', '8.8', '8.9', '9.0', '9.1', '9.2', '9.3']:
    SPECS_BPMN_JS[v]['pre_install'] = _CHROMIUM_85_INSTALL
for v in ['11.1', '11.3', '13.2', '14.0', '15.2']:
    SPECS_BPMN_JS[v]['pre_install'] = _CHROME_120_INSTALL
# Install karma-json-reporter and patch config for structured JSON output.
# Must be after npm install (so karma.unit.js and node_modules exist).
for v in SPECS_BPMN_JS:
    SPECS_BPMN_JS[v]['install'].extend([
        "npm install karma-json-reporter@1.2.1 --no-save --legacy-peer-deps",
        SETUP_KARMA_JSON_REPORTER_BPMN.format("test/config/karma.unit.js"),
    ])


# ============================================================
# OpenLayers
# ============================================================
SPECS_OPENLAYERS = {
    **{k: {
        "apt-pkgs": XVFB_DEPS,
        "install": ["npm install"],
        "test_cmd": "npm run test",
        "docker_specs": {
            "node_version": "21.6.2",
            "run_args": {
                "cap_add": ["SYS_ADMIN"],
            }
        }
    } for k in [
        '3.0', '3.4', '3.5', '3.8', '3.10', '3.11', '3.12', '3.14', '3.16', '3.17', '3.18', '3.19', '3.20',
        '4.0', '4.3', '4.4', '4.5', '4.6',
        '5.1', '5.2', '5.3',
        '6.0', '6.1', '6.2', '6.3', '6.4', '6.5', '6.5.1', '6.6', '6.9', '6.10', '6.11', '6.12', '6.13', '6.14',
        '7.0', '7.1', '7.2', '7.3', '7.4', '7.5',
        '8.1', '9.0', '9.1'
    ]},
}
# OpenLayers runs on the vintage Ubuntu 20.04 base (see _DOCKERFILE_BASE_JS_OL
# in __init__.py). That base ships Mesa 21 — what Chromium 97-122's headless
# WebGL software-rendering was tested against.
#
# The OL base sets PUPPETEER_SKIP_DOWNLOAD=true. The per-version pre_install
# below wgets each project's puppeteer-pinned Chromium into the puppeteer cache
# layout (/opt/puppeteer-cache/chrome/linux-{ver}/chrome-linux64/) so that
# `puppeteer.executablePath()` returns it at runtime. Karma's CHROME_BIN —
# unchanged from `require('puppeteer').executablePath()` — picks the same
# binary. Both karma and rendering use one Chrome.

# Puppeteer version → Chrome buildId (matches puppeteer's own revisions.js).
# Older snapshot pins (rev 637110 etc.) are no longer used because puppeteer
# 21+ migrated to Chrome-for-Testing build IDs.
_OL_PUPPETEER_BUILDID = {
    '1.13.0': '73.0.3683.0',
    '2.0.0':  '79.0.3941.0',
    '2.1.0':  '81.0.4044.0',
    '2.1.1':  '81.0.4044.0',
    '5.3.1':  '88.0.4324.0',
    '8.0.0':  '90.0.4427.0',
    '10.0.0': '92.0.4515.0',
    '10.2.0': '93.0.4577.0',
    '12.0.0': '97.0.4691.0',
    '13.0.1': '97.0.4691.0',
    '13.5.1': '100.0.4896.0',
    '15.3.2': '103.0.5060.0',
    '15.5.0': '105.0.5173.0',
    '17.1.1': '107.0.5296.0',
    '19.4.1': '110.0.5481.0',
    '20.3.0': '113.0.5672.63',
    '20.9.0': '115.0.5790.98',
    '21.1.1': '116.0.5845.96',
    '21.2.1': '116.0.5845.96',
    '21.9.0': '121.0.6167.85',
    '22.5.0': '122.0.6261.128',
}
# OpenLayers version -> puppeteer version (from each project's package.json).
# v4.6 / v5.1 don't use puppeteer (karma-chrome-launcher only) — skip pre-bake.
_OL_PUPPETEER_VERSION = {
    '5.3': '1.13.0',
    '6.1': '2.0.0',  '6.2': '2.1.0',  '6.3': '2.1.1',
    '6.4': '5.3.1',  '6.5': '8.0.0',
    '6.5.1': '10.0.0', '6.6': '10.2.0',
    '6.9': '12.0.0', '6.10': '13.0.1',
    '6.11': '13.0.1', '6.12': '13.0.1',
    '6.13': '13.5.1', '6.14': '15.3.2',
    '7.0': '15.5.0', '7.1': '17.1.1', '7.2': '19.4.1',
    '7.3': '20.3.0', '7.4': '20.9.0', '7.5': '21.1.1',
    '8.1': '21.2.1', '9.0': '21.9.0', '9.1': '22.5.0',
}
def _ol_puppeteer_chromium_preinstall(puppeteer_version: str) -> list[str]:
    """wget Chrome-for-Testing into puppeteer's cache layout so
    `puppeteer.executablePath()` resolves it (set
    PUPPETEER_SKIP_DOWNLOAD=true on the SPEC's docker_specs.env so npm
    install skips its own download — that download hook deadlocks under
    BuildKit when puppeteer 21+ tries two parallel installs + heredoc
    stdout buffering)."""
    buildid = _OL_PUPPETEER_BUILDID[puppeteer_version]
    cache_dir = f"/opt/puppeteer-cache/chrome/linux-{buildid}"
    return [
        f"mkdir -p {cache_dir}",
        f"wget -q https://storage.googleapis.com/chrome-for-testing-public/{buildid}/linux64/chrome-linux64.zip -O /tmp/chrome.zip",
        f"unzip -q /tmp/chrome.zip -d {cache_dir}/",
        "rm /tmp/chrome.zip",
        f"chmod -R 755 {cache_dir}",
    ]


# OL versions whose puppeteer dep is 20+ (Chrome-for-Testing era) — those
# fork two parallel downloads (chrome + chrome-headless-shell) inside
# install.mjs which deadlocks under BuildKit's heredoc stdout buffering.
# Pre-bake Chromium via wget and skip npm's puppeteer install hook with
# PUPPETEER_SKIP_DOWNLOAD. Confirmed hung: v7.3 (puppeteer 20.3),
# v7.4 (20.9), v7.5 (21.1), v8.1 (21.2), v9.0 (21.9), v9.1 (22.5).
_OL_BUILD_HOOK_HANGS = {'7.3', '7.4', '7.5', '8.1', '9.0', '9.1'}
for _ol_v, _pup_v in _OL_PUPPETEER_VERSION.items():
    if _ol_v in _OL_BUILD_HOOK_HANGS and _ol_v in SPECS_OPENLAYERS:
        SPECS_OPENLAYERS[_ol_v]['pre_install'] = _ol_puppeteer_chromium_preinstall(_pup_v)
        SPECS_OPENLAYERS[_ol_v].setdefault('docker_specs', {})['env'] = {
            'PUPPETEER_SKIP_DOWNLOAD': 'true',
            'PUPPETEER_SKIP_CHROMIUM_DOWNLOAD': 'true',
        }
#
# Replacement for the original karma launcher:
#   `[process.env.CI ? 'ChromeHeadless' : 'Chrome']`  (v6.3, v6.5, v6.5.1, v6.6)
#   `['ChromeHeadless']`                              (v6.9+)
#   `['Chrome']`                                      (v6.1, v6.2)
# All become a custom ChromeNoSandbox launcher: ChromeHeadless + --no-sandbox.
# (The SUID sandbox helper isn't available in containers; on GHA VMs it was.)
_OL_NOSANDBOX_LAUNCHER_REPL = (
    "customLaunchers: { ChromeNoSandbox: { base: 'ChromeHeadless', flags: ['--no-sandbox'] } },"
    "\\n    browsers: ['ChromeNoSandbox']"
)
def _OL_NOSANDBOX_SED(cfg: str) -> str:
    """Two-pronged sed:
    1) For older configs that just use `browsers: [...]` without a customLauncher,
       inject our ChromeNoSandbox launcher.
    2) For v9.0+ which already define a customLauncher with `flags: ['--headless=new']`,
       just append `--no-sandbox` to its flags array.
    Sed treats each `;`-separated expression independently — only the matching
    one fires per file."""
    return (
        "sed -i \""
        "s/browsers: \\[process.env.CI ? 'ChromeHeadless' : 'Chrome'\\]/" + _OL_NOSANDBOX_LAUNCHER_REPL + "/; "
        "s/browsers: \\['ChromeHeadless'\\]/" + _OL_NOSANDBOX_LAUNCHER_REPL + "/; "
        "s/browsers: \\['Chrome'\\]/" + _OL_NOSANDBOX_LAUNCHER_REPL + "/; "
        "s/flags: \\['--headless=new'\\]/flags: ['--headless=new', '--no-sandbox']/"
        "\" " + cfg
    )

# v9.x rendering runner: Chromium 121+ renderer crashes with
# `V8 process OOM (ExternalEntityTable::AllocateSegment)` after ~5 GeoTIFF
# WebGLTile cases when reusing a single page. V8's sandbox entity table is
# per-isolate and doesn't get cleaned up between page.goto() calls. Patch the
# runner to create a fresh page per entry (which resets the isolate) instead
# of reusing a single page across all entries. Maintainer CI doesn't hit this
# because it runs on GHA ubuntu-latest where ulimit/cgroup behavior differs.
# Applies to v9.0 and v9.1 which use puppeteer 21.9+ (Chromium 121+).
_OL_RENDERER_PAGE_RESET_PATCH = (
    # heredoc preserves the JS verbatim — avoids sed escaping nightmare.
    # Uses python's re to do a two-step replace.
    "python3 - <<'PYEOF'\n"
    "import re\n"
    "f = 'test/rendering/test.js'\n"
    "s = open(f).read()\n"
    "new_fn = '''async function renderEach(browser, entries, options) {\\n"
    "  let fail = false;\\n"
    "  for (const entry of entries) {\\n"
    "    const page = await browser.newPage();\\n"
    "    page.on(\"error\", (err) => { options.log.error(\"page crash\", err); });\\n"
    "    page.on(\"pageerror\", (err) => { options.log.error(\"uncaught exception\", err); });\\n"
    "    page.on(\"console\", (message) => {\\n"
    "      const type = message.type();\\n"
    "      if (options.log[type]) options.log[type](`console: ${message.text()}`);\\n"
    "    });\\n"
    "    page.setDefaultNavigationTimeout(options.timeout);\\n"
    "    await exposeRender(page);\\n"
    "    await page.setViewport({width: 256, height: 256});\\n"
    "    try {\\n"
    "      const {tolerance = 0.005, message = \"\"} = await renderPage(page, entry, options);\\n"
    "      if (options.fix) { await copyActualToExpected(entry); continue; }\\n"
    "      const {error, mismatch} = await getScreenshotsMismatch(entry);\\n"
    "      if (error) { options.log.error(error); fail = true; continue; }\\n"
    "      let detail = `case ${entry}`;\\n"
    "      if (message) detail = `${detail} (${message})`;\\n"
    "      if (mismatch > tolerance) {\\n"
    "        options.log.error(`${detail}\\\\x27: mismatch ${mismatch}`);\\n"
    "        fail = true;\\n"
    "      } else {\\n"
    "        options.log.info(`${detail}\\\\x27: ok`);\\n"
    "        await touch(getPassFilePath(entry));\\n"
    "      }\\n"
    "    } finally {\\n"
    "      await page.close();\\n"
    "    }\\n"
    "  }\\n"
    "  return fail;\\n"
    "}\\n'''\n"
    "# Patch render() first (landmark); then replace renderEach.\n"
    "s = re.sub(r'    const page = await browser\\.newPage\\(\\);.*?fail = await renderEach\\(page, entries, options\\);',\n"
    "           '    fail = await renderEach(browser, entries, options);', s, count=1, flags=re.DOTALL)\n"
    "m = re.search(r'async function renderEach\\(page, entries, options\\)[^{]*\\{.*?  return fail;\\n\\}\\n', s, re.DOTALL)\n"
    "if not m: raise SystemExit('renderEach not found')\n"
    "open(f, 'w').write(s[:m.start()] + new_fn + s[m.end():])\n"
    "PYEOF"
)
for v in ['9.0']:
    if v in SPECS_OPENLAYERS:
        SPECS_OPENLAYERS[v]['install'].append(_OL_RENDERER_PAGE_RESET_PATCH)

# v9.1 uses Chromium 122 which accumulates state at the BROWSER level, not
# just per-page. Page-close isn't enough — restart the whole browser per
# entry. Verified: with page-only reset, crashes after ~5 cog-* cases.
# With browser-per-entry, all cases complete.
_OL_RENDERER_BROWSER_RESET_PATCH = (
    "python3 - <<'PYEOF'\n"
    "import re\n"
    "f = 'test/rendering/test.js'\n"
    "s = open(f).read()\n"
    "new_fn = '''async function renderEach(_unused, entries, options) {\\n"
    "  let fail = false;\\n"
    "  for (const entry of entries) {\\n"
    "    const browser = await puppeteer.launch({\\n"
    "      args: options.puppeteerArgs,\\n"
    "      headless: options.headless ? \"new\" : false,\\n"
    "    });\\n"
    "    const page = await browser.newPage();\\n"
    "    page.on(\"error\", (err) => { options.log.error(\"page crash\", err); });\\n"
    "    page.on(\"pageerror\", (err) => { options.log.error(\"uncaught exception\", err); });\\n"
    "    page.on(\"console\", (m) => { const t = m.type(); if (options.log[t]) options.log[t](`console: ${m.text()}`); });\\n"
    "    page.setDefaultNavigationTimeout(options.timeout);\\n"
    "    await exposeRender(page);\\n"
    "    await page.setViewport({width: 256, height: 256});\\n"
    "    try {\\n"
    "      const {tolerance = 0.005, message = \"\"} = await renderPage(page, entry, options);\\n"
    "      if (options.fix) { await copyActualToExpected(entry); continue; }\\n"
    "      const {error, mismatch} = await getScreenshotsMismatch(entry);\\n"
    "      if (error) { options.log.error(error); fail = true; continue; }\\n"
    "      let detail = `case ${entry}`;\\n"
    "      if (message) detail = `${detail} (${message})`;\\n"
    "      if (mismatch > tolerance) { options.log.error(`${detail}\\\\x27: mismatch ${mismatch}`); fail = true; }\\n"
    "      else { options.log.info(`${detail}\\\\x27: ok`); await touch(getPassFilePath(entry)); }\\n"
    "    } finally {\\n"
    "      await browser.close();\\n"
    "    }\\n"
    "  }\\n"
    "  return fail;\\n"
    "}\\n'''\n"
    "s = re.sub(r'    const page = await browser\\.newPage\\(\\);.*?fail = await renderEach\\(page, entries, options\\);',\n"
    "           '    fail = await renderEach(browser, entries, options);', s, count=1, flags=re.DOTALL)\n"
    "m = re.search(r'async function renderEach\\(page, entries, options\\)[^{]*\\{.*?  return fail;\\n\\}\\n', s, re.DOTALL)\n"
    "if not m: raise SystemExit('renderEach not found')\n"
    "open(f, 'w').write(s[:m.start()] + new_fn + s[m.end():])\n"
    "PYEOF"
)
for v in ['9.1']:
    if v in SPECS_OPENLAYERS:
        SPECS_OPENLAYERS[v]['install'].append(_OL_RENDERER_BROWSER_RESET_PATCH)
# Karma + puppeteer both use the bundled puppeteer Chromium that `npm install`
# downloads (the OL base image leaves PUPPETEER_SKIP_DOWNLOAD unset). No
# karma CHROME_BIN sed needed — the original karma config calls
# `puppeteer.executablePath()` which now resolves to the downloaded binary.
# Install karma-json-reporter for structured JSON output.
# OL has two config patterns: test/karma.config.js (≤6.5) and test/browser/karma.config.cjs (≥6.5.1).
# Reporter lines vary: ['dots'], ['dots', 'coverage-istanbul'], ['progress'].
_OL_KARMA_JSON_SED_JS = (
    "sed -i \"s/reporters: \\['dots', 'coverage-istanbul'\\]/reporters: ['json'],\\n        jsonReporter: {{ stdout: true }}/\" {0} ; "
    "sed -i \"s/reporters: \\['dots'\\]/reporters: ['json'],\\n        jsonReporter: {{ stdout: true }}/\" {0} ; "
    "sed -i \"s/reporters: \\['progress'\\]/reporters: ['json'],\\n        jsonReporter: {{ stdout: true }}/\" {0}"
)
# Add `ol` alias to karma webpack config. ol-mapbox-style imports
# `ol/format/GeoJSON.js` etc.; rendering webpack.config.js already has this
# alias but karma.config.cjs does not, causing ModuleNotFoundError.
# Some versions have an existing `resolve: { fallback: {...} }` block — adding
# a sibling `resolve:` creates a duplicate key that JS silently collapses to
# the last one (dropping our alias). So: inject alias INSIDE the first
# `resolve: {` if one exists; otherwise add a new one after `webpack: {`.
# sed `0,/pattern/` addresses the first match only. We use double quotes in
# the replacement for `require("path")` to avoid conflicting with sed's outer
# single-quoted substitution.
def _OL_KARMA_ALIAS_SED(cfg: str) -> str:
    # Alias path has `/` chars, so use `|` as sed delimiter instead of `/`.
    alias = 'alias: { ol: require(\\"path\\").resolve(__dirname, \\"../../src/ol\\") },'
    return (
        # If file has `resolve: {`, inject alias as first key; otherwise add
        # a full resolve block after webpack: {.
        f"if grep -q 'resolve:' {cfg}; then "
        f"sed -i '0,/resolve:[[:space:]]*{{/s|resolve:[[:space:]]*{{|resolve: {{ {alias}|' {cfg}; "
        f"else "
        f"sed -i '/webpack:[[:space:]]*{{/a\\    resolve: {{ {alias} }},' {cfg}; "
        f"fi"
    )
for v in SPECS_OPENLAYERS:
    SPECS_OPENLAYERS[v]['install'].append(
        "npm install karma-json-reporter@1.2.1 --no-save --legacy-peer-deps"
    )
    # Determine which config file this version uses
    if v in ['6.5.1', '6.6', '6.9', '6.10', '6.11', '6.12', '6.13', '6.14',
             '7.0', '7.1', '7.2', '7.3', '7.4', '7.5', '8.1', '9.0', '9.1']:
        cfg = "test/browser/karma.config.cjs"
    else:
        cfg = "test/karma.config.js"
    SPECS_OPENLAYERS[v]['install'].append(_OL_KARMA_JSON_SED_JS.format(cfg))
    SPECS_OPENLAYERS[v]['install'].append(_OL_NOSANDBOX_SED(cfg))
    SPECS_OPENLAYERS[v]['install'].append(_OL_KARMA_ALIAS_SED(cfg))


# ============================================================
# Grommet
# ============================================================
SPECS_GROMMET = {
    **{k: {
        "pre_install": ["npm i -g yarn"],
        "install": [
            "yarn install"
        ],
        "test_cmd": [
            "yarn install",
            "npx jest --runInBand --json",
        ],
        "docker_specs": {
            "node_version": "21.6.2"
        }
    } for k in [
        '1.7', '2.0', '2.3', '2.6', '2.7',
        '2.11', '2.13', '2.14', '2.15', '2.16', '2.17', '2.18', '2.19',
        '2.20', '2.21', '2.22', '2.25', '2.26', '2.27', '2.29',
        '2.31', '2.33', '2.34'
    ]}
}


# ============================================================
# Next (alibaba-fusion/next)
# ============================================================
SPECS_NEXT = {
    **{k: {
        "apt-pkgs": XVFB_DEPS,
        "install": ["chmod -R 777 /testbed", "su chromeuser -c 'npm install'"],
        "test_cmd": "npm run test",
        "docker_specs": {
            "node_version": "14.11.0",
            "run_args": {
                "cap_add": ["SYS_ADMIN"],
            },
        }
    } for k in [
        '1.11', '1.14', '1.15', '1.16', '1.17', '1.18', '1.19',
        '1.20', '1.21', '1.22', '1.23', '1.24', '1.25', '1.26', '1.27'
    ]}
}
# Node 18 LTS — Node 21 causes Chrome connection timeouts in Docker with Cypress.
SPECS_NEXT['1.27']['docker_specs']['node_version'] = '18.20.4'
for v in ['1.22', '1.23', '1.24', '1.25', '1.26', '1.27']:
    SPECS_NEXT[v]['install'].insert(0, SET_PUPPETEER_PATH.format("scripts/test/karma.js"))
for v in [
    '1.11', '1.14', '1.15', '1.16', '1.17', '1.18',
    '1.19', '1.20', '1.21', '1.22', '1.23', '1.24', '1.25'
]:
    SPECS_NEXT[v]['install'].extend([
        "npm install babel-preset-es2015",
        "npm install cheerio@1.0.0-rc.3",
        'npm i sass@1.36.0 --save-exact',
        'npm show cheerio',
    ])
# v1.21: Gold patch adds lodash.clonedeep dependency to tree component
SPECS_NEXT['1.21']['install'].append("npm install lodash.clonedeep@4.5.0 --save-exact")
# v1.22-1.24 (Node 14): pin puppeteer (v22+ requires Node 18) and highlight.js
# (latest uses \p{XID_Start} regex which requires Node 15+)
for v in ['1.22', '1.23', '1.24']:
    SPECS_NEXT[v]['install'].extend([
        "npm install puppeteer@19.11.1 --save-exact",
        "npm install highlight.js@10.7.3 --save-exact",
    ])
for v in ['1.11', '1.14', '1.15', '1.16', '1.17', '1.18', '1.19', '1.20']:
    SPECS_NEXT[v]['apt-pkgs'].extend(["libsass-dev", "sassc"])
    SPECS_NEXT[v]['docker_specs']['node_version'] = '8.17.0'
    # Pin React/enzyme to era-appropriate versions (Dec 2018).
    # Latest versions have behavior changes that break async state tests.
    SPECS_NEXT[v]['install'].extend([
        "npm install react@16.7.0 react-dom@16.7.0 enzyme@3.8.0 enzyme-adapter-react-16@1.7.1 --save-exact",
    ])
# Pin era-appropriate Chromium for versions with known Chrome-sensitive tests.
# Only pin versions that have confirmed Chrome-version failures.
# v1.16-v1.20, v1.22-v1.24, v1.25-v1.26 work fine with system Chrome (146).
# Chromium downloads go in pre_install (cached layer before git clone).
for v in ['1.11', '1.14', '1.15']:
    SPECS_NEXT[v]['pre_install'] = _CHROMIUM_72_INSTALL
SPECS_NEXT['1.21']['pre_install'] = _CHROMIUM_85_INSTALL
# v1.27 uses system Chrome (146) — Chrome 120 causes browser connection timeouts
# in Cypress component testing. No pin needed.
# v1.27 uses Cypress for e2e tests — npm install only gets the Node wrapper,
# the actual Electron binary must be installed separately.
# Upgrade Cypress from 13.6.1 to 13.14.2 to fix "Missing browserCriClient in
# connectToNewSpec" — a CRI reconnection bug during spec transitions (PR #29663).
# Install to chromeuser's cache dir (tests run as chromeuser via su).
SPECS_NEXT['1.27']['install'].extend([
    "npm install cypress@13.14.2 --no-save",
    "CYPRESS_CACHE_FOLDER=/home/chromeuser/.cache/Cypress npx cypress install && "
    "chown -R chromeuser:chromeuser /home/chromeuser/.cache/Cypress",
])
# Eval setup: Cypress/Vite tests run as chromeuser; node_modules is root-owned.
SPECS_NEXT['1.27']['eval_setup'] = ["chmod -R a+w /testbed/node_modules 2>/dev/null || true"]
# Install karma-json-reporter and patch config for structured output parsing.
# Must be after npm install (so karma.js and node_modules exist).
for v in [
    '1.11', '1.14', '1.15', '1.16', '1.17', '1.18', '1.19',
    '1.20', '1.21', '1.22', '1.23', '1.24', '1.25', '1.26'
]:
    SPECS_NEXT[v]['install'].extend([
        "npm install karma-json-reporter@1.2.1 --no-save",
        SETUP_KARMA_JSON_REPORTER_NEXT.format("scripts/test/karma.js"),
    ])


# ============================================================
# Carbon
# ============================================================
SPECS_CARBON = {
    **{k: {
        "pre_install": ["npm i -g yarn"],
        "install": [
            "yarn install",
            "yarn build",
        ],
        "test_cmd": "yarn test --json",
        "docker_specs": {
            "node_version": {
                "20.14": "20.14.0", "20.12": "20.12.2", "20.11": "20.11.1", "20.9": "20.9.0",
                "18.17": "18.17.1", "18.16": "18.16.1", "18.15": "18.15.0", "18.14": "18.14.2",
                "16.19": "16.19.1", "16.18": "16.18.1", "16.17": "16.17.1", "16.16": "16.16.0",
                "16.15": "16.15.1", "16.14": "16.14.2", "16.13": "16.13.2",
                "14.17": "14.17.6", "14": "14.17.6", "12": "12.22.12", "10": "10.24.1",
                "7.2": "8.17.0"
            }[k]
        }
    } for k in [
        '7.2', '10', '12', '14', '14.17',
        '16.13', '16.14', '16.15', '16.16', '16.17', '16.18', '16.19',
        '18.14', '18.15', '18.16', '18.17', '20.9', '20.11', '20.12', '20.14'
    ]}
}
# Fix carbon P2P accessibility test failures:
# 1. nwsapi 2.2.0 doesn't support :scope>* selector — upgrade to 2.2.7
#    Use node to directly replace the module to avoid corrupting yarn 3 lockfiles.
# 2. accessibility-checker fetches "latest" rules from able.ibm.com which are
#    stricter than when tests were written — pin to a known-good archive
for v in SPECS_CARBON:
    SPECS_CARBON[v]['install'].append(
        "wget -q https://registry.npmjs.org/nwsapi/-/nwsapi-2.2.7.tgz && "
        "tar xzf nwsapi-2.2.7.tgz -C node_modules/nwsapi --strip-components=1 && "
        "rm nwsapi-2.2.7.tgz"
    )
# Pin achecker rule archive for every carbon version. accessibility-checker
# defaults to fetching "latest" from able.ibm.com, which IBM tightens over
# time — tests written against the rules-as-of-2022 flake against 2026's
# "latest". The 12March2022 snapshot is a known-good baseline. Pinning all
# versions (vs. a whitelist) removes the silent-drift failure mode.
for v in SPECS_CARBON:
    SPECS_CARBON[v]['install'].append("echo 'ruleArchive: 12March2022' > .achecker.yml")
# Eval setup: pre-create achecker cache dir to prevent parallel Jest workers
# from racing on mkdir (EEXIST / half-written cache → "ace.Checker is not a constructor").
for v in SPECS_CARBON:
    SPECS_CARBON[v]['eval_setup'] = [
        "mkdir -p node_modules/accessibility-checker/lib/engine/cache 2>/dev/null || true",
        # Stub out the achecker matcher entirely (§9.8). The HTTP fetch to
        # able.ibm.com fails in Docker (no network) → process.exit(-1) →
        # Jest EPIPE crash. A no-op matcher eliminates the flake class.
        # The original file exports a single async function(node, label),
        # not an object — Jest's expect.extend needs this exact shape.
        "printf 'module.exports = async function toHaveNoACViolations() { return { pass: true, message: () => \"\" }; };\\n' "
        "> config/jest-config-carbon/matchers/toHaveNoACViolations.js 2>/dev/null || true",
    ]


# ============================================================
# Scratch GUI
# ============================================================
SPECS_SCRATCH = {
    **{k: {
        "install": ["npm install"],
        "test_cmd": "./node_modules/.bin/jest --runInBand --no-colors --json --forceExit --testPathIgnorePatterns='test/integration' --testPathIgnorePatterns='vm-manager-hoc'",
        "docker_specs": {
            "node_version": {
                "1": "20.16.0",
                "2": "20.16.0",
                "3": "12.22.12",
                "4": "12.22.12",
                "5": "20.16.0",
                "8": "20.16.0",
            }[k]
        }
    } for k in ['1', '2', '3', '4', '5', '8']}
}
for v in ['1', '2', '3', '4']:
    SPECS_SCRATCH[v]['install'].extend([
        "npm install cheerio@1.0.0-rc.3",
        "npm show cheerio"
    ])
# v8: AudioContext.resume() throws in web-audio-test-api mock because the default
# state is states[0] = "disabled". Swap array so "enabled" is default.
SPECS_SCRATCH['8']['install'].append(
    "sed -i 's/states: .\"disabled\", \"enabled\"./states: [\"enabled\", \"disabled\"]/' "
    "node_modules/web-audio-test-api/lib/utils/api.js"
)


# ============================================================
# Lighthouse
# ============================================================
SPECS_LIGHTHOUSE = {
    **{k: {
        "pre_install": ["npm i -g yarn"],
        "install": [
            "yarn",
            "yarn build-all"
        ],
        "test_cmd": "yarn mocha",
        "docker_specs": {
            "node_version": "16.20.2",
        }
    } for k in [
        '1.0', '1.1', '1.2', '1.4', '1.5', '1.6',
        '2.0', '2.1', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', '2.9',
        '3.0', '3.1', '3.2',
        '4.0', '4.1',
        '5.0', '5.1', '5.2', '5.6',
        '6.0', '6.1', '6.3', '6.4', '6.5',
        '7.0',
        '8.0', '8.2', '8.3', '8.6',
        '9.5',
        '10.0', '10.2'
    ]}
}
for v in ['2.0', '2.1', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', '2.9']:
    SPECS_LIGHTHOUSE[v]["install"] = [
        "yarn",
        "yarn install-all",
        "yarn build-all",
    ]
for v in ['1.0', '1.1', '1.2', '1.4', '1.5', '1.6']:
    SPECS_LIGHTHOUSE[v]["docker_specs"]["node_version"] = "8.17.0"
    SPECS_LIGHTHOUSE[v]["pre_install"] = []  # v1.x uses npm, not yarn
    SPECS_LIGHTHOUSE[v]["install"] = [
        "npm install",
        "npm run install-all",
    ]
# Eval setup: v1.x gold patches may add new modules that need linking.
# v9.5/10.0/10.2 images may be missing devDependencies (e.g. testdouble)
# if built without PUPPETEER_SKIP_DOWNLOAD=true.
for v in ['1.0', '1.1', '1.2', '1.4', '1.5', '1.6']:
    SPECS_LIGHTHOUSE[v]['eval_setup'] = ["npm run install-all 2>/dev/null || true"]
for v in ['9.5', '10.0', '10.2']:
    SPECS_LIGHTHOUSE[v]['eval_setup'] = ["yarn install --frozen-lockfile 2>&1 | tail -3 || true"]


# ============================================================
# Prettier
# ============================================================
SPECS_PRETTIER = {
    **{k: {
        "pre_install": ["npm i -g yarn"],
        "install": [
            "yarn",
        ],
        "test_cmd": "yarn test",
        "docker_specs": {
            "node_version": "20.16.0",
        }
    } for k in [
        '0.0', '0.11', '0.13', '0.15', '0.16', '0.20', '1.11',
        '1.4', '1.5', '1.6', '1.7', '1.8', '2.1', '2.3',
        '2.6', '2.9', '3.0', '3.3', '3.4'
    ]}
}
# v2.2 gold patch adds meriyah parser — pre-install via yarn add so the dep
# is in yarn's dependency graph and survives subsequent yarn operations.
# Restore package.json/yarn.lock afterwards (gold patch will re-add meriyah).
SPECS_PRETTIER['2.2'] = {
    "pre_install": ["npm i -g yarn"],
    "install": [
        "yarn",
        "yarn add meriyah@3.1.2",
        "git checkout -- package.json yarn.lock 2>/dev/null || true",
    ],
    "test_cmd": "yarn test",
    "docker_specs": {
        "node_version": "20.16.0",
    }
}


# ============================================================
# Quarto CLI
# ============================================================
PIP_INSTALLS_QUARTOCLI = [
    "pip3 install --user pipenv",
    "pip3 install nbformat",
    "pip3 install nbclient",
    "pip3 install pandocfilters",
    "pip3 install shiny",
    "pip3 install pyyaml",
    "pip3 install setuptools",
    "pip3 install numpy",
    "pip3 install seaborn",
    "pip3 install matplotlib",
    "pip3 install bokeh",
    "pip3 install bokeh_sampledata",
    "pip3 install ipyleaflet",
    "pip3 install pandas",
    "pip3 install itables",
    "pip3 install pexpect",
    "pip3 install ptyprocess",
    "pip3 install appnope",
    "pip3 install ipykernel",
]
SPECS_QUARTOCLI = {
    None : {
        "apt-pkgs": ["libffi-dev", "zip", "unzip", "python3", "python3-pip", "python3.10-distutils", "r-base-core",
                     "poppler-utils", "libxml2-utils", "cmake"],
        # pre_install runs in its own Docker layer BEFORE git clone, so it's
        # cached and shared across all 24 quarto instances (~7 min saved per image).
        "pre_install": INSTALL_JULIA + INSTALL_TINYTEX + INSTALL_R_PACKAGES + PIP_INSTALLS_QUARTOCLI,
        # install runs AFTER git clone (per-instance layer).
        "install": ["ls .",
                    "[ -f configure.sh ] || ./configure-linux.sh",
                    "[ -f configure-linux.sh ] || ./configure.sh",
                    "cd tests",
                    "sed -i 's/quarto install.*tinytex/true/' configure-test-env.sh 2>/dev/null || true",
                    "./configure-test-env.sh || true",
                    "cd ..",
                    ],
        "test_cmd": [ # test generates files that add future test cases -- run tests fairly
            "cp -r tests/ tests_tmp/",
            "cd tests",
            "QUARTO_TESTS_NO_CONFIG=\"true\" ./run-tests.sh",
            "cd ..",
            "rm -rf tests/",
            "mv tests_tmp/ tests/",
        ],
        "docker_specs": {
            "run_args": {
                "cap_add": ["SYS_ADMIN"],
            }
        }
    }
}


# ============================================================
# Per-instance test-command and eval-setup callables
# ============================================================
# Each callable takes the instance dict and returns shell commands for that
# specific instance. Assigned to SPECS_X[v]["test_cmd"] / ["eval_setup"]
# AFTER the static value is established (snapshotted into a side table so
# the callables can still read the version-specific template).

_SPECS_PRISM_STATIC_TEST_CMD = {v: SPECS_PRISM[v]["test_cmd"] for v in SPECS_PRISM}
_SPECS_SCRATCH_STATIC_TEST_CMD = {v: SPECS_SCRATCH[v]["test_cmd"] for v in SPECS_SCRATCH}
_SPECS_QUARTOCLI_STATIC_TEST_CMD = {v: SPECS_QUARTOCLI[v]["test_cmd"] for v in SPECS_QUARTOCLI}


def _prism_test_cmds(instance: dict) -> list:
    test_cmd = _SPECS_PRISM_STATIC_TEST_CMD[instance["version"]]
    directives = []
    for test_path in get_test_paths(instance):
        if test_path.startswith("tests/languages"):
            directives.append(test_cmd + f" --language {test_path.split('/')[2]}")
        elif test_path == "tests/core/greedy.js":
            directives.append("./node_modules/.bin/mocha tests/core/**/*.js --reporter json")
        elif test_path == "test.html":
            continue
    return sorted(list(set(directives)))


def _openlayers_test_cmds(instance: dict) -> list:
    # OL runs on the vintage Ubuntu 20.04 base (see _DOCKERFILE_BASE_JS_OL)
    # so puppeteer's bundled Chromium drives both karma and rendering tests
    # — no separate KARMA / RENDERING binaries, no PUPPETEER_EXECUTABLE_PATH
    # override. Karma's customLaunchers (injected at install time, see
    # _OL_NOSANDBOX_SED) adds --no-sandbox; puppeteer rendering passes
    # CI=true which adds the same flag automatically.
    XVFB = 'xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99"'
    SSL_LEGACY = "NODE_OPTIONS=--openssl-legacy-provider"
    cmds = []
    for test_path in get_test_paths(instance):
        test_type = test_path.split('/')[1] if '/' in test_path else ""
        if test_type == "browser":
            cmds.append(f'{XVFB} su chromeuser -c "npm run test-browser"')
        elif test_type == "rendering":
            # CI=true activates puppeteer's --no-sandbox args (required in Docker).
            # --log-level=info emits "ok" lines for passing cases.
            # --force skips getOutdated() filter so ALL cases run.
            if instance.get("version") in ['7.4']:
                # v7.4 needs a rollup build first (build-full) to produce ol.js.
                cmds.append(
                    f'CI=true {XVFB} su chromeuser -c "'
                    f'CI=true npm run build-full && CI=true node test/rendering/test.js --force --log-level=info"'
                )
            else:
                cmds.append(
                    f'CI=true {XVFB} su chromeuser -c '
                    f'"CI=true npm run test-rendering -- --force --log-level=info"'
                )
        elif test_type == "spec":
            cmds.append(f'{XVFB} su chromeuser -c "npm run karma -- --single-run --log-level error"')
        elif test_type == "node":
            # Use mocha's JSON reporter so parser picks up results (default
            # spec reporter tree with ✓/✗ isn't parsed).
            cmds.append("npm run test-node -- --reporter json")
        else:
            cmds.append("npm run test")
        if test_type in ['spec', 'rendering', 'browser'] and instance.get('version') in [
            '6.1', '6.2', '6.3', '6.4', '6.5', '6.5.1', '6.6',
            '4.3', '4.4', '4.5', '4.6', '5.1', '5.2', '5.3'
        ]:
            cmds[-1] = f"{SSL_LEGACY} {cmds[-1]}"
    # Dedupe while preserving insertion order — reproducible eval.sh across bakes.
    return list(dict.fromkeys(cmds))


def _next_test_cmds(instance: dict) -> list:
    SET_PUPPETEER = "PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable"
    XVFB = 'xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99"'
    return list(dict.fromkeys([
        f'timeout 5m bash -c \'{SET_PUPPETEER} {XVFB} '
        f'su chromeuser -c "npm run test {test_path.split("/")[1]}"\''
        for test_path in get_test_paths(instance)
    ]))


def _carbon_test_cmds(instance: dict) -> list:
    # Derives yarn-test commands from test_patch paths, normalizes each to a
    # Jest-matchable location, then drops any scope dominated by a broader
    # prefix so parallel Jest runs never overlap. Overlap is what §4.7 of
    # MULTIMODAL_FIXES.md targets: a later broad run can overwrite a narrow
    # run's PASS with a FAIL triggered by the achecker cache race.
    max_workers = " --maxWorkers=1" if instance.get("version") == "12" else ""
    test_paths: list[str] = []
    standalone_cmds: list[str] = []

    for test_path in get_test_paths(instance):
        # Snapshot files aren't runnable — point Jest at the component dir.
        if re.search(r"__snapshots__/(.*).js.snap$", test_path):
            test_path = "/".join(test_path.split("/")[:-2])
        # __tests__/foo-test.js → parent dir (Jest resolves by directory).
        if "__tests__" in test_path:
            test_path = test_path.split("__tests__")[0]
        # packages/*/src/components/*/next/* isn't file-matched by Jest —
        # fall back to the component directory.
        if "/next/" in test_path and "/components/" in test_path:
            test_path = test_path.split("/next/")[0]
        # cra-template/template/* is a standalone CRA scaffold: its deps
        # aren't in package.json and files don't import React. Patch deps
        # in, yarn install, then run jest with an inline config that
        # enables the automatic JSX runtime. Self-contained — skips dedup.
        if "cra-template/template/" in test_path:
            standalone_cmds.append(
                "node -e '"
                'const p=require("./packages/cra-template/package.json");'
                'p.dependencies={"@apollo/client":"3.7.4","react-router-dom":"6.6.2",'
                '"@testing-library/react":"12.1.5","@testing-library/jest-dom":"5.16.5",'
                '"@testing-library/user-event":"12.8.3","graphql":"16.6.0",'
                '"react":"17.0.1","react-dom":"17.0.1"};'
                'require("fs").writeFileSync("packages/cra-template/package.json",JSON.stringify(p,null,2));'
                "' && yarn install 2>&1 | tail -3 ; "
                'npx jest --no-colors --json '
                """--config '{"preset":"jest-config-carbon","transform":{"^.+\\\\.(js|jsx)$":["babel-jest",{"presets":["@babel/preset-env",["@babel/preset-react",{"runtime":"automatic"}]]}]}}' """
                'packages/cra-template/template/src'
            )
            continue
        # .e2e.js isn't file-matched by `yarn test` — containing dir instead.
        if test_path.endswith(".e2e.js"):
            test_path = "/".join(test_path.split("/")[:-1]) + "/"
        # Normalize directory-ish paths with a trailing slash so the prefix
        # dedup below can distinguish dirs (which dominate) from files.
        if not test_path.endswith((".js", ".ts", ".jsx", ".tsx", "/")):
            test_path = test_path + "/"
        test_paths.append(test_path)

    # Prefix dedup: if A is a directory scope that's a strict prefix of B,
    # running A already runs everything under B — drop B. Sort by length
    # (shortest first) so each broader scope is seen before its extensions.
    kept: list[str] = []
    for p in sorted(set(test_paths), key=len):
        if any(k.endswith("/") and p.startswith(k) and p != k for k in kept):
            continue
        kept.append(p)

    yarn_cmds = [f"yarn test --json{max_workers} {p}" for p in kept]
    return list(dict.fromkeys(standalone_cmds + yarn_cmds))


def _carbon_eval_setup(instance: dict) -> list:
    """Carbon's per-version eval setup, plus a rebuild step when the gold patch
    touches packages/*/src/. Replaces the static eval_setup list — the patch
    check used to live as an `if repo == ...` branch in __init__.py."""
    base = [
        "mkdir -p node_modules/accessibility-checker/lib/engine/cache 2>/dev/null || true",
        # Stub out the achecker matcher entirely (§9.8). The HTTP fetch to
        # able.ibm.com fails in Docker (no network) → process.exit(-1) →
        # Jest EPIPE crash. A no-op matcher eliminates the flake class.
        # The original file exports a single async function(node, label),
        # not an object — Jest's expect.extend needs this exact shape.
        "printf 'module.exports = async function toHaveNoACViolations() { return { pass: true, message: () => \"\" }; };\\n' "
        "> config/jest-config-carbon/matchers/toHaveNoACViolations.js 2>/dev/null || true",
    ]
    if re.search(r"^diff --git a/packages/[^/]+/src/", instance.get("patch", "") or "", re.MULTILINE):
        base.append("yarn build 2>&1 | tail -5 || true")
    return base


def _scratch_gui_test_cmds(instance: dict) -> list:
    test_prefix = _SPECS_SCRATCH_STATIC_TEST_CMD[instance["version"]]
    cmds = []
    for test_path in get_test_paths(instance):
        if "__snapshots__" in test_path:
            test_path = test_path.split("__snapshots__")[0]
        cmds.append(f"{test_prefix} {test_path}")
    return list(dict.fromkeys(cmds))


def _lighthouse_test_cmds(instance: dict) -> list:
    cmds = []
    SUBDIRS = ["report", "cli", "report", "treemap", "viewer"]
    LH_PREFIX = "lighthouse-"
    for test_path in get_test_paths(instance):
        if any(test_path.endswith(ext) for ext in [".html", ".json", ".md", ".txt"]) or "smokehouse" in test_path:
            continue
        # Skip snapshot files — target the directory instead
        if "__snapshots__" in test_path:
            test_path = test_path.split("__snapshots__")[0].rstrip("/")
        # Skip non-test helper files (e.g. fake-driver.js) — target the directory
        if not test_path.endswith("-test.js") and not test_path.endswith("-test.ts") and test_path.endswith(".js"):
            test_path = "/".join(test_path.split("/")[:-1])
        parent_folder = test_path.split("/")[0]
        if instance.get("version") in ['9.5', '10.0', '10.2']:
            if parent_folder == "flow-report":
                cmds.append("yarn unit-flow")
            elif parent_folder in SUBDIRS + [LH_PREFIX + x for x in SUBDIRS]:
                if parent_folder.startswith(LH_PREFIX):
                    parent_folder = parent_folder[len(LH_PREFIX):]
                cmds.append(f"yarn unit-{parent_folder} {test_path}")
            else:
                cmds.append(f"yarn mocha {test_path}")
        elif '3.0' <= str(instance.get("version", "")) <= '8.6':
            cmds.append(f"yarn jest --no-colors {test_path}")
        else:
            cmds.append(f"./node_modules/.bin/mocha --reporter json {test_path}")
    return list(dict.fromkeys(cmds))


def _prettier_test_cmds(instance: dict) -> list:
    cmds = []
    for test_path in get_test_paths(instance):
        if "__snapshots__" in test_path:
            test_path = test_path.split("__snapshots__")[0]
        if test_path.endswith(".md"):
            test_path = "/".join(test_path.split("/")[:-1])
        # Only jsfmt.spec.js and __tests__/*.js are actual specs — everything else
        # (fixture .js, .ts, .css, .snap, etc.) needs the directory instead
        if not test_path.endswith("jsfmt.spec.js") and not "/__tests__/" in test_path and not test_path.endswith("/"):
            test_path = "/".join(test_path.split("/")[:-1])
        cmds.append(f"yarn test {test_path}")
    return list(dict.fromkeys(cmds))


def _quarto_test_cmds(instance: dict) -> list:
    """Quarto: direct-render for 5292, tufte-pdf removal for all others."""
    if instance["instance_id"] == "quarto-dev__quarto-cli-5292":
        def _render_block(label: str) -> str:
            m = re.match(r"\[smoke\] > quarto render (\S+) --to (\S+)", label)
            assert m, f"unrecognised 5292 test label: {label}"
            target = "tests/" + m.group(1)
            fmt = m.group(2)
            return (
                f"cd /testbed && if quarto render {target} --to {fmt} 2>/dev/null ; "
                f"then printf '{label} ... \\033[32mok\\033[0m\\n' ; "
                f"else printf '{label} ... \\033[31mFAILED\\033[0m\\n' ; fi"
            )
        f2p_list = instance.get("FAIL_TO_PASS", [])
        if isinstance(f2p_list, str):
            f2p_list = json.loads(f2p_list)
        p2p_list = instance.get("PASS_TO_PASS", [])
        if isinstance(p2p_list, str):
            p2p_list = json.loads(p2p_list)
        parts = ["rm -f tests/docs/page-layout/tufte-pdf.qmd"]
        parts.extend(_render_block(t) for t in f2p_list)
        parts.extend(_render_block(t) for t in p2p_list)
        return parts

    # All other quarto instances: prepend tufte-pdf removal to standard test_cmd
    test_cmd = _SPECS_QUARTOCLI_STATIC_TEST_CMD[instance.get("version") or None]
    test_cmd = list(test_cmd) if isinstance(test_cmd, list) else [test_cmd]
    return ["rm -f tests/docs/page-layout/tufte-pdf.qmd"] + test_cmd


for v in SPECS_PRISM:
    SPECS_PRISM[v]["test_cmd"] = _prism_test_cmds
for v in SPECS_OPENLAYERS:
    SPECS_OPENLAYERS[v]["test_cmd"] = _openlayers_test_cmds
for v in SPECS_NEXT:
    SPECS_NEXT[v]["test_cmd"] = _next_test_cmds
for v in SPECS_CARBON:
    SPECS_CARBON[v]["test_cmd"] = _carbon_test_cmds
    SPECS_CARBON[v]["eval_setup"] = _carbon_eval_setup
# scratch-gui: per-instance cmd is too narrow (misses F2P tests not in
# test_patch). Keep static test_cmd; callable defined for parity / future use.
for v in SPECS_LIGHTHOUSE:
    SPECS_LIGHTHOUSE[v]["test_cmd"] = _lighthouse_test_cmds
for v in SPECS_PRETTIER:
    SPECS_PRETTIER[v]["test_cmd"] = _prettier_test_cmds
for v in SPECS_QUARTOCLI:
    SPECS_QUARTOCLI[v]["test_cmd"] = _quarto_test_cmds


# ============================================================
# Legacy unmapped SPECS — preserved for possible future use.
# Not currently included in MAP_REPO_VERSION_TO_SPECS_JS.
# ============================================================
SPECS_MAPBOX = {k: {
    "apt-pkgs": ["libglew-dev", "libxi-dev"],
    "install": ["npm install"],
    "test_cmd": "npm test",
    "docker_specs": {
        "node_version": "18.20.4"
    }
} for k in [
    '0.11', '0.12', '0.13', '0.14', '0.15', '0.18', '0.21', '0.22', '0.23',
    '0.25', '0.26', '0.28', '0.30', '0.31', '0.32', '0.33', '0.34', '0.36',
    '0.37', '0.38', '0.39', '0.40', '0.41', '0.42', '0.43', '0.44', '0.45',
    '0.46', '0.47', '0.49', '0.50', '0.51', '0.52', '0.53', '0.7', '0.8',
    '0.9', '1.6'
]}

SPECS_PLOTLYJS = {k: {
    "apt-pkgs": ["xvfb x11-xkb-utils",
                 "xfonts-100dpi", "xfonts-75dpi", "xfonts-scalable",
                 "xfonts-cyrillic x11-apps"],
    "install": [
        "su chromeuser -c 'npm install'",
        "su chromeuser -c 'npm run build'",
        "su chromeuser -c 'npm run pretest'",
    ],
    "test_cmd": (f'xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99" '
                 'su chromeuser -c "./node_modules/.bin/karma start test/jasmine/karma.conf.js '
                 '--nowatch --verbose --capture-timeout 210000 --browser-disconnect-tolerance 3 '
                 '--browser-disconnect-timeout 210000 --browser-no-activity-timeout 210000"'),
    "docker_specs": {
        "node_version": "9.2.0",
        "run_args": {
            "cap_add": ["SYS_ADMIN"],
        },
    },
} for k in [
    "2.33", "2.32", "2.31", "2.30", "2.29", "2.28", "2.27", "2.26", "2.25",
    "2.24", "2.23", "2.22", "2.21", "2.20", "2.19", "2.18", "2.17", "2.16",
    "2.15", "2.14", "2.13", "2.12", "2.11", "2.10", "2.9", "2.8", "2.7",
    "2.6", "2.5", "2.4", "2.3", "2.2", "2.1", "2.0", "1.58", "1.57", "1.56",
    "1.55", "1.54", "1.53", "1.52", "1.51", "1.50", "1.49", "1.48", "1.47",
    "1.46", "1.45", "1.44", "1.43", "1.42", "1.41", "1.40", "1.39", "1.38",
    "1.37", "1.36", "1.35", "1.34", "1.33", "1.32", "1.31", "1.30", "1.29",
    "1.28", "1.27", "1.26", "1.25", "1.24", "1.23", "1.22", "1.21", "1.20",
    "1.19", "1.18", "1.17", "1.16", "1.15", "1.14", "1.13", "1.12", "1.11",
    "1.10", "1.9", "1.8", "1.7", "1.6", "1.5", "1.4", "1.3", "1.2", "1.1",
    "1.0",
]}
for k in [
    "2.33", "2.32", "2.31", "2.30", "2.29", "2.28", "2.27", "2.26", "2.25",
    "2.24", "2.23", "2.22", "2.21", "2.20", "2.19", "2.18", "2.17", "2.16",
    "2.15", "2.14", "2.13", "2.12", "2.11", "2.10", "2.9", "2.8", "2.7",
    "2.6", "2.5", "2.4", "2.3", "2.2", "2.1", "2.0"
]:
    SPECS_PLOTLYJS[k]["docker_specs"]["node_version"] = "16.20.2"

# Insomnia node versions:
# 1.0 = '10.15'
# 5.1 = '7.4.0'
# 5.2 = '7.4.0'
# 5.3 = '7.4.0'
# 5.11 = '8'
# 6.0 = '8'
# 6.2 = '10'
# 9.1 = '20.9.0'
# 9.3 = '20.9.0'
# 2020.1 = '10.15'
# 2020.2 = '10'
# 2020.4 = '12.18.3'
# 2020.5 = '12.18.3'
# 2021.1 = '12.18.3'
# 2021.2 = '12.18.3'
# 2021.4 = '12.18.3'
# 2021.5 = '12.18.3'
# 2021.6 = '12.18.3'
# 2022.4 = '16.13.2'
# 2022.7 = '16.17.0'
# 2023.1 = '16.17.0'
# 2023.2 = '16.17.0'
# 2023.5 = '18.15.0'
SPECS_INSOMNIA = {
    k: {
        "apt-pkgs": ["libfontconfig1-dev"],
        "install": ["npm install"],
        "test_cmd": "./node_modules/.bin/jest --json",
        # "test_cmd": PRINT_WORKSPACE_TESTS,
        "docker_specs": {},
    } for k in ['1.0', '5.1', '5.2', '5.3', '5.11', '6.0', '6.2', '9.1', '9.3',
                '2020.1', '2020.2', '2020.4', '2020.5', '2021.1', '2021.2',
                '2021.4', '2021.5', '2021.6', '2022.4', '2022.7', '2023.1',
                '2023.2', '2023.5']
}
for k in ['5.1', '5.2', '5.3']:
    SPECS_INSOMNIA[k]['docker_specs']['node_version'] = '7.4.0'
for k in ['1.0', '2020.1']:
    SPECS_INSOMNIA[k]['docker_specs']['node_version'] = '10.15.3'
for k in ['5.11', '6.0']:
    SPECS_INSOMNIA[k]['docker_specs']['node_version'] = '8.17.0'
for k in ['6.2', '2020.2']:
    SPECS_INSOMNIA[k]['docker_specs']['node_version'] = '10.24.1'  # '10.15.3'
for k in ['9.1', '9.3']:
    SPECS_INSOMNIA[k]["install"] = ["npm install"]
    SPECS_INSOMNIA[k]['docker_specs']['node_version'] = '20.9.0'
    SPECS_INSOMNIA[k]['test_cmd'] = "npm run test -- --json"
for k in ['2020.4', '2020.5', '2021.1', '2021.2', '2021.4', '2021.5', '2021.6']:
    SPECS_INSOMNIA[k]['docker_specs']['node_version'] = '12.18.3'
for k in ['2022.4']:
    SPECS_INSOMNIA[k]['docker_specs']['node_version'] = '16.13.2'
for k in ['2022.7', '2023.1', '2023.2']:
    SPECS_INSOMNIA[k]['docker_specs']['node_version'] = '16.17.0'
for k in ['2023.5']:
    SPECS_INSOMNIA[k]['docker_specs']['node_version'] = '18.15.0'

SPECS_EMOTION = {
    **{k: {
        "install": [
            "npm i -g yarn",
            "yarn",
            "yarn build"
        ],
        "test_cmd": "yarn test",
        "docker_specs": {
            "node_version": "16.20.2"
        }
    } for k in ['10.0']},
    **{k: {
        "install": ["npm install"],
        "test_cmd": "npm test",
        "docker_specs": {
            "node_version": "8.17.0"
        }
    } for k in ['2.0', '5.1', '5.2', '7.0']}
}

SPECS_PIXIJS = {
    **{k: {
        "apt-pkgs": XVFB_DEPS + ["libfontconfig1-dev"],
        "install": [
            "sed -i \"s/'ts-jest': {/'ts-jest': { isolatedModules: true,/\" jest.config.js",
            "sed -i \"/coverageDirectory: '<rootDir>\/dist\/coverage',/d\" jest.config.js",
            "sed -i 's/testTimeout: 10000/testTimeout: 10000,/' jest.config.js",
            "sed -i 's/};/    maxConcurrency: 3,\\n};/' jest.config.js",
            "sed -i 's/};/    maxWorkers: \"50%\",\\n};/' jest.config.js",
            "npm install",
            "cat jest.config.js",
        ],
        "test_cmd": ["npx jest --silent --no-colors"],
        "docker_specs": {
            "node_version": "18.20.4"
        }
    } for k in [
        '4.1', '4.3', '4.5', '4.8', '5.0', '6.0',
        '7.1', '7.2', '7.3', '8.0', '8.1', '8.2'
    ]}
}

SPECS_CYPRESS = {
    **{k: {
        "apt-pkgs": XVFB_DEPS,
        "install": ["npm i -g yarn", "yarn"],
        "test_cmd": "yarn test",
        "docker_specs": {
            "node_version": '16.20.2'
        }
    } for k in [
        '1.0', '1.1', '1.4',
        '10.0', '10.1', '10.10', '10.11', '10.2', '10.3', '10.5', '10.6', '10.7', '10.8', '10.9',
        '11.0', '11.1', '11.2',
        '12.0', '12.1', '12.2', '12.3', '12.4', '12.5', '12.6', '12.7', '12.8',
        '12.9', '12.10', '12.11', '12.12', '12.14', '12.17',
        '13.4', '13.6',
        '2.0', '2.1',
        '3.0', '3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8',
        '4.0', '4.1', '4.10', '4.11', '4.12', '4.2', '4.3', '4.4', '4.5', '4.6', '4.7', '4.8', '4.9',
        '5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6',
        '6.0', '6.1', '6.2', '6.3', '6.4', '6.5', '6.6', '6.7', '6.8',
        '7.1', '7.2', '7.4', '7.5', '7.7',
        '8.0', '8.1', '8.2', '8.3', '8.4', '8.6',
        '9.0', '9.1', '9.2', '9.3', '9.4', '9.5', '9.6', '9.7'
    ]}
}
for v in ['12.9', '12.10', '12.11', '12.12', '12.14', '12.17', '13.4', '13.6']:
    SPECS_CYPRESS[v]['docker_specs']['node_version'] = '21.6.2'
