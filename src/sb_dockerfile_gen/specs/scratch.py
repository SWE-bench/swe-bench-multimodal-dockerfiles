"""Scratch GUI spec."""

from sb_dockerfile_gen.utils import get_test_paths


SPECS_SCRATCH = {
    **{k: {
        "install": ["npm install"],
        "test_cmd": "./node_modules/.bin/jest --runInBand --no-colors --json --forceExit --testPathIgnorePatterns='test/integration' --testPathIgnorePatterns='vm-manager-hoc'",
        "docker_specs": {
            "node_version": {
                "1": "20.16.0",
                "2": "20.16.0",
                "3": "12.22.12",
                "4": "12.22.12",
                "5": "20.16.0",
                "8": "20.16.0",
            }[k]
        }
    } for k in ['1', '2', '3', '4', '5', '8']}
}
for v in ['1', '2', '3', '4']:
    SPECS_SCRATCH[v]['install'].extend([
        "npm install cheerio@1.0.0-rc.3",
        "npm show cheerio"
    ])
# v8: AudioContext.resume() throws in web-audio-test-api mock because the default
# state is states[0] = "disabled". Swap array so "enabled" is default.
SPECS_SCRATCH['8']['install'].append(
    "sed -i 's/states: .\"disabled\", \"enabled\"./states: [\"enabled\", \"disabled\"]/' "
    "node_modules/web-audio-test-api/lib/utils/api.js"
)


_SPECS_SCRATCH_STATIC_TEST_CMD = {v: SPECS_SCRATCH[v]["test_cmd"] for v in SPECS_SCRATCH}


def _scratch_gui_test_cmds(instance: dict) -> list:
    test_prefix = _SPECS_SCRATCH_STATIC_TEST_CMD[instance["version"]]
    cmds = []
    for test_path in get_test_paths(instance):
        if "__snapshots__" in test_path:
            test_path = test_path.split("__snapshots__")[0]
        cmds.append(f"{test_prefix} {test_path}")
    return list(dict.fromkeys(cmds))


# scratch-gui: per-instance cmd is too narrow (misses F2P tests not in
# test_patch). Keep static test_cmd; callable defined for parity / future use.
