# Chromium pins for Multimodal repos

Reference table mapping each `(repo, version, base_commit)` in `SWE-bench_Multimodal`
to the Chromium revision its test suite expects, based on the `puppeteer` /
`playwright` / `karma-chrome-launcher` / `cypress` / `chromedriver` dep versions
declared in `package.json` at that commit.

Pins were derived by fetching `raw.githubusercontent.com/{repo}/{base_commit}/package.json`
and mapping each browser-driver version to its bundled Chromium:
- `puppeteer <20`: commit revision from `src/revisions.ts` (or `revisions.js` / `Launcher.js` for v1.x).
- `puppeteer >=20`: chrome-for-testing version from `packages/puppeteer-core/src/revisions.ts`.
- `playwright`: Chromium version from the Playwright GitHub release notes.
- `cypress`: Chromium from the bundled Electron runtime (Cypress 7.2 → Electron 12 → Chromium 89; Cypress 9.2 → Electron 15 → Chromium 94).
- `karma-chrome-launcher` without puppeteer: system Chrome — no deterministic pin; era-appropriate version noted.
- `chromedriver`: system Chrome matching the chromedriver major.

Install kinds referenced in the tables:
- `rev` — chromium-snapshots bucket, e.g. `https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/{rev}/chrome-linux.zip`
- `cft` — chrome-for-testing, e.g. `https://storage.googleapis.com/chrome-for-testing-public/{ver}/linux64/chrome-linux64.zip`
- `system` — any recent Chrome on PATH (no deterministic pin available from deps)
- `bundled-electron` — cypress ships its own Chromium inside Electron; no separate install needed
- `none` — test suite does not launch a real browser (pure Node / jsdom)

All puppeteer-based pins below are wired into the generator: per-repo
`*_PINS` dicts in `src/sb_dockerfile_gen/specs/<repo>.py` map each version
to a named `CHROMIUM_*` constant in `common.py`, and `chromium_preinstall()`
pre-bakes the binary at `/opt/chromium/chrome` (with a `--no-sandbox`
wrapper that also spoofs `--version` as "Google Chrome" for Cypress).
OpenLayers uses a per-instance multi-pin pre-bake (`OL_PINS` +
`_ol_prebake_chromium` in `specs/openlayers.py`) since one OL version may
span multiple puppeteer patches.

---

## Automattic/wp-calypso

All 9 sampled commits are pure Jest (jsdom). The `test/e2e/` subproject uses its
own lockfile and is not invoked by root `npm test`, so evaluation needs no
browser binary.

| instance_id | version | base_commit | browser_dep | dep_version | kind | pin | chrome |
|---|---|---|---|---|---|---|---|
| Automattic__wp-calypso-21977 | 8.9.3 | 6c46667 | none | – | none | – | – |
| Automattic__wp-calypso-23017 | 8.9.4 | 2a551f4 | none | – | none | – | – |
| Automattic__wp-calypso-23915 | 8.11.0 | 24d762a | none | – | none | – | – |
| Automattic__wp-calypso-25160 | 8.11.2 | bcc8e2e | none | – | none | – | – |
| Automattic__wp-calypso-25725 | 10.5.0 | af9cf1f | none | – | none | – | – |
| Automattic__wp-calypso-26335 | 10.6.0 | 1afcc6a | none | – | none | – | – |
| Automattic__wp-calypso-26816 | 10.9.0 | 5bb7ee7 | none | – | none | – | – |
| Automattic__wp-calypso-29804 | 10.14.0 | 73ff0f9 | none | – | none | – | – |
| Automattic__wp-calypso-33948 | 10.15.2 | d1c128c | none | – | none | – | – |

---

## GoogleChrome/lighthouse

`chrome-launcher` drives the SYSTEM chrome in smokehouse; any recent Chrome
works. `puppeteer` was added in 2.9 for viewer/extension pptr tests and pins a
bundled Chromium revision — that's the `pin` column below.

