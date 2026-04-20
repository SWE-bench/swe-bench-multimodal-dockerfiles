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

# Legacy install-command-list helpers kept for chart.js only (sets up
# /usr/bin/google-chrome wrapper at a specific Chromium rev). Everyone else
# uses the `CHROMIUM_*` constants + `chromium_preinstall` pattern below.
_CHROMIUM_85_INSTALL = _chromium_snapshot_install("793478")
_CHROMIUM_90_INSTALL = _chromium_snapshot_install("856583")   # Chrome 90


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
_CHROME_120_INSTALL = _chrome_for_testing_install("120.0.6099.109")


SET_OPENSSL_TO_LEGACY = "NODE_OPTIONS=--openssl-legacy-provider"
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
# chart.js uses a separate legacy table (no puppeteer dep to derive from).

CHROMIUM_60      = ('rev', '474900')    # target 474934 unavailable
CHROMIUM_61      = ('rev', '494755')
CHROMIUM_62      = ('rev', '499100')    # target 499098 unavailable
CHROMIUM_63      = ('rev', '508578')
CHROMIUM_63_DEC  = ('rev', '513000')    # late Chrome 63, target 515693 unavailable
CHROMIUM_64      = ('rev', '530400')    # target 530368 unavailable
CHROMIUM_66      = ('rev', '536395')    # puppeteer 1.1.1
CHROMIUM_68      = ('rev', '555668')    # puppeteer 1.4.0
CHROMIUM_71_A    = ('rev', '599821')    # puppeteer 1.10 / karma era
CHROMIUM_71_B    = ('rev', '609904')    # puppeteer 1.11
CHROMIUM_72_A    = ('rev', '624492')    # puppeteer 1.12.2
CHROMIUM_72_B    = ('rev', '637110')    # puppeteer 1.13
CHROMIUM_73      = ('rev', '641577')    # puppeteer 1.14.0
CHROMIUM_76_A    = ('rev', '669486')    # puppeteer 1.18.0
CHROMIUM_76_B    = ('rev', '672088')    # puppeteer 1.18.1
CHROMIUM_76_P5   = ('rev', '686378')    # puppeteer 2.0
CHROMIUM_77      = ('rev', '674921')    # puppeteer 1.19.0
CHROMIUM_79      = ('rev', '706915')    # puppeteer 2.1.1
CHROMIUM_81      = ('rev', '722234')    # puppeteer 2.1
CHROMIUM_83      = ('rev', '737027')    # puppeteer 3.x
CHROMIUM_85_A    = ('rev', '793478')
CHROMIUM_85_B    = ('rev', '756035')    # puppeteer 5.2
CHROMIUM_87      = ('rev', '782078')    # puppeteer 5.4
CHROMIUM_88_A    = ('rev', '818858')    # puppeteer 5.5.0
CHROMIUM_88_B    = ('rev', '800071')    # puppeteer 5.4.1
CHROMIUM_90      = ('rev', '856583')    # puppeteer 8.0.0
CHROMIUM_91      = ('rev', '869685')    # puppeteer 9.1.1
CHROMIUM_92      = ('rev', '884014')    # puppeteer 10.0.0
CHROMIUM_93      = ('rev', '901912')    # puppeteer 10.2.0
CHROMIUM_97      = ('rev', '938248')    # puppeteer 13.0
CHROMIUM_98      = ('rev', '950341')    # puppeteer 13.5
CHROMIUM_100     = ('rev', '970485')    # puppeteer 14.0
CHROMIUM_101     = ('rev', '982053')    # puppeteer 14.1
CHROMIUM_104     = ('rev', '1011831')   # puppeteer 16.x
CHROMIUM_106     = ('rev', '1022525')   # puppeteer 17.x
CHROMIUM_107_A   = ('rev', '1036745')   # puppeteer 18.0.5
CHROMIUM_107_B   = ('rev', '1045629')
CHROMIUM_109     = ('rev', '1056772')   # puppeteer 18.2
CHROMIUM_110_A   = ('rev', '1069273')   # puppeteer 19.4.1
CHROMIUM_110_B   = ('rev', '1083080')   # puppeteer 19.6.0
CHROMIUM_111     = ('rev', '1095492')   # puppeteer 19.7
CHROMIUM_112_A   = ('rev', '1110000')   # snapshot (CfT 112 unavailable)
CHROMIUM_112_B   = ('rev', '1108766')   # puppeteer 19.8
CHROMIUM_CFT_113   = ('cft', '113.0.5672.63')    # puppeteer 20.1.0
CHROMIUM_CFT_115_A = ('cft', '115.0.5790.98')    # puppeteer 20.8
CHROMIUM_CFT_115_B = ('cft', '115.0.5790.102')   # puppeteer 21.0
CHROMIUM_CFT_115_C = ('cft', '115.0.5790.170')   # puppeteer 21.1
CHROMIUM_CFT_116   = ('cft', '116.0.5845.96')    # puppeteer 21.2
CHROMIUM_CFT_117_A = ('cft', '117.0.5938.149')   # puppeteer 21.3.8
CHROMIUM_CFT_117_B = ('cft', '117.0.5938.92')    # puppeteer 21.3.4
CHROMIUM_CFT_118   = ('cft', '118.0.5993.70')    # puppeteer 21.4
CHROMIUM_CFT_119   = ('cft', '119.0.6045.105')   # puppeteer 21.7
CHROMIUM_CFT_121   = ('cft', '121.0.6167.85')    # puppeteer 21.9
CHROMIUM_CFT_122_A = ('cft', '122.0.6261.69')    # puppeteer 22.0
CHROMIUM_CFT_122_B = ('cft', '122.0.6261.128')   # puppeteer 22.1
CHROMIUM_CFT_123_A = ('cft', '123.0.6312.58')    # puppeteer 22.2
CHROMIUM_CFT_123_B = ('cft', '123.0.6312.122')   # puppeteer 22.3
CHROMIUM_CFT_124_A = ('cft', '124.0.6367.78')    # puppeteer 22.4
CHROMIUM_CFT_124_B = ('cft', '124.0.6367.91')    # puppeteer 22.5
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
