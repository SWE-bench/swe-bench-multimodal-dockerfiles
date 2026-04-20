"""
Shared helpers used across multiple repo SPECS modules.

Browser/Chrome installation, XVFB/X11 dependency lists, Karma/Puppeteer
patching snippets, and language-runtime installers (Julia, TinyTeX, R).
"""

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

# Chrome 146 has breaking changes for older tests (floating-point precision,
# disconnect timeouts, MessagePort errors, rendering differences).
# Use Chromium snapshots for era-appropriate versions.
# Snapshots are at: https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/{rev}/chrome-linux.zip
# Wrap the binary in a shell script that adds --no-sandbox (needed in Docker).
def _chromium_snapshot_install(revision: str) -> list[str]:
    """Install a specific Chromium snapshot revision, replacing system Chrome."""
    return [
        # libxtst6 is needed by old Chromium but not pulled by the APT Chrome package
        "apt-get update && apt-get install -y libxtst6 && rm -rf /var/lib/apt/lists/*",
        f"wget -q https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/{revision}/chrome-linux.zip",
        "unzip -q chrome-linux.zip -d /opt/",
        "rm chrome-linux.zip",
        # Replace symlinks with a wrapper script that adds --no-sandbox
        # (Chromium snapshots don't include the SUID sandbox helper)
        "rm -f /usr/bin/google-chrome /usr/bin/google-chrome-stable",
        'printf \'#!/bin/bash\\nexec /opt/chrome-linux/chrome --no-sandbox "$@"\\n\' > /usr/bin/google-chrome',
        "chmod +x /usr/bin/google-chrome",
        "cp /usr/bin/google-chrome /usr/bin/google-chrome-stable",
    ]

# Revision → approximate Chrome version mapping:
#   599821 → Chrome ~72 (Oct 2018) — for v1.11-v1.15
#   793478 → Chrome ~85 (Aug 2020) — for v1.21
# Chrome for Testing 120 — for v1.27 and openlayers v7.4
_CHROMIUM_72_INSTALL = _chromium_snapshot_install("599821")
_CHROMIUM_85_INSTALL = _chromium_snapshot_install("793478")
# Additional era-appropriate Chromium pins for chart.js visual/rendering tests.
_CHROMIUM_90_INSTALL = _chromium_snapshot_install("856583")   # Chrome 90
_CHROMIUM_97_INSTALL = _chromium_snapshot_install("938248")   # Chrome 97
_CHROMIUM_100_INSTALL = _chromium_snapshot_install("901912")  # Chrome 100
_CHROMIUM_107_INSTALL = _chromium_snapshot_install("1036745") # Chrome 107
_CHROMIUM_108_INSTALL = _chromium_snapshot_install("1025233") # Chrome 108


def _chrome_for_testing_install(version: str) -> list[str]:
    """Install a specific Chrome-for-Testing version, replacing system Chrome."""
    return [
        f"wget -q https://storage.googleapis.com/chrome-for-testing-public/{version}/linux64/chrome-linux64.zip",
        "unzip -q chrome-linux64.zip -d /opt/",
        "rm chrome-linux64.zip",
        "rm -f /usr/bin/google-chrome /usr/bin/google-chrome-stable",
        'printf \'#!/bin/bash\\nexec /opt/chrome-linux64/chrome --no-sandbox "$@"\\n\' > /usr/bin/google-chrome',
        "chmod +x /usr/bin/google-chrome",
        "cp /usr/bin/google-chrome /usr/bin/google-chrome-stable",
    ]


_CHROMIUM_110_INSTALL = _chromium_snapshot_install("1069273")  # Chrome 110
_CHROME_113_INSTALL = _chrome_for_testing_install("113.0.5672.63")
_CHROME_120_INSTALL = _chrome_for_testing_install("120.0.6099.109")