| instance_id | version | base_commit | browser_dep | dep_version | kind | pin | chrome |
|---|---|---|---|---|---|---|---|
| GoogleChrome__lighthouse-1617 | 1.4 | 4a63f3c | none in pkg | – | system | – | any |
| GoogleChrome__lighthouse-1755 | 1.5 | 4e140a9 | none in pkg | – | system | – | any |
| GoogleChrome__lighthouse-1941 | 1.6 | 9dd433c | none in pkg | – | system | – | any |
| GoogleChrome__lighthouse-2610 | 2.1 | 5c8d4ec | chrome-launcher | 0.8.0 | system | – | any |
| GoogleChrome__lighthouse-3442 | 2.4 | 4b8d8a1 | chrome-launcher | 0.8.1 | system | – | any |
| GoogleChrome__lighthouse-3692 | 2.5 | efe0e48 | chrome-launcher | 0.8.1 | system | – | any |
| GoogleChrome__lighthouse-4036 | 2.6 | f49ef06 | chrome-launcher | 0.8.1 | system | – | any |
| GoogleChrome__lighthouse-4301 | 2.8 | a52378e | chrome-launcher | 0.10.2 | system | – | any |
| GoogleChrome__lighthouse-5084 | 2.9 | 6159de6 | puppeteer | 1.1.1 | rev | 536395 | 66 |
| GoogleChrome__lighthouse-5688 | 3.0 | 8cee113 | puppeteer | 1.4.0 | rev | 555668 | 68 |
| GoogleChrome__lighthouse-5925 | 3.1 | 265d956 | puppeteer | 1.4.0 | rev | 555668 | 68 |
| GoogleChrome__lighthouse-6694 | 4.0 | 9f58eb4 | puppeteer | 1.10.0 | rev | 599821 | 71 |
| GoogleChrome__lighthouse-7356 | 4.1 | 5865c87 | puppeteer | 1.10.0 | rev | 599821 | 71 |
| GoogleChrome__lighthouse-8940 | 5.0 | ffb1deb | puppeteer | 1.10.0 | rev | 599821 | 71 |
| GoogleChrome__lighthouse-9334 | 5.1 | b751de5 | puppeteer | 1.10.0 | rev | 599821 | 71 |
| GoogleChrome__lighthouse-9451 | 5.2 | 5eb01d6 | puppeteer | 1.10.0 | rev | 599821 | 71 |
| GoogleChrome__lighthouse-10295 | 5.6 | 7ffb922 | puppeteer | 1.19.0 | rev | 674921 | 77 |
| GoogleChrome__lighthouse-10505 | 6.0 | 1457b4c | puppeteer | 1.19.0 | rev | 674921 | 77 |
| GoogleChrome__lighthouse-11068 | 6.1 | 6c4bfee | puppeteer | 1.19.0 | rev | 674921 | 77 |
| GoogleChrome__lighthouse-11489 | 6.4 | 252c329 | puppeteer | 1.19.0 | rev | 674921 | 77 |
| GoogleChrome__lighthouse-11738 | 6.5 | 61fbca3 | puppeteer | 1.19.0 | rev | 674921 | 77 |
| GoogleChrome__lighthouse-12067 | 7.0 | b439bf2 | puppeteer | 1.19.0 | rev | 674921 | 77 |
| GoogleChrome__lighthouse-12970 | 8.3 | 47c2bc5 | puppeteer | 9.1.1 | rev | 869685 | 91 |
| GoogleChrome__lighthouse-13185 | 8.6 | 50ca924 | puppeteer | 10.2.0 | rev | 901912 | 93 |
| GoogleChrome__lighthouse-14672 | 9.5 | 3055496 | puppeteer | 18.0.5 | rev | 1036745 | 107 |
| GoogleChrome__lighthouse-14800 | 10.0 | 8357117 | puppeteer | 19.6.0 | rev | 1083080 | 110 |
| GoogleChrome__lighthouse-15054 | 10.2 | 3ba11a8 | puppeteer | 20.1.0 | cft | 113.0.5672.63 | 113 |

---

## PrismJS/prism

All 11 sampled commits (1.15 → 1.28) are pure Mocha Node tests. No browser dep.

