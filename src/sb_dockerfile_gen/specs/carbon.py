"""Carbon spec."""

import re

from sb_dockerfile_gen.utils import get_test_paths


def _jest_file_cmd(yarn_invocation: str, idx: int) -> str:
    """Wrap a jest/yarn-test invocation so the --json blob is written to a
    file instead of stdout, then cat'd back. This sidesteps a docker-log
    line-length truncation seen with >64KB single-line stdout writes (scratch-gui
    large jest JSON got cut mid-test). cat of a pre-written file is safe (chart.js
    does the same with karma-results.json)."""
    out = f"/testbed/jest-{idx}.json"
    # Pretty-print across many lines (docker log-pipe 64KB chunk truncation
    # then only affects one short line, not the blob). Wrap in `{ set +x; …;
    # set -x; } 2>/dev/null` so the xtrace line for the NEXT command (e.g.
    # `>>>>> End Test Output`) can't interleave mid-JSON via docker's
    # stderr→stdout merge.
    return (
        f"{{ set +x; {yarn_invocation} --outputFile={out} > /dev/null 2>&1 || true; "
        f"(python3 -m json.tool {out} 2>/dev/null || cat {out} 2>/dev/null); "
        f"set -x; }} 2>/dev/null"
    )


SPECS_CARBON = {
    **{k: {
        "pre_install": ["npm i -g yarn"],
        "install": [
            "yarn install",
            "yarn build",
        ],
        "test_cmd": _jest_file_cmd("yarn test --json", 0),
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
            jest_inv = (
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
            standalone_cmds.append(_jest_file_cmd(jest_inv, f"s{len(standalone_cmds)}"))
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

    yarn_cmds = [
        _jest_file_cmd(f"yarn test --json{max_workers} {p}", i)
        for i, p in enumerate(kept)
    ]
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


for v in SPECS_CARBON:
    SPECS_CARBON[v]["test_cmd"] = _carbon_test_cmds
    SPECS_CARBON[v]["eval_setup"] = _carbon_eval_setup
