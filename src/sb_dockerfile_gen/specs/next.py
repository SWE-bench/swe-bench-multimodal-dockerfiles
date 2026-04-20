"""alibaba-fusion/next spec."""

from sb_dockerfile_gen.common import (
    XVFB_DEPS,
    SET_PUPPETEER_PATH_OPT,
    SETUP_KARMA_JSON_REPORTER_NEXT,
    chromium_preinstall,
    CHROMIUM_71_A, CHROMIUM_85_A, CHROMIUM_88_A, CHROMIUM_93,
)
from sb_dockerfile_gen.utils import get_test_paths


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
    SPECS_NEXT[v]['install'].insert(0, SET_PUPPETEER_PATH_OPT.format("scripts/test/karma.js"))
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
# Per-version Chromium pins. Constants in common.py. v1.11–1.20 use a
# karma-chrome-launcher era rev (no puppeteer to derive from); v1.21–1.27
# follow each commit's puppeteer dep.
NEXT_PINS = {
    '1.11': CHROMIUM_71_A,
    '1.14': CHROMIUM_71_A,
    '1.15': CHROMIUM_71_A,
    '1.16': CHROMIUM_71_A,
    '1.17': CHROMIUM_71_A,
    '1.18': CHROMIUM_71_A,
    '1.19': CHROMIUM_71_A,
    '1.20': CHROMIUM_71_A,
    '1.21': CHROMIUM_85_A,
    '1.22': CHROMIUM_88_A,
    '1.23': CHROMIUM_88_A,
    '1.24': CHROMIUM_88_A,
    '1.25': CHROMIUM_93,
    '1.26': CHROMIUM_93,
    '1.27': CHROMIUM_93,
}
for _v, (_kind, _rev) in NEXT_PINS.items():
    SPECS_NEXT[_v]['pre_install'] = chromium_preinstall(_kind, _rev)
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


def _next_test_cmds(instance: dict) -> list:
    # Env vars must be inside the `su chromeuser -c` payload — su strips
    # parent env by default, so setting them outside leaks through to the
    # outer shell but not to npm/karma. CHROME_BIN for v1.11-1.21 karma-
    # chrome-launcher; PUPPETEER_EXECUTABLE_PATH for v1.22+ puppeteer path.
    ENV = "PUPPETEER_EXECUTABLE_PATH=/opt/chromium/chrome CHROME_BIN=/opt/chromium/chrome"
    XVFB = 'xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99"'
    return list(dict.fromkeys([
        f'timeout 5m bash -c \'{XVFB} '
        f'su chromeuser -c "{ENV} npm run test {test_path.split("/")[1]}"\''
        for test_path in get_test_paths(instance)
    ]))


for v in SPECS_NEXT:
    SPECS_NEXT[v]["test_cmd"] = _next_test_cmds
