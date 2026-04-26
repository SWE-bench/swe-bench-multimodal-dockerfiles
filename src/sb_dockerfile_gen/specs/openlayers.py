"""OpenLayers spec."""

from sb_dockerfile_gen.common import (
    XVFB_DEPS,
    CHROMIUM_71_B, CHROMIUM_72_B, CHROMIUM_73, CHROMIUM_76_P5,
    CHROMIUM_79, CHROMIUM_81, CHROMIUM_83,
    CHROMIUM_85_B, CHROMIUM_87, CHROMIUM_88_B, CHROMIUM_90,
    CHROMIUM_92, CHROMIUM_93, CHROMIUM_97, CHROMIUM_98,
    CHROMIUM_100, CHROMIUM_101, CHROMIUM_104, CHROMIUM_106,
    CHROMIUM_107_A, CHROMIUM_109, CHROMIUM_110_A, CHROMIUM_111,
    CHROMIUM_112_B, CHROMIUM_CFT_113,
    CHROMIUM_CFT_115_A, CHROMIUM_CFT_115_B, CHROMIUM_CFT_115_C,
    CHROMIUM_CFT_116, CHROMIUM_CFT_117_B, CHROMIUM_CFT_118,
    CHROMIUM_CFT_119, CHROMIUM_CFT_121,
    CHROMIUM_CFT_122_A, CHROMIUM_CFT_122_B,
    CHROMIUM_CFT_123_A, CHROMIUM_CFT_123_B,
    CHROMIUM_CFT_124_A, CHROMIUM_CFT_124_B,
)
from sb_dockerfile_gen.utils import get_test_paths