| instance_id | version | base_commit | browser_dep | kind |
|---|---|---|---|---|
| PrismJS__prism-1585 | 1.15 | 1169562 | none | none |
| PrismJS__prism-1853 | 1.16 | 2f9c926 | none | none |
| PrismJS__prism-2029 | 1.17 | c6c62a6 | none | none |
| PrismJS__prism-2195 | 1.19 | 0bf73dc | none | none |
| PrismJS__prism-2348 | 1.20 | c932447 | none | none |
| PrismJS__prism-2649 | 1.22 | a5107d5 | none | none |
| PrismJS__prism-2703 | 1.23 | 01af04e | none | none |
| PrismJS__prism-3050 | 1.24 | 8df825e | none | none |
| PrismJS__prism-3174 | 1.25 | 79f250f | none | none |
| PrismJS__prism-3351 | 1.27 | 3bd8fdb | none | none |
| PrismJS__prism-3438 | 1.28 | 293dce4 | none | none |

---

## alibaba-fusion/next

karma-chrome-launcher throughout. Puppeteer added in 1.22 for visual/smoke
tests and supplies the bundled Chromium pin.

| instance_id | version | base_commit | browser_dep | dep_version | kind | pin | chrome |
|---|---|---|---|---|---|---|---|
| alibaba-fusion__next-101 | 1.11 | f658785 | karma-chrome-launcher | 2.2.0 | system | – | any |
| alibaba-fusion__next-717 | 1.14 | 02d786b | karma-chrome-launcher | 2.2.0 | system | – | any |
| alibaba-fusion__next-870 | 1.15 | e604b6a | karma-chrome-launcher | 2.2.0 | system | – | any |
| alibaba-fusion__next-877 | 1.16 | 599f7c1 | karma-chrome-launcher | 2.2.0 | system | – | any |
| alibaba-fusion__next-1067 | 1.17 | a631db4 | karma-chrome-launcher | 2.2.0 | system | – | any |
| alibaba-fusion__next-1500 | 1.19 | 2a59086 | karma-chrome-launcher | 2.2.0 | system | – | any |
| alibaba-fusion__next-1807 | 1.20 | 981599d | karma-chrome-launcher | 2.2.0 | system | – | any |
| alibaba-fusion__next-2355 | 1.21 | c345df1 | karma-chrome-launcher | 2.2.0 | system | – | any |
| alibaba-fusion__next-2860 | 1.22 | 8196c63 | puppeteer | 5.5.0 | rev | 818858 | 88 |
| alibaba-fusion__next-3218 | 1.23 | 47fd0fc | puppeteer | 5.5.0 | rev | 818858 | 88 |
| alibaba-fusion__next-3345 | 1.24 | adeb9f6 | puppeteer | 5.5.0 | rev | 818858 | 88 |
| alibaba-fusion__next-3947 | 1.25 | 9b40758 | puppeteer | 10.2.0 | rev | 901912 | 93 |
| alibaba-fusion__next-4182 | 1.26 | 72c9786 | puppeteer | 10.2.0 | rev | 901912 | 93 |
| alibaba-fusion__next-4859 | 1.27 | 56f9fa2 | puppeteer | 10.4.0 | rev | 901912 | 93 |

---

## bpmn-io/bpmn-js

All 20 rows pin a bundled Chromium via puppeteer.

