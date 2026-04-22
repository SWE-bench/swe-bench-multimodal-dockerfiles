"""Lighthouse spec."""

from sb_dockerfile_gen.common import (
    chromium_preinstall,
    CHROMIUM_60, CHROMIUM_61, CHROMIUM_62, CHROMIUM_63, CHROMIUM_63_DEC,
    CHROMIUM_64, CHROMIUM_66, CHROMIUM_68,
    CHROMIUM_71_A, CHROMIUM_77, CHROMIUM_91, CHROMIUM_93,
    CHROMIUM_107_A, CHROMIUM_110_B, CHROMIUM_CFT_113,
)
from sb_dockerfile_gen.utils import get_test_paths


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
# Per-version Chromium pins. Constants in common.py. v1.x–v2.8 use
# era-approximations since there's no puppeteer dep to derive from.
LIGHTHOUSE_PINS = {
    '1.4': CHROMIUM_60,
    '1.5': CHROMIUM_61,
    '1.6': CHROMIUM_62,
    '2.1': CHROMIUM_62,
    '2.4': CHROMIUM_63,
    '2.5': CHROMIUM_63_DEC,
    '2.6': CHROMIUM_63_DEC,
    '2.8': CHROMIUM_64,
    '2.9': CHROMIUM_66,
    '3.0': CHROMIUM_68,
    '3.1': CHROMIUM_68,
    '4.0': CHROMIUM_71_A,
    '4.1': CHROMIUM_71_A,
    '5.0': CHROMIUM_71_A,
    '5.1': CHROMIUM_71_A,
    '5.2': CHROMIUM_71_A,
    '5.6': CHROMIUM_77,
    '6.0': CHROMIUM_77,
    '6.1': CHROMIUM_77,
    '6.4': CHROMIUM_77,
    '6.5': CHROMIUM_77,
    '7.0': CHROMIUM_77,
    '8.3': CHROMIUM_91,
    '8.6': CHROMIUM_93,
    '9.5': CHROMIUM_107_A,
    '10.0': CHROMIUM_110_B,
    '10.2': CHROMIUM_CFT_113,
}
for _v, (_kind, _rev) in LIGHTHOUSE_PINS.items():
    # Append chromium install so yarn install from earlier pre_install isn't lost.
    SPECS_LIGHTHOUSE[_v]['pre_install'] = (
        list(SPECS_LIGHTHOUSE[_v].get('pre_install') or []) + chromium_preinstall(_kind, _rev)
    )
# Eval setup: v1.x gold patches may add new modules that need linking.
# v9.5/10.0/10.2 images may be missing devDependencies (e.g. testdouble)
# if built without PUPPETEER_SKIP_DOWNLOAD=true.
for v in ['1.0', '1.1', '1.2', '1.4', '1.5', '1.6']:
    SPECS_LIGHTHOUSE[v]['eval_setup'] = ["npm run install-all 2>/dev/null || true"]
for v in ['9.5', '10.0', '10.2']:
    SPECS_LIGHTHOUSE[v]['eval_setup'] = ["yarn install --frozen-lockfile 2>&1 | tail -3 || true"]


def _lighthouse_test_cmds(instance: dict) -> list:
    # Point puppeteer + chrome-launcher at the pinned /opt/chromium/chrome.
    # PUPPETEER_EXECUTABLE_PATH handles viewer/extension puppeteer tests;
    # CHROME_PATH handles smokehouse via chrome-launcher (v1.x–2.8 era).
    ENV = "PUPPETEER_EXECUTABLE_PATH=/opt/chromium/chrome CHROME_PATH=/opt/chromium/chrome"
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
                cmds.append(f"{ENV} yarn unit-flow")
            elif parent_folder in SUBDIRS + [LH_PREFIX + x for x in SUBDIRS]:
                if parent_folder.startswith(LH_PREFIX):
                    parent_folder = parent_folder[len(LH_PREFIX):]
                cmds.append(f"{ENV} yarn unit-{parent_folder} {test_path}")
            else:
                cmds.append(f"{ENV} yarn mocha {test_path}")
        elif '3.0' <= str(instance.get("version", "")) <= '8.6':
            # Write JSON to file then cat — avoids docker-log truncation on
            # large single-line stdout writes. Wrap in `{ set +x; …; set -x;
            # } 2>/dev/null` so the xtrace line for the NEXT jest invocation
            # (ENV var assignments + yarn jest) can't interleave mid-JSON via
            # docker's stderr→stdout merge. See specs/carbon.py _jest_file_cmd.
            out = f"/testbed/jest-{len(cmds)}.json"
            cmds.append(
                f"{{ set +x; {ENV} yarn jest --no-colors --json --outputFile={out} {test_path} "
                f"> /dev/null 2>&1 || true; cat {out} 2>/dev/null; set -x; }} 2>/dev/null"
            )
        else:
            # Shell stdout redirect instead of `--reporter-options output=…`:
            # mocha 3.x (lighthouse <v3) doesn't honor that flag for the json
            # reporter, so we pipe mocha's stdout to the file directly. Wrap
            # in `{ set +x; …; set -x; } 2>/dev/null` so the xtrace line for
            # the next command (e.g. `>>>>> End Test Output`) can't interleave
            # mid-JSON via docker's stderr→stdout merge.
            out = f"/testbed/mocha-{len(cmds)}.json"
            cmds.append(
                f"{{ set +x; {ENV} ./node_modules/.bin/mocha --reporter json {test_path} "
                f"> {out} 2>/dev/null ; cat {out} 2>/dev/null; set -x; }} 2>/dev/null"
            )
    return list(dict.fromkeys(cmds))


for v in SPECS_LIGHTHOUSE:
    SPECS_LIGHTHOUSE[v]["test_cmd"] = _lighthouse_test_cmds
