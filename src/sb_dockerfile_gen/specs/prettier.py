"""Prettier spec."""

from sb_dockerfile_gen.utils import get_test_paths


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


def _prettier_test_cmds(instance: dict) -> list:
    cmds = []
    for i, test_path in enumerate(get_test_paths(instance)):
        if "__snapshots__" in test_path:
            test_path = test_path.split("__snapshots__")[0]
        if test_path.endswith(".md"):
            test_path = "/".join(test_path.split("/")[:-1])
        # Only jsfmt.spec.js and __tests__/*.js are actual specs — everything else
        # (fixture .js, .ts, .css, .snap, etc.) needs the directory instead
        if not test_path.endswith("jsfmt.spec.js") and not "/__tests__/" in test_path and not test_path.endswith("/"):
            test_path = "/".join(test_path.split("/")[:-1])
        # Write JSON to file then cat — avoids docker-log truncation on large
        # single-line stdout writes. See specs/carbon.py _jest_file_cmd.
        out = f"/testbed/jest-{i}.json"
        cmds.append(
            f"yarn test --json --outputFile={out} {test_path} > /dev/null 2>&1 || true; "
            f"cat {out} 2>/dev/null || true"
        )
    return list(dict.fromkeys(cmds))


for v in SPECS_PRETTIER:
    SPECS_PRETTIER[v]["test_cmd"] = _prettier_test_cmds