| instance_id | version | base_commit | browser_dep | dep_version | kind | pin | chrome |
|---|---|---|---|---|---|---|---|
| bpmn-io__bpmn-js-1011 | 3.4 | 13f1e05 | puppeteer | 1.14.0 | rev | 641577 | 73 |
| bpmn-io__bpmn-js-1143 | 4.0 | f5d55fe | puppeteer | 1.18.0 | rev | 669486 | 76 |
| bpmn-io__bpmn-js-1192 | 5.0 | 0143595 | puppeteer | 1.18.1 | rev | 672088 | 76 |
| bpmn-io__bpmn-js-1236 | 5.1 | f8ef569 | puppeteer | 1.18.1 | rev | 672088 | 76 |
| bpmn-io__bpmn-js-1238 | 6.0 | 7ad31ae | puppeteer | 1.18.1 | rev | 672088 | 76 |
| bpmn-io__bpmn-js-1299 | 6.3 | 9c114de | puppeteer | 1.18.1 | rev | 672088 | 76 |
| bpmn-io__bpmn-js-1330 | 7.2 | a445144 | puppeteer | 1.18.1 | rev | 672088 | 76 |
| bpmn-io__bpmn-js-1348 | 7.3 | 36e4f61 | puppeteer | 1.18.1 | rev | 672088 | 76 |
| bpmn-io__bpmn-js-1382 | 7.4 | d252ba2 | puppeteer | 5.5.0 | rev | 818858 | 88 |
| bpmn-io__bpmn-js-1434 | 8.3 | c3e0d6d | puppeteer | 8.0.0 | rev | 856583 | 90 |
| bpmn-io__bpmn-js-1542 | 8.8 | 0f4d308 | puppeteer | 10.0.0 | rev | 884014 | 92 |
| bpmn-io__bpmn-js-1584 | 8.9 | 7baefd7 | puppeteer | 10.0.0 | rev | 884014 | 92 |
| bpmn-io__bpmn-js-1636 | 9.0 | 0a25fd6 | puppeteer | 10.0.0 | rev | 884014 | 92 |
| bpmn-io__bpmn-js-1659 | 9.1 | 9737708 | puppeteer | 10.0.0 | rev | 884014 | 92 |
| bpmn-io__bpmn-js-1677 | 9.2 | ee75929 | puppeteer | 10.0.0 | rev | 884014 | 92 |
| bpmn-io__bpmn-js-1719 | 9.3 | a02fe7b | puppeteer | 10.0.0 | rev | 884014 | 92 |
| bpmn-io__bpmn-js-1802 | 11.1 | 39dd936 | puppeteer | 19.4.1 | rev | 1069273 | 109 |
| bpmn-io__bpmn-js-1847 | 11.3 | 3c90e8e | puppeteer | 19.4.1 | rev | 1069273 | 109 |
| bpmn-io__bpmn-js-1928 | 13.2 | 948c0d7 | puppeteer | 20.0.0 | cft | 112.0.5615.121 | 112 |
| bpmn-io__bpmn-js-2024 | 15.2 | 460125a | puppeteer | 21.3.8 | cft | 117.0.5938.149 | 117 |

---

## carbon-design-system/carbon

Three eras: karma (v10–14) in `packages/components`, Cypress (v14.17–16.14) in
`packages/react`, Playwright (v16.15+) at repo root.

| instance_id | version | base_commit | browser_dep | dep_version | kind | pin | chrome |
|---|---|---|---|---|---|---|---|
| carbon-design-system__carbon-3928 | 10 | 4c06756 | karma-chrome-launcher | 2.2.0 | system | – | ~75–78 |
| carbon-design-system__carbon-6520 | 12 | 1574611 | karma-chrome-launcher | 2.2.0 | system | – | ~83–85 |
| carbon-design-system__carbon-8130 | 14 | e928b91 | karma-chrome-launcher | 2.2.0 | system | – | ~91–93 |
| carbon-design-system__carbon-8912 | 14.17 | cb6de30 | cypress | 7.2.0 | bundled-electron | Electron 12 | 89 |
| carbon-design-system__carbon-10599 | 16.13 | 4060572 | cypress | 9.2.0 | bundled-electron | Electron 15 | 94 |
| carbon-design-system__carbon-15197 | 16.14 | 3e1660d | cypress | 9.2.0 | bundled-electron | Electron 15 | 94 |
| carbon-design-system__carbon-11416 | 16.15 | b53e3e9 | @playwright/test | 1.21.1 | cft | 101.0.4951.26 | 101 |
| carbon-design-system__carbon-11613 | 16.16 | 68e55ec | @playwright/test | 1.21.1 | cft | 101.0.4951.26 | 101 |
| carbon-design-system__carbon-12151 | 16.17 | f2ce743 | @playwright/test | 1.21.1 | cft | 101.0.4951.26 | 101 |
| carbon-design-system__carbon-12398 | 16.18 | d5390eb | @playwright/test | 1.21.1 | cft | 101.0.4951.26 | 101 |
| carbon-design-system__carbon-13218 | 18.14 | 30b49b1 | @playwright/test | 1.28.0 | cft | 108.0.5359.29 | 108 |
| carbon-design-system__carbon-13317 | 18.15 | 33f683f | @playwright/test | 1.28.0 | cft | 108.0.5359.29 | 108 |
| carbon-design-system__carbon-13851 | 18.16 | 97b6ca3 | @playwright/test | 1.28.0 | cft | 108.0.5359.29 | 108 |
| carbon-design-system__carbon-14476 | 18.17 | d9a3ae9 | @playwright/test | 1.36.2 | cft | 115.0.5790.75 | 115 |
| carbon-design-system__carbon-16237 | 20.12 | 7ea3b30 | @playwright/test | 1.36.2 | cft | 115.0.5790.75 | 115 |
| carbon-design-system__carbon-16332 | 20.14 | 8dd1cf5 | @playwright/test | 1.36.2 | cft | 115.0.5790.75 | 115 |