SET_OPENSSL_TO_LEGACY = "NODE_OPTIONS=--openssl-legacy-provider"
SET_PUPPETEER_ENV_VAR = "PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable"
SET_PUPPETEER_PATH = "sed -i \"s|process.env.CHROME_BIN = require('puppeteer').executablePath();|process.env.CHROME_BIN = '/usr/bin/google-chrome-stable';|\" {}"
# Retargets `CHROME_BIN` to the pre-baked /opt/chromium/chrome path (see
# chromium_preinstall). Used by p5.js / bpmn-js / next / lighthouse pins.
SET_PUPPETEER_PATH_OPT = "sed -i \"s|process.env.CHROME_BIN = require('puppeteer').executablePath();|process.env.CHROME_BIN = '/opt/chromium/chrome';|\" {}"


def chromium_preinstall(kind: str, rev_or_ver: str) -> list[str]:
    """Pre-bake Chromium at /opt/chromium/chrome for a repo's puppeteer pin.

    Mirrors `_ol_chromium_preinstall` in specs/test_split.py so non-OL repos
    share one install pattern. `kind` is 'rev' (chromium-snapshots bucket) or
    'cft' (chrome-for-testing). `/opt/chromium/chrome` is a shell wrapper
    that adds `--no-sandbox` (required to launch Chromium inside Docker
    without CAP_SYS_ADMIN). Callers set PUPPETEER_EXECUTABLE_PATH and/or
    CHROME_BIN to /opt/chromium/chrome in test_cmd and (where needed) use
    SET_PUPPETEER_PATH_OPT to rewrite karma configs."""
    if kind == "rev":
        url = f"https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/{rev_or_ver}/chrome-linux.zip"
        zip_subdir = "chrome-linux"
    elif kind == "cft":
        url = f"https://storage.googleapis.com/chrome-for-testing-public/{rev_or_ver}/linux64/chrome-linux64.zip"
        zip_subdir = "chrome-linux64"
    else:
        raise ValueError(f"chromium_preinstall: unknown kind {kind!r} (expected 'rev' or 'cft')")
    return [
        # libxtst6 needed by older Chromium snapshots; harmless for CfT.
        "apt-get update && apt-get install -y libxtst6 && rm -rf /var/lib/apt/lists/*",
        f"wget -q {url} -O /tmp/chromium.zip",
        "unzip -q /tmp/chromium.zip -d /opt/chromium-pinned/",
        "rm /tmp/chromium.zip",
        "mkdir -p /opt/chromium",
        f"ln -sf /opt/chromium-pinned/{zip_subdir}/chrome /opt/chromium/chrome-bin",
        'printf \'#!/bin/bash\\nexec /opt/chromium/chrome-bin --no-sandbox "$@"\\n\' > /opt/chromium/chrome',
        "chmod +x /opt/chromium/chrome",
        "chmod -R 755 /opt/chromium-pinned",
    ]


# ── Named Chromium pins (kind, rev_or_ver) ────────────────────────────
# Each constant is a distinct Chromium build used by one or more repos.
# Suffixes disambiguate multiple revs mapping to the same Chrome major
# (different puppeteer bundles). Per-repo pin tables live next to the
# SPECS dicts in specs/test_split.py and specs/dev_split.py.
#
# OL is NOT listed here — it reads the project's own puppeteer
# revisions.js at build time (per-instance puppeteer patch overrides).
# chart.js uses a separate legacy table (no puppeteer dep to derive from).

