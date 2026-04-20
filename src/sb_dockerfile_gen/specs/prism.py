"""Prism spec."""

from sb_dockerfile_gen.utils import get_test_paths


TEST_CMD_PRISM = "./node_modules/.bin/mocha tests/run.js --reporter json"
SPECS_PRISM = {
    **{k: {
        "install": ["npm ci", "npm run build"],
        "test_cmd": TEST_CMD_PRISM,
        "docker_specs": {
            "node_version": "12.22.12",
        }
    } for k in ['1.24', '1.25', '1.27', '1.28']},
    **{k: {
        "install": ["npm install", "npm run build"],
        "test_cmd": TEST_CMD_PRISM,
        "docker_specs": {
            "node_version": "10.24.1",
        }
    } for k in ['1.22', '1.23']},
    **{k: {
        "install": ["npm install"],
        "test_cmd": TEST_CMD_PRISM,
        "docker_specs": {
            "node_version": "8.17.0",
        }
    } for k in ['1.15', '1.16', '1.17', '1.19', '1.20']}
}
SPECS_PRISM['1.15']['docker_specs']['node_version'] = '4.9.1'
SPECS_PRISM['1.16']['docker_specs']['node_version'] = '21.6.2'
SPECS_PRISM['1.17']['docker_specs']['node_version'] = '21.6.2'


_SPECS_PRISM_STATIC_TEST_CMD = {v: SPECS_PRISM[v]["test_cmd"] for v in SPECS_PRISM}


def _prism_test_cmds(instance: dict) -> list:
    test_cmd = _SPECS_PRISM_STATIC_TEST_CMD[instance["version"]]
    directives = []
    for test_path in get_test_paths(instance):
        if test_path.startswith("tests/languages"):
            directives.append(test_cmd + f" --language {test_path.split('/')[2]}")
        elif test_path == "tests/core/greedy.js":
            directives.append("./node_modules/.bin/mocha tests/core/**/*.js --reporter json")
        elif test_path == "test.html":
            continue
    return sorted(list(set(directives)))


for v in SPECS_PRISM:
    SPECS_PRISM[v]["test_cmd"] = _prism_test_cmds