---

## chartjs/Chart.js

All 10 rows (3.0 → 4.3) use `karma ^6.3.2 + karma-chrome-launcher ^3.1.0`
with the system Chrome. No puppeteer/playwright/cypress. Suggested pin
follows commit date.

| instance_id | version | base_commit | browser_dep | dep_version | kind | pin | chrome |
|---|---|---|---|---|---|---|---|
| chartjs__Chart.js-8867 | 3.0 | ba84cc5 | karma-chrome-launcher | 3.1.0 | system | – | ~89 |
| chartjs__Chart.js-9101 | 3.2 | 927f24a | karma-chrome-launcher | 3.1.0 | system | – | ~90 |
| chartjs__Chart.js-9199 | 3.3 | 599e23a | karma-chrome-launcher | 3.1.0 | system | – | ~91 |
| chartjs__Chart.js-9399 | 3.4 | 31be610 | karma-chrome-launcher | 3.1.0 | system | – | ~91 |
| chartjs__Chart.js-9678 | 3.5 | 8e68481 | karma-chrome-launcher | 3.1.0 | system | – | ~93 |
| chartjs__Chart.js-9871 | 3.6 | 6bc47d3 | karma-chrome-launcher | 3.1.0 | system | – | ~96 |
| chartjs__Chart.js-10157 | 3.7 | c80b145 | karma-chrome-launcher | 3.1.0 | system | – | ~97 |
| chartjs__Chart.js-10806 | 4.0 | c35d0c6 | karma-chrome-launcher | 3.1.0 | system | – | ~107 |
| chartjs__Chart.js-11116 | 4.2 | 23e8f7d | karma-chrome-launcher | 3.1.0 | system | – | ~110 |
| chartjs__Chart.js-11352 | 4.3 | 201ddff | karma-chrome-launcher | 3.1.0 | system | – | ~113 |

---

## diegomura/react-pdf

All 3 sampled commits are pure Jest (jsdom). No browser dep.

| instance_id | version | base_commit | browser_dep | kind |
|---|---|---|---|---|
| diegomura__react-pdf-433 | 1.1 | f508d4e | none | none |
| diegomura__react-pdf-471 | 1.2 | 23b89c2 | none | none |
| diegomura__react-pdf-1552 | 2.0 | 7acd39f | none | none |

---

## eslint/eslint

v3.16–4.9 use PhantomJS (no Chromium). v5.14–8.1 use puppeteer for a Karma
browser-bundle smoke test invoked from `Makefile.js`. v8.50 removed Karma
entirely (back to pure Node Mocha). Note: default `npm test` target runs
Mocha only in all eras; the browser smoke is a separate `Makefile.js karma`
target.

| instance_id | version | base_commit | browser_dep | dep_version | kind | pin | chrome |
|---|---|---|---|---|---|---|---|
| eslint__eslint-8120 | 3.16 | f3a6ced | none (PhantomJS) | – | none | – | – |
| eslint__eslint-8850 | 4.1 | 5c3ac8e | none (PhantomJS) | – | none | – | – |
| eslint__eslint-9348 | 4.7 | a7668c2 | none (PhantomJS) | – | none | – | – |
| eslint__eslint-9436 | 4.9 | ecac0fd | none (PhantomJS) | – | none | – | – |
| eslint__eslint-11407 | 5.14 | af9688b | puppeteer | 1.12.2 | rev | 624492 | 73 |
| eslint__eslint-12472 | 6.6 | 990065e | puppeteer | 1.18.0 | rev | 669486 | 77 |
| eslint__eslint-12652 | 6.7 | a230f84 | puppeteer | 1.18.0 | rev | 669486 | 77 |
| eslint__eslint-14033 | 7.18 | f6602d5 | puppeteer | 4.0.0 | rev | 756035 | 85 |
| eslint__eslint-14242 | 7.22 | 8984c91 | puppeteer | 7.1.0 | rev | 848005 | 90 |
| eslint__eslint-15243 | 8.1 | 796587a | puppeteer | 9.1.1 | rev | 869685 | 92 |
| eslint__eslint-17618 | 8.50 | 2665552 | none | – | none | – | – |