CHROMIUM_60      = ('rev', '474900')    # lighthouse v1.4 era-approx (target 474934 unavailable)
CHROMIUM_61      = ('rev', '494755')    # lighthouse v1.5
CHROMIUM_62      = ('rev', '499100')    # lighthouse v1.6/v2.1, p5.js v0.6 (target 499098 unavailable)
CHROMIUM_63      = ('rev', '508578')    # lighthouse v2.4
CHROMIUM_63_DEC  = ('rev', '513000')    # late Chrome 63 — lighthouse v2.5/v2.6 (target 515693 unavailable)
CHROMIUM_64      = ('rev', '530400')    # lighthouse v2.8 (target 530368 unavailable)
CHROMIUM_66      = ('rev', '536395')    # puppeteer 1.1.1 (lighthouse v2.9)
CHROMIUM_68      = ('rev', '555668')    # puppeteer 1.4.0 (lighthouse v3.0/v3.1)
CHROMIUM_71      = ('rev', '599821')    # puppeteer 1.10 / karma era (lighthouse v4–v5.2, next v1.11–v1.20)
CHROMIUM_72      = ('rev', '624492')    # puppeteer 1.12.2 (p5.js v0.7/v0.8)
CHROMIUM_73      = ('rev', '641577')    # puppeteer 1.14.0 (bpmn-js v3.4)
CHROMIUM_76_A    = ('rev', '669486')    # puppeteer 1.18.0 (bpmn-js v4.0)
CHROMIUM_76_B    = ('rev', '672088')    # puppeteer 1.18.1 (bpmn-js v5–v7.3, p5.js v0.10)
CHROMIUM_76_P5   = ('rev', '686378')    # p5.js v1.0 puppeteer
CHROMIUM_77      = ('rev', '674921')    # puppeteer 1.19.0 (lighthouse v5.6–v7.0)
CHROMIUM_85      = ('rev', '793478')    # next v1.21, bpmn-js v9.0
CHROMIUM_88      = ('rev', '818858')    # puppeteer 5.5.0 (bpmn-js v7.4, next v1.22–v1.24, p5.js v1.3)
CHROMIUM_90      = ('rev', '856583')    # puppeteer 8.0.0 (bpmn-js v8.3)
CHROMIUM_91      = ('rev', '869685')    # puppeteer 9.1.1 (lighthouse v8.3)
CHROMIUM_92      = ('rev', '884014')    # puppeteer 10.0.0 (bpmn-js v8.8–v9.3)
CHROMIUM_93      = ('rev', '901912')    # puppeteer 10.2.0 (next v1.25–v1.27, p5.js v1.4, lighthouse v8.6)
CHROMIUM_107_A   = ('rev', '1036745')   # puppeteer 18.0.5 (lighthouse v9.5)
CHROMIUM_107_B   = ('rev', '1045629')   # p5.js v1.5/v1.6
CHROMIUM_110_A   = ('rev', '1069273')   # puppeteer 19.4.1 (bpmn-js v11.x)
CHROMIUM_110_B   = ('rev', '1083080')   # puppeteer 19.6.0 (lighthouse v10.0)
CHROMIUM_112     = ('rev', '1110000')   # bpmn-js v13.2 snapshot (CfT 112 unavailable)
CHROMIUM_CFT_113 = ('cft', '113.0.5672.63')    # puppeteer 20.1.0 (lighthouse v10.2)
CHROMIUM_CFT_117 = ('cft', '117.0.5938.149')   # puppeteer 21.3.8 (bpmn-js v15.2)
# Switch Karma from 'spec' to 'json' reporter for structured test output.
# The config file has an explicit plugins array so we must register the plugin.
# The sed on 'karma-coverage' handles both with and without trailing comma (v1.11 vs v1.14+).
SETUP_KARMA_JSON_REPORTER_NEXT = "sed -i \"s/'karma-coverage'/'karma-coverage', 'karma-json-reporter'/\" {0} && " \
    "sed -i \"s/reporters: \\['spec', 'coverage'\\]/reporters: ['json'],\\n        jsonReporter: {{ stdout: true }}/\" {0}"
# bpmn-js variant: reporters line is `[ 'progress' ].concat(coverage ? 'coverage' : [])`.
# No explicit plugins array — karma-* auto-discovery loads the reporter.
SETUP_KARMA_JSON_REPORTER_BPMN = "sed -i \"s/reporters: \\[ 'progress' \\].concat(coverage ? 'coverage' : \\[\\])/reporters: ['json'],\\n        jsonReporter: {{ stdout: true }}/\" {0}"

