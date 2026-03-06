"""
Constants for the multimodal (JavaScript) dockerfile generator.

Dev split repos: calypso, chart.js, marked, p5.js, react-pdf
Test split repos: lighthouse, carbon, openlayers, highlight.js, alibaba-fusion/next,
                  bpmn-js, prism, quarto-cli, prettier, grommet, eslint, scratch-gui
"""

CONTAINER_WORKDIR = "/testbed"

REPO_BASE_COMMIT_BRANCH: dict[str, dict[str, str]] = {}

START_TEST_OUTPUT = ">>>>> Start Test Output"
END_TEST_OUTPUT = ">>>>> End Test Output"

FAIL_ONLY_REPOS = {
    # Dev split
    "chartjs/Chart.js",
    "processing/p5.js",
    "markedjs/marked",
}

MAP_REPO_TO_PARSER_NAME = {
    # Dev split repos
    "Automattic/wp-calypso": "parse_log_calypso",
    "chartjs/Chart.js": "parse_log_chart_js",
    "markedjs/marked": "parse_log_marked",
    "processing/p5.js": "parse_log_p5js",
    "diegomura/react-pdf": "parse_log_react_pdf",
    # Test split repos
    "GoogleChrome/lighthouse": "parse_log_tap",
    "carbon-design-system/carbon": "parse_log_jest",
    "openlayers/openlayers": "parse_log_karma",
    "highlightjs/highlight.js": "parse_log_tap",
    "alibaba-fusion/next": "parse_log_karma",
    "bpmn-io/bpmn-js": "parse_log_karma",
    "PrismJS/prism": "parse_log_tap",
    "quarto-dev/quarto-cli": "parse_log_tap",
    "prettier/prettier": "parse_log_jest",
    "grommet/grommet": "parse_log_jest",
    "eslint/eslint": "parse_log_tap",
    "scratchfoundation/scratch-gui": "parse_log_jest",
}

# --- Common constants ---

TEST_XVFB_PREFIX = 'xvfb-run --server-args="-screen 0 1280x1024x24 -ac :99"'
XVFB_DEPS = [
    "python3",
    "python3-pip",
    "xvfb",
    "x11-xkb-utils",
    "xfonts-100dpi",
    "xfonts-75dpi",
    "xfonts-scalable",
    "xfonts-cyrillic",
    "x11-apps",
    "firefox",
]
X11_DEPS = [
    "libx11-xcb1",
    "libxcomposite1",
    "libxcursor1",
    "libxdamage1",
    "libxi6",
    "libxtst6",
    "libnss3",
    "libcups2",
    "libxss1",
    "libxrandr2",
    "libasound2",
    "libatk1.0-0",
    "libgtk-3-0",
    "x11-utils",
]

# ============================================================
# Dev split repos (versioned specs)
# ============================================================

SPECS_CALYPSO = {
    **{
        k: {
            "apt-pkgs": ["libsass-dev", "sassc"],
            "install": ["npm install --unsafe-perm"],
            "test_cmd": "npm run test-client",
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
            "10.14.0",
            "10.15.2",
            "10.16.3",
        ]
    }
}

TEST_CHART_JS_TEMPLATE = "./node_modules/.bin/cross-env NODE_ENV=test ./node_modules/.bin/karma start {} --single-run --coverage --grep --auto-watch false"
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