---

## grommet/grommet

All 9 sampled commits run Jest with jsdom. No browser dep.

| instance_id | version | base_commit | browser_dep | kind |
|---|---|---|---|---|
| grommet__grommet-2061 | 2.0 | 279b3ec | none | none |
| grommet__grommet-2695 | 2.3 | bcde5d6 | none | none |
| grommet__grommet-6307 | 2.25 | 95a5e83 | none | none |
| grommet__grommet-6350 | 2.26 | 7885dbb | none | none |
| grommet__grommet-6494 | 2.27 | 67795aa | none | none |
| grommet__grommet-6600 | 2.29 | aaf8a69 | none | none |
| grommet__grommet-6749 | 2.31 | f1ea50d | none | none |
| grommet__grommet-5243 | 2.33 | d69a75e | none | none |
| grommet__grommet-7025 | 2.34 | 766c675 | none | none |

---

## highlightjs/highlight.js

All 11 sampled commits run `mocha test` with jsdom (for the `test/browser`
suite). No real browser.

| instance_id | version | base_commit | browser_dep | kind |
|---|---|---|---|---|
| highlightjs__highlight.js-2704 | 10.2 | 5b87cc4 | jsdom (stubbed) | none |
| highlightjs__highlight.js-2811 | 10.3 | 259b7c9 | jsdom | none |
| highlightjs__highlight.js-2899 | 10.4 | 1166e68 | jsdom | none |
| highlightjs__highlight.js-2960 | 10.5 | a7947a6 | jsdom | none |
| highlightjs__highlight.js-2972 | 10.6 | b85f4ab | jsdom | none |
| highlightjs__highlight.js-3207 | 11.0 | 5d51ee4 | jsdom | none |
| highlightjs__highlight.js-3301 | 11.2 | 67525ee | jsdom | none |
| highlightjs__highlight.js-3438 | 11.3 | c0138d9 | jsdom | none |
| highlightjs__highlight.js-3457 | 11.4 | 777eb91 | jsdom | none |
| highlightjs__highlight.js-3516 | 11.5 | 4eb662d | jsdom | none |
| highlightjs__highlight.js-3644 | 11.6 | 71f5cb2 | jsdom | none |

---

## markedjs/marked

All 11 sampled commits use `jasmine --config=jasmine.json`. Pure Node.

| instance_id | version | base_commit | browser_dep | kind |
|---|---|---|---|---|
| markedjs__marked-1262 | 0.3 | 579f7bf | none | none |
| markedjs__marked-684 | 0.5 | 86214bb | none | none |
| markedjs__marked-1435 | 0.6 | ae9484d | none | none |
| markedjs__marked-1535 | 0.7 | 2df12a7 | none | none |
| markedjs__marked-1674 | 1.0 | 0cd8598 | none | none |
| markedjs__marked-1739 | 1.1 | a9384ee | none | none |
| markedjs__marked-1825 | 1.2 | da071c9 | none | none |
| markedjs__marked-1936 | 2.0 | 18207d1 | none | none |
| markedjs__marked-2483 | 4.0 | b01ae92 | none | none |
| markedjs__marked-2627 | 4.1 | 2c9728d | none | none |
| markedjs__marked-2811 | 5.0 | ffcca41 | none | none |

---

## openlayers/openlayers

Wired via `OL_PINS` in `src/sb_dockerfile_gen/specs/openlayers.py`. Each
version maps to a list of `CHROMIUM_*` constants pre-baked into the
puppeteer cache layout so any per-instance puppeteer patch resolves to a
matching binary at runtime. v4.6 and v5.1 (no puppeteer dep) install
`google-chrome-stable` via the deb repo and set `CHROME_BIN`.

