"""ESLint spec."""

TEST_CMD_ESLINT = './node_modules/.bin/mocha --forbid-only --reporter json -t 10000 --no-colors "tests/{bin,conf,lib,tools}/**/*.js"'
SPECS_ESLINT = {
    **{k: {
        "install": ["npm install"],
        "test_cmd": TEST_CMD_ESLINT,
        "docker_specs": {
            "node_version": "10.24.1",
        }
    } for k in [
        '0.20', '0.24', '0.3', '0.5', '1.0', '1.1',
        '1.10', '1.5', '1.7', '1.9', '2.0', '2.10',
        '2.12', '2.13', '2.5', '3.1', '3.11',
        '3.16', '3.5', '4.1', '4.7', '4.9', '5.14',
        '6.6', '6.7', '7.18', '7.22', '8.1', '8.50'
    ]},
}
for v in ['0.20', '0.24', '0.3', '0.5', '1.0', '1.1', '1.10', '1.5',
    '1.7', '1.9', '2.0', '2.10', '2.12', '2.13', '2.5', '3.1', '3.11']:
    SPECS_ESLINT[v]["docker_specs"]["node_version"] = "4.9.1"
for v in ['8.1', '8.50']:
    SPECS_ESLINT[v]["docker_specs"]["node_version"] = "21.6.2"