SPECS_MARKED = {
    **{
        k: {
            "install": ["npm install"],
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

SPECS_P5_JS = {
    **{
        k: {
            "apt-pkgs": X11_DEPS,
            "install": [
                "npm install",
                "PUPPETEER_SKIP_CHROMIUM_DOWNLOAD='' node node_modules/puppeteer/install.js",
                "./node_modules/.bin/grunt yui",
            ],
            "test_cmd": (
                """sed -i 's/concurrency:[[:space:]]*[0-9][0-9]*/concurrency: 1/g' Gruntfile.js\n"""
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
for k in ["0.4", "0.5", "0.6"]:
    SPECS_P5_JS[k]["install"] = [
        "npm install",
        "./node_modules/.bin/grunt yui",
    ]

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
            "install": ["npm i -g yarn", "yarn install"],
            "test_cmd": 'NODE_OPTIONS="--experimental-vm-modules" ./node_modules/.bin/jest --no-color',
            "docker_specs": {"node_version": "18.20.4"},
        }
        for k in ["1.0", "1.1", "1.2", "2.0"]
    }
}
for v in ["1.0", "1.1", "1.2"]:
    SPECS_REACT_PDF[v]["docker_specs"]["node_version"] = "8.17.0"
    SPECS_REACT_PDF[v]["install"] = ["npm install", "npm install cheerio@1.0.0-rc.3"]
    SPECS_REACT_PDF[v]["test_cmd"] = "./node_modules/.bin/jest --no-color"

# ============================================================
# Test split repos (all keyed by "" since version is empty)
# ============================================================

# --- Jest-based repos (no browser deps) ---

SPECS_GROMMET = {
    "": {
        "install": ["npm i -g yarn", "yarn install"],
        "test_cmd": ["npx jest --runInBand --no-color --verbose"],
        "docker_specs": {"node_version": "18"},
    },
}

SPECS_PRETTIER = {
    "": {
        "install": ["npm i -g yarn", "yarn install"],
        "test_cmd": ["npx jest --no-color --verbose"],
        "docker_specs": {"node_version": "18"},
    },
}

SPECS_SCRATCH_GUI = {
    "": {
        "install": ["npm install", "npm install cheerio@1.0.0-rc.12"],
        "test_cmd": ["npx jest test/unit --no-color --verbose"],
        "docker_specs": {"node_version": "16"},
    },
}

SPECS_CARBON = {
    "": {
        "install": [
            "npm i -g yarn cross-env",
            "yarn install --network-timeout 300000",
        ],
        "test_cmd": ["cross-env BABEL_ENV=test npx jest --no-color --verbose"],
        "docker_specs": {"node_version": "18"},
    },
}

# --- Mocha-based repos (output forced to TAP for parsing) ---

SPECS_LIGHTHOUSE = {
    "": {
        "install": ["npm i -g yarn", "yarn install --frozen-lockfile || yarn install"],
        "test_cmd": ["yarn unit"],
        "docker_specs": {"node_version": "18"},
    },
}

SPECS_HIGHLIGHT_JS = {
    "": {
        "install": ["npm install"],
        "build": ["node ./tools/build.js -t node"],
        "test_cmd": ["npx mocha test --no-color -R tap"],
        "docker_specs": {"node_version": "18"},
    },
}

SPECS_PRISM = {
    "": {
        "install": ["npm install"],
        "test_cmd": ["npx mocha tests/run.js --no-color -R tap"],
        "docker_specs": {"node_version": "18"},
    },
}

SPECS_ESLINT = {
    "": {
        "install": ["npm install --legacy-peer-deps"],
        "test_cmd": ["npx mocha tests/lib/ --reporter tap --recursive"],
        "docker_specs": {"node_version": "18"},
    },
}

# --- Karma/browser-based repos (need Chrome + xvfb) ---

SPECS_OPENLAYERS = {
    "": {
        "apt-pkgs": XVFB_DEPS,
        "install": [
            "npm install",
            """sed -i '/process.env.CHROME_BIN/d' test/browser/karma.config.cjs""",
        ],
        "test_cmd": [
            f'NODE_OPTIONS=--openssl-legacy-provider {TEST_XVFB_PREFIX} su chromeuser -c "CHROME_BIN=/usr/bin/google-chrome npm run karma -- --single-run --log-level error"',
        ],
        "docker_specs": {
            "node_version": "18",
            "run_args": {"cap_add": ["SYS_ADMIN"]},
        },
    },
}

SPECS_BPMN_JS = {
    "": {
        "apt-pkgs": XVFB_DEPS,
        "install": ["npm install"],
        "test_cmd": [
            f'NODE_OPTIONS=--openssl-legacy-provider {TEST_XVFB_PREFIX} su chromeuser -c "npx karma start test/config/karma.unit.js --single-run"',
        ],
        "docker_specs": {
            "node_version": "18",
            "run_args": {"cap_add": ["SYS_ADMIN"]},
        },
    },
}

SPECS_ALIBABA_NEXT = {
    "": {
        "apt-pkgs": XVFB_DEPS + ["libsass-dev"],
        "install": ["npm install", "npm install cheerio@1.0.0-rc.3"],
        "test_cmd": [
            f'TRAVIS=true {TEST_XVFB_PREFIX} su chromeuser -c "node --max_old_space_size=8192 ./scripts/test/index.js"',
        ],
        "docker_specs": {
            "node_version": "8.17.0",
            "run_args": {"cap_add": ["SYS_ADMIN"]},
        },
    },
}

# --- Deno-based repos ---

SPECS_QUARTO = {
    "": {
        "apt-pkgs": ["unzip", "pipenv"],
        "install": [
            "bash configure.sh",
        ],
        "test_cmd": ["cd tests && QUARTO_TESTS_FORCE_NO_PIPENV=1 GITHUB_ACTION=1 bash run-tests.sh"],
        "docker_specs": {"node_version": "18"},
    },
}

# ============================================================
# Aggregate map
# ============================================================

MAP_REPO_VERSION_TO_SPECS_JS = {
    # Dev split
    "Automattic/wp-calypso": SPECS_CALYPSO,
    "chartjs/Chart.js": SPECS_CHART_JS,
    "markedjs/marked": SPECS_MARKED,
    "processing/p5.js": SPECS_P5_JS,
    "diegomura/react-pdf": SPECS_REACT_PDF,
    # Test split
    "GoogleChrome/lighthouse": SPECS_LIGHTHOUSE,
    "carbon-design-system/carbon": SPECS_CARBON,
    "openlayers/openlayers": SPECS_OPENLAYERS,
    "highlightjs/highlight.js": SPECS_HIGHLIGHT_JS,
    "alibaba-fusion/next": SPECS_ALIBABA_NEXT,
    "bpmn-io/bpmn-js": SPECS_BPMN_JS,
    "PrismJS/prism": SPECS_PRISM,
    "quarto-dev/quarto-cli": SPECS_QUARTO,
    "prettier/prettier": SPECS_PRETTIER,
    "grommet/grommet": SPECS_GROMMET,
    "eslint/eslint": SPECS_ESLINT,
    "scratchfoundation/scratch-gui": SPECS_SCRATCH_GUI,
}
