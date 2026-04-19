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