INSTALL_JULIA = [
    "wget https://julialang-s3.julialang.org/bin/linux/x64/1.9/julia-1.9.3-linux-x86_64.tar.gz",
    "tar zxvf julia-1.9.3-linux-x86_64.tar.gz",
    "mv julia-1.9.3/ /opt/",
    "ln -s /opt/julia-1.9.3/bin/julia /usr/local/bin/julia",
]
# Install TinyTeX directly (older quarto versions lack 'quarto install tool tinytex').
# Uses the default TinyTeX-1 bundle (~125 packages), then adds packages needed by the
# test suite's PDF renders (tufte, koma-script, tcolorbox, etc.).
INSTALL_TINYTEX = [
    "wget -qO- 'https://yihui.org/tinytex/install-bin-unix.sh' | sh && "
    "ln -sf $HOME/.TinyTeX/bin/x86_64-linux/* /usr/local/bin/",
    # Install the full set of TeX packages needed by quarto's test suite PDF renders.
    # This list matches quarto's own TinyTeX installer output (~320 packages).
    "export PATH=$HOME/.TinyTeX/bin/x86_64-linux:$PATH && "
    "tlmgr install "
    "a4wide achemso adjustbox ae algorithmicx algorithms apacite appendix "
    "awesomebox babel-english babel-french bbm-macros beamer biblatex biber "
    "breakurl caption carlisle catoptions ccicons changepage charter chemgreek "
    "cite cleveref collectbox colorprofiles colortbl comment count1to courier "
    "crop csquotes currfile datetime dblfloatfix doclicense draftwatermark "
    "eepic endfloat endnotes enumitem environ epsf epstopdf-pkg eso-pic esvect "
    "etex-pkg eurosym everysel everyshi expex extsizes fancyhdr fancyvrb "
    "filemod float floatflt floatrow fmtcount fontawesome5 fontaxes fontspec "
    "footmisc forarray fp fpl framed gincltex grfext grffile hardwrap hyperxmp "
    "hyphen-english hyphen-french hyphenat ifmtarg jknapltx kastrup koma-script "
    "langsci lastpage latex-lab latexindent lettrine libertine lineno lipsum "
    "listings logreq ltxkeys ly1 lualatex-math makecell makecmds makeindex "
    "marginnote marvosym mathalpha mathpazo mathspec mathtools mdframed memoir "
    "metalogo mhchem microtype minifp mnras morefloats moreverb multirow "
    "multitoc mweights natbib ncntrsbk needspace newfloat newtx ntgclass "
    "oberdiek palatino paralist parskip pbox pdfcol pdflscape "
    "pdfmanagement-testphase pdfpages pdfsync pgf picinpar placeins polyglossia "
    "prelim2e preprint preview psfrag ragged2e realscripts revtex4-1 roboto "
    "rsfs sauerj sectsty selnolig seqsplit setspace sidecap sidenotes siunitx "
    "soul srcltx standalone stix stmaryrd sttools subfig subfigure svn-prov "
    "tabto-ltx tabu tcolorbox tex-gyre texcount textcase thmtools "
    "threeparttable threeparttablex thumbpdf tikzfill tipa titlesec totcount "
    "totpages translator trimspaces tufte-latex ucs ulem units upquote urlbst "
    "varwidth vmargin vruler wallpaper wrapfig xargs xifthen xltxtra xpatch "
    "xstring xwatermark xypic zapfchan",
]
# Install R packages needed by knitr engine for rendering .qmd documents with {r} blocks.
# cmake is required to compile the 'fs' R package (dependency of rmarkdown).
INSTALL_R_PACKAGES = [
    "R -e \"install.packages(c('rmarkdown', 'knitr', 'jsonlite'), "
    "repos='https://cloud.r-project.org', quiet=TRUE)\"",
]