SPECS_OPENLAYERS = {
    **{k: {
        "apt-pkgs": XVFB_DEPS,
        "install": ["npm install"],
        "test_cmd": "npm run test",
        "docker_specs": {
            "node_version": "21.6.2",
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
# WebGL software-rendering was tested against. PUPPETEER_SKIP_DOWNLOAD=true
# is set in the base; per-version pre-bake below writes Chromium variants
# into the cache layout puppeteer resolves at runtime.
#
# Each OL version's pin list covers every distinct Chromium observed across
# its instances — we pre-bake ALL of them so `puppeteer.executablePath()`
# finds a matching binary regardless of which puppeteer patch an individual
# instance pinned. Snapshot revs go under
# `node_modules/puppeteer/.local-chromium/linux-{rev}/chrome-linux/` (the path
# puppeteer 1.x-19.x hardcodes). CfT buildIds go under
# `/opt/puppeteer-cache/chrome/linux-{buildId}/chrome-linux64/` (puppeteer 20+
# with PUPPETEER_CACHE_DIR=/opt/puppeteer-cache from the base).
#
# `npm install --ignore-scripts` skips ALL postinstall hooks. For puppeteer
# 20+ this avoids install.mjs's parallel-download deadlock under BuildKit
# heredoc stdout buffering; for 1.x-19.x the install hook was already a
# silent no-op on Node 21 / Ubuntu 20.04 anyway.
OL_PINS = {
    '5.3':   [CHROMIUM_71_B, CHROMIUM_72_B, CHROMIUM_73, CHROMIUM_76_P5],
    '6.1':   [CHROMIUM_79],
    '6.2':   [CHROMIUM_81],
    '6.3':   [CHROMIUM_81, CHROMIUM_83, CHROMIUM_85_B],
    '6.4':   [CHROMIUM_87, CHROMIUM_88_B],
    '6.5':   [CHROMIUM_90],
    '6.5.1': [CHROMIUM_92],
    '6.6':   [CHROMIUM_93],
    '6.9':   [CHROMIUM_93, CHROMIUM_97],
    '6.10':  [CHROMIUM_97],
    '6.11':  [CHROMIUM_97],
    '6.12':  [CHROMIUM_97, CHROMIUM_98],
    '6.13':  [CHROMIUM_100],
    '6.14':  [CHROMIUM_100, CHROMIUM_101, CHROMIUM_104],
    '7.0':   [CHROMIUM_104, CHROMIUM_106],
    '7.1':   [CHROMIUM_106, CHROMIUM_107_A, CHROMIUM_109],
    '7.2':   [CHROMIUM_110_A],
    '7.3':   [CHROMIUM_111, CHROMIUM_112_B, CHROMIUM_CFT_113],
    '7.4':   [CHROMIUM_CFT_115_A],
    '7.5':   [CHROMIUM_CFT_115_B, CHROMIUM_CFT_115_C],
    '8.1':   [CHROMIUM_CFT_116, CHROMIUM_CFT_117_B, CHROMIUM_CFT_118],
    '9.0':   [CHROMIUM_CFT_119, CHROMIUM_CFT_121, CHROMIUM_CFT_122_A],
    '9.1':   [CHROMIUM_CFT_122_B, CHROMIUM_CFT_123_A, CHROMIUM_CFT_123_B,
              CHROMIUM_CFT_124_A, CHROMIUM_CFT_124_B],
}


def _ol_prebake_chromium(kind: str, rev_or_ver: str) -> str:
    """Pre-bake one Chromium variant into the path puppeteer expects at runtime.

    For 'rev' installs we keep the legacy path (older puppeteer uses it) AND
    symlink it into `$PUPPETEER_CACHE_DIR/chrome/linux-<rev>` so puppeteer ≥19.7
    (which moved to the cache layout) also resolves the binary. Fixes OL
    rendering tests on v7.1/7.2/7.3 instances that bundle puppeteer ≥19.4."""
    if kind == 'rev':
        url = f"https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/{rev_or_ver}/chrome-linux.zip"
        dest = f"node_modules/puppeteer/.local-chromium/linux-{rev_or_ver}"
        cache_alias = f"/opt/puppeteer-cache/chrome/linux-{rev_or_ver}"
        return (
            f"mkdir -p {dest} && "
            f"wget -q {url} -O /tmp/chrome.zip && "
            f"unzip -q /tmp/chrome.zip -d {dest}/ && "
            f"rm /tmp/chrome.zip && "
            f"chmod -R 755 {dest} && "
            f"mkdir -p $(dirname {cache_alias}) && "
            f"ln -sfn /testbed/{dest} {cache_alias}"
        )
    elif kind == 'cft':
        url = f"https://storage.googleapis.com/chrome-for-testing-public/{rev_or_ver}/linux64/chrome-linux64.zip"
        dest = f"/opt/puppeteer-cache/chrome/linux-{rev_or_ver}"
        return (
            f"mkdir -p {dest} && "
            f"wget -q {url} -O /tmp/chrome.zip && "
            f"unzip -q /tmp/chrome.zip -d {dest}/ && "
            f"rm /tmp/chrome.zip && "
            f"chmod -R 755 {dest}"
        )
    else:
        raise ValueError(f"_ol_prebake_chromium: unknown kind {kind!r}")


for _ol_v, _pins in OL_PINS.items():
    if _ol_v not in SPECS_OPENLAYERS:
        continue
    new_steps = []
    for step in SPECS_OPENLAYERS[_ol_v]['install']:
        if step == 'npm install':
            new_steps.append('npm install --ignore-scripts')
            for _kind, _rev in _pins:
                new_steps.append(_ol_prebake_chromium(_kind, _rev))
        else:
            new_steps.append(step)
    SPECS_OPENLAYERS[_ol_v]['install'] = new_steps


# Pre-6.5 karma configs don't read CHROME_BIN from puppeteer. Append the line
# if missing (grep guard keeps this idempotent for versions where it's already there).
_OL_KARMA_CHROME_BIN_FALLBACK = (
    "grep -q 'process.env.CHROME_BIN' test/karma.config.js || "
    "echo \"process.env.CHROME_BIN = require('puppeteer').executablePath();\" >> test/karma.config.js"
)
_OL_SNAPSHOT_VERSIONS = {v for v, pins in OL_PINS.items() if any(p[0] == 'rev' for p in pins)}
for _ol_v in _OL_SNAPSHOT_VERSIONS:
    if _ol_v in SPECS_OPENLAYERS:
        SPECS_OPENLAYERS[_ol_v]['install'].append(_OL_KARMA_CHROME_BIN_FALLBACK)


# v4.6 and v5.1 don't use puppeteer at all (karma-chrome-launcher relies on
# CHROME_BIN finding a system Chromium). Install Google Chrome via the deb
# repo and point CHROME_BIN at it. (Stays inside the OL-only image.)
_OL_NO_PUPPETEER_CHROME_INSTALL = [
    "wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -",
    "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list",
    "apt-get update && apt-get install -y google-chrome-stable && rm -rf /var/lib/apt/lists/*",
]
for _ol_v in {'4.6', '5.1'}:
    if _ol_v in SPECS_OPENLAYERS:
        SPECS_OPENLAYERS[_ol_v]['pre_install'] = _OL_NO_PUPPETEER_CHROME_INSTALL
        SPECS_OPENLAYERS[_ol_v].setdefault('docker_specs', {})['env'] = {
            'CHROME_BIN': '/usr/bin/google-chrome-stable',
        }
#
# Replacement for the original karma launcher:
#   `[process.env.CI ? 'ChromeHeadless' : 'Chrome']`  (v6.3, v6.5, v6.5.1, v6.6)
#   `['ChromeHeadless']`                              (v6.9+)
#   `['Chrome']`                                      (v6.1, v6.2)
# All become a custom ChromeNoSandbox launcher: ChromeHeadless + --no-sandbox.
# (The SUID sandbox helper isn't available in containers; on GHA VMs it was.)
_OL_NOSANDBOX_LAUNCHER_REPL = (
    "customLaunchers: { ChromeNoSandbox: { base: 'ChromeHeadless', flags: ['--no-sandbox', '--disable-dev-shm-usage'] } },"
    "\\n    browsers: ['ChromeNoSandbox']"
)
def _OL_NOSANDBOX_SED(cfg: str) -> str:
    """Two-pronged sed:
    1) For older configs that just use `browsers: [...]` without a customLauncher,
       inject our ChromeNoSandbox launcher.
    2) For v9.0+ which already define a customLauncher with `flags: ['--headless=new']`,
       append `--no-sandbox` and `--disable-dev-shm-usage` to its flags array.
    `--disable-dev-shm-usage` routes Chrome IPC away from /dev/shm (Docker
    default 64 MB) — required for v9.x rendering runs that previously needed
    `--shm-size=2g` at the harness level.
    Sed treats each `;`-separated expression independently — only the matching
    one fires per file."""
    return (
        "sed -i \""
        "s/browsers: \\[process.env.CI ? 'ChromeHeadless' : 'Chrome'\\]/" + _OL_NOSANDBOX_LAUNCHER_REPL + "/; "
        "s/browsers: \\['ChromeHeadless'\\]/" + _OL_NOSANDBOX_LAUNCHER_REPL + "/; "
        "s/browsers: \\['Chrome'\\]/" + _OL_NOSANDBOX_LAUNCHER_REPL + "/; "
        "s/flags: \\['--headless=new'\\]/flags: ['--headless=new', '--no-sandbox', '--disable-dev-shm-usage']/"
        "\" " + cfg
    )

# Render harness has a promise-leak: renderPage awaits `renderCalled` which
# only resolves when the test page calls `window.render(...)`. If the page's
# main.js throws before reaching `render()`, `handleRender` is never invoked
# and the await hangs indefinitely. Under nopatch, cases that depend on the
# fix's new API/operator (e.g. cog-style needs `layer.setStyle`, vector-id
# needs the 'id' text-expression operator) throw on load and hang the whole
# render loop. The eval script then times out at 1800s with no report.json.
#
# Fix (universal): race renderCalled against a 30s timeout AND reject it on
# page-level `pageerror` events. Wrap renderPage's call-site in renderEach
# with try/catch so one bad case logs a `mismatch 1 (render error: ...)`
# line (parser-recognized) and continues. Also install a process-level
# unhandledRejection handler so stray rejections don't kill Node v21+.
# Applied to all OL versions; v9.0/v9.1's renderEach replacement patches
# run AFTER this and replace their renderEach body, so the try/catch is
# only effective on pre-v9 vanilla renderEach — acceptable since the 3
# known hanging instances are all pre-v9.
_OL_RENDER_ERROR_GUARD = (
    "python3 - <<'PYEOF'\n"
    "import re\n"
    "f = 'test/rendering/test.js'\n"
    "s = open(f).read()\n"
    "old_render_page = '''async function renderPage(page, entry, options) {\\n"
    "  const renderCalled = new Promise((resolve) => {\\n"
    "    handleRender = (config) => {\\n"
    "      handleRender = null;\\n"
    "      resolve(config || {});\\n"
    "    };\\n"
    "  });\\n"
    "  options.log.debug(\\'navigating\\', entry);\\n"
    "  await page.goto(`http://${options.host}:${options.port}${getHref(entry)}`, {\\n"
    "    waitUntil: \\'networkidle0\\',\\n"
    "  });\\n"
    "  const config = await renderCalled;\\n"
    "  options.log.debug(\\'screenshot\\', entry);\\n"
    "  await page.screenshot({path: getActualScreenshotPath(entry)});\\n"
    "  return config;\\n"
    "}'''\n"
    "new_render_page = '''async function renderPage(page, entry, options) {\\n"
    "  let rejectRender;\\n"
    "  const renderCalled = new Promise((resolve, reject) => {\\n"
    "    rejectRender = reject;\\n"
    "    handleRender = (config) => {\\n"
    "      handleRender = null;\\n"
    "      resolve(config || {});\\n"
    "    };\\n"
    "  });\\n"
    "  renderCalled.catch(() => {});\\n"
    "  const pageErrHandler = (err) => {\\n"
    "    if (handleRender) { handleRender = null; rejectRender(err); }\\n"
    "  };\\n"
    "  page.on(\\'pageerror\\', pageErrHandler);\\n"
    "  const timer = setTimeout(() => {\\n"
    "    if (handleRender) { handleRender = null;\\n"
    "      rejectRender(new Error(\\'renderCalled timeout (30s) for \\' + entry)); }\\n"
    "  }, 30000);\\n"
    "  try {\\n"
    "    options.log.debug(\\'navigating\\', entry);\\n"
    "    await page.goto(`http://${options.host}:${options.port}${getHref(entry)}`, {\\n"
    "      waitUntil: \\'networkidle0\\', timeout: 30000,\\n"
    "    });\\n"
    "    const config = await renderCalled;\\n"
    "    options.log.debug(\\'screenshot\\', entry);\\n"
    "    await page.screenshot({path: getActualScreenshotPath(entry)});\\n"
    "    return config;\\n"
    "  } finally {\\n"
    "    clearTimeout(timer);\\n"
    "    page.off(\\'pageerror\\', pageErrHandler);\\n"
    "  }\\n"
    "}\\n\\n"
    "process.on(\\'unhandledRejection\\', (reason) => {\\n"
    "  console.error(\\'[renderPage] swallowed unhandled rejection:\\', reason && reason.message ? reason.message : reason);\\n"
    "});'''\n"
    "if old_render_page not in s: raise SystemExit('renderPage block not found; skipping guard')\n"
    "s = s.replace(old_render_page, new_render_page)\n"
    "\n"
    "# Wrap renderPage call in try/catch inside vanilla renderEach.\n"
    "old_re = '''async function renderEach(page, entries, options) {\\n"
    "  let fail = false;\\n"
    "  for (const entry of entries) {\\n"
    "    const {tolerance = 0.005, message = \\'\\'} = await renderPage(\\n"
    "      page,\\n"
    "      entry,\\n"
    "      options\\n"
    "    );'''\n"
    "new_re = '''async function renderEach(page, entries, options) {\\n"
    "  let fail = false;\\n"
    "  for (const entry of entries) {\\n"
    "    let tolerance = 0.005, message = \\'\\';\\n"
    "    try {\\n"
    "      const _cfg = await renderPage(page, entry, options);\\n"
    "      tolerance = _cfg.tolerance ?? 0.005;\\n"
    "      message = _cfg.message || \\'\\';\\n"
    "    } catch (err) {\\n"
    "      options.log.error(`case ${entry}\\\\x27: mismatch 1 (render error: ${err.message})`);\\n"
    "      fail = true; handleRender = null; continue;\\n"
    "    }\\n"
    "    {'''\n"
    "if old_re in s:\n"
    "  s = s.replace(old_re, new_re)\n"
    "  # Close extra block-scope brace before `return fail;`.\n"
    "  s = s.replace('    }\\n  }\\n  return fail;\\n}', '    }\\n    }\\n  }\\n  return fail;\\n}', 1)\n"
    "open(f, 'w').write(s)\n"
    "PYEOF"
)
# NOTE: not attached to `install` — applied at test_cmd time instead (see
# _openlayers_test_cmds prepending it before rendering invocations), so
# existing images don't need rebuilding.

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
# Install karma-json-reporter for structured JSON output. Writes to
# /testbed/karma-results.json (not stdout) — large karma runs emit 200–500KB
# single-line JSON which Docker's log pipe truncates at 64KB boundaries.
# Eval post-step pretty-prints the file into the log so the parser can read
# the full result across multiple lines.
# OL has two config patterns: test/karma.config.js (≤6.5) and test/browser/karma.config.cjs (≥6.5.1).
# Reporter lines vary: ['dots'], ['dots', 'coverage-istanbul'], ['progress'].
_OL_KARMA_JSON_SED_JS = (
    "sed -i \"s|reporters: \\['dots', 'coverage-istanbul'\\]|reporters: ['json'],\\n        jsonReporter: {{ outputFile: '/testbed/karma-results.json', stdout: false }}|\" {0} ; "
    "sed -i \"s|reporters: \\['dots'\\]|reporters: ['json'],\\n        jsonReporter: {{ outputFile: '/testbed/karma-results.json', stdout: false }}|\" {0} ; "
    "sed -i \"s|reporters: \\['progress'\\]|reporters: ['json'],\\n        jsonReporter: {{ outputFile: '/testbed/karma-results.json', stdout: false }}|\" {0}"
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


# Strict byte-level rendering comparison for instances whose F2P target is a
# new rendering case added by the test_patch but whose gold vs nopatch pixel
# delta falls within the runner's 0.5% tolerance — the tolerance check passes
# both ways and the test is non-discriminating without byte-exact comparison.
# Appended after the rendering command; emits a parser-recognised mismatch
# line when actual.png and expected.png differ. Viable because per-version
# Chromium pins make the rendering reproducible.
_OL_STRICT_CMP_CASES = {
    "openlayers__openlayers-12194": ["immediate-pixel-ratio"],
    "openlayers__openlayers-13981": ["text-style-offset"],
    "openlayers__openlayers-14932": ["text-style-linestring-nice"],
}


def _ol_strict_cmp_cmd(cases: list[str]) -> str:
    parts = []
    for case in cases:
        path = f"test/rendering/cases/{case}"
        parts.append(
            f"if [ -f {path}/actual.png ] && [ -f {path}/expected.png ] "
            f"&& ! cmp -s {path}/actual.png {path}/expected.png ; then "
            f"printf \"case ./cases/{case}/main.js': mismatch (strict byte comparison)\\n\" ; fi"
        )
    return " ; ".join(parts)


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
    ran_rendering = False
    for test_path in get_test_paths(instance):
        test_type = test_path.split('/')[1] if '/' in test_path else ""
        if test_type == "browser":
            cmds.append(f'{XVFB} su chromeuser -c "npm run test-browser"')
        elif test_type == "rendering":
            # CI=true activates puppeteer's --no-sandbox args (required in Docker).
            # --log-level=info emits "ok" lines for passing cases.
            # --force skips getOutdated() filter so ALL cases run.
            # Apply render-harness error guard before invocation — v9.0/v9.1
            # install-time patches overwrite renderEach; if both apply, the
            # v9.x patch runs later in eval_setup (install) and wins there.
            cmds.append(_OL_RENDER_ERROR_GUARD)
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
            ran_rendering = True
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
    strict_cases = _OL_STRICT_CMP_CASES.get(instance.get("instance_id", ""))
    if strict_cases and ran_rendering:
        cmds.append(_ol_strict_cmp_cmd(strict_cases))
    # Pretty-print karma-results.json into the log so parser sees full JSON.
    # karma-json-reporter writes single-line JSON (200-500KB for OL) which gets
    # cut at 64KB by Docker's log pipe; json.tool outputs multi-line.
    cmds.append(
        "python3 -m json.tool /testbed/karma-results.json 2>/dev/null || "
        "cat /testbed/karma-results.json 2>/dev/null || true"
    )
    # Dedupe while preserving insertion order — reproducible eval.sh across bakes.
    return list(dict.fromkeys(cmds))


for v in SPECS_OPENLAYERS:
    SPECS_OPENLAYERS[v]["test_cmd"] = _openlayers_test_cmds