| version | puppeteer | kind | pin | chrome |
|---|---|---|---|---|
| 4.6 | (none) | system | – | any |
| 5.1 | (none) | system | – | any |
| 5.3 | 1.13.0 | rev | 637110 | 73 |
| 6.1 | 2.0.0 | rev | 706915 | 79 |
| 6.2 | 2.1.0 | rev | 722234 | 81 |
| 6.3 | 2.1.1 | rev | 722234 | 81 |
| 6.4 | 5.3.1 | rev | 800071 | 88 |
| 6.5 | 8.0.0 | rev | 856583 | 90 |
| 6.5.1 | 10.0.0 | rev | 884014 | 92 |
| 6.6 | 10.2.0 | rev | 901912 | 93 |
| 6.9 | 12.0.0 | rev | 938248 | 97 |
| 6.10 | 13.0.1 | rev | 938248 | 97 |
| 6.11 | 13.0.1 | rev | 938248 | 97 |
| 6.12 | 13.0.1 | rev | 938248 | 97 |
| 6.13 | 13.0.1 | rev | 938248 | 97 |
| 6.14 | 13.0.1 | rev | 938248 | 97 |
| 7.0 | 15.5.0 | rev | 1022525 | 105 |
| 7.1 | 17.1.1 | rev | 1036745 | 107 |
| 7.2 | 19.4.1 | rev | 1069273 | 110 |
| 7.3 | 20.3.0 | cft | 113.0.5672.63 | 113 |
| 7.4 | 20.9.0 | cft | 115.0.5790.98 | 115 |
| 7.5 | 21.1.1 | cft | 116.0.5845.96 | 116 |
| 8.1 | 21.2.1 | cft | 116.0.5845.96 | 116 |
| 9.0 | 21.9.0 | cft | 121.0.6167.85 | 121 |
| 9.1 | 22.5.0 | cft | 122.0.6261.128 | 122 |

---

## prettier/prettier

All 8 sampled commits run `jest` in Node. No browser dep.

| instance_id | version | base_commit | browser_dep | kind |
|---|---|---|---|---|
| prettier__prettier-4202 | 1.11 | e03e4d6 | none | none |
| prettier__prettier-6319 | 2.1 | 1b56e90 | none | none |
| prettier__prettier-9514 | 2.2 | d6858d5 | none | none |
| prettier__prettier-9866 | 2.3 | 892a70e | none | none |
| prettier__prettier-12177 | 2.6 | 9106e7e | none | none |
| prettier__prettier-14262 | 2.9 | 37fb53a | none | none |
| prettier__prettier-14688 | 3.0 | fb948bb | none | none |
| prettier__prettier-16347 | 3.4 | b26f56b | none | none |

---

## processing/p5.js

Karma + puppeteer for browser tests at every sampled commit (except v0.6,
which predates the puppeteer dep and uses system Chrome via karma).

| instance_id | version | base_commit | browser_dep | dep_version | kind | pin | chrome |
|---|---|---|---|---|---|---|---|
| processing__p5.js-3068 | 0.6 | 5215106 | karma-chrome-launcher | 2.2.0 | system | – | ~66 |
| processing__p5.js-3680 | 0.7 | 9372b29 | puppeteer | 1.12.2 | rev | 624492 | 72 |
| processing__p5.js-3769 | 0.8 | f310e50 | puppeteer | 1.12.2 | rev | 624492 | 72 |
| processing__p5.js-4147 | 0.10 | c6d686e | puppeteer | 1.18.1 | rev | 672088 | 73 |
| processing__p5.js-4561 | 1.0 | 4364d60 | puppeteer | 1.20.0 | rev | 686378 | 76 |
| processing__p5.js-5305 | 1.3 | efd946e | puppeteer | 5.5.0 | rev | 818858 | 88 |
| processing__p5.js-5794 | 1.4 | aeda6d2 | puppeteer | 10.2.0 | rev | 901912 | 93 |
| processing__p5.js-5917 | 1.5 | ce831a8 | puppeteer | 18.2.1 | rev | 1045629 | 107 |
| processing__p5.js-6111 | 1.6 | 113b99e | puppeteer | 18.2.1 | rev | 1045629 | 107 |

---

## quarto-dev/quarto-cli

Deno project — no npm `package.json`. `src/dev_import_map.json` pins
`deno.land/x/puppeteer@9.0.2`; chromium is only launched at runtime by
`quarto render --to pdf/screenshot`, not by the Deno test suite.

| instance_id | version | base_commit | browser_dep | dep_version | kind | pin | chrome |
|---|---|---|---|---|---|---|---|
| quarto-dev__quarto-cli-5064 | (none) | 45f6955 | deno puppeteer | 9.0.2 | rev (runtime only) | 869685 | 90 |

---

## scratchfoundation/scratch-gui

Uses `chromedriver` + `selenium-webdriver` — drives the SYSTEM chrome matching
the chromedriver major (chromedriver 2.x is the legacy numbering for
Chrome 66–73; chromedriver 74+ matches Chrome major).

| instance_id | version | base_commit | browser_dep | dep_version | kind | chrome |
|---|---|---|---|---|---|---|
| scratchfoundation__scratch-gui-2778 | 2 | 63c189e | chromedriver | 2.40.0 | system | 66 |
| scratchfoundation__scratch-gui-3342 | 3 | a9f1e2e | chromedriver | 2.42.1 | system | 68 |
| scratchfoundation__scratch-gui-4568 | 4 | 1a2c3bd | chromedriver | 2.44.1 | system | 69 |
| scratchfoundation__scratch-gui-5039 | 5 | 5b1670f | chromedriver | 74.0.0 | system | 74 |
| scratchfoundation__scratch-gui-8492 | 8 | 0eb9ced | chromedriver | 103.0.0 | system | 103 |

---

## Consolidated status

| Repo | Total rows | Needs Chromium | Kind |
|---|---|---|---|
| Automattic/wp-calypso | 9 | 0 | — |
| GoogleChrome/lighthouse | 27 | 19 (bundled) + 8 (smokehouse system) | rev + system |
| PrismJS/prism | 11 | 0 | — |
| alibaba-fusion/next | 14 | 6 (bundled) + 8 (system) | rev + system |
| bpmn-io/bpmn-js | 20 | 20 | rev (18) + cft (2) |
| carbon-design-system/carbon | 16 | 16 | system (3) + bundled-electron (3) + cft (10) |
| chartjs/Chart.js | 10 | 10 | system |
| diegomura/react-pdf | 3 | 0 | — |
| eslint/eslint | 11 | 6 (smoke only) | rev |
| grommet/grommet | 9 | 0 | — |
| highlightjs/highlight.js | 11 | 0 | — |
| markedjs/marked | 11 | 0 | — |
| openlayers/openlayers | 25 | 23 | rev (13) + cft (10) — already applied |
| prettier/prettier | 8 | 0 | — |
| processing/p5.js | 9 | 9 | rev |
| quarto-dev/quarto-cli | 1 | 1 (runtime only) | rev |
| scratchfoundation/scratch-gui | 5 | 5 | system |
| **Total** | **200** | **128** (incl. 11 runtime-only / smoke-only) | |

## Status (post-cleanup)

All four buckets above are now resolved:

1. **No-chromium repos** — base image no longer installs `google-chrome-stable`;
   only repos that pre-bake a Chromium via `chromium_preinstall` ship one.
2. **Deterministic bundled Chromium** — bpmn-js, next 1.21+, lighthouse, p5.js,
   chart.js (era-approximations) are all wired via per-repo `*_PINS` dicts +
   `chromium_preinstall`. eslint/quarto-cli were not wired (their puppeteer
   usage is for build-time/runtime tooling, not the test suites).
3. **System-Chrome era-approximations** — chart.js + lighthouse 1.x–2.8 +
   next 1.11–1.20 all use `chromium-snapshots` revs picked from the commit
   date; no system Chrome dep remains.
4. **Cypress bundled Electron** — carbon 14.17–16.14 still rely on Cypress's
   bundled Electron; the wrapper at `/opt/chromium/chrome` spoofs `--version`
   as "Google Chrome" so `cypress run -b chrome` accepts the pinned binary
   for repos that need it (e.g. next 1.27).

