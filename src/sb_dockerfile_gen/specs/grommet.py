"""Grommet spec."""

SPECS_GROMMET = {
    **{k: {
        "pre_install": ["npm i -g yarn"],
        "install": [
            "yarn install"
        ],
        # Write JSON to file then cat — avoids a docker-log truncation seen
        # on >64KB single-line stdout writes. See specs/carbon.py _jest_file_cmd.
        "test_cmd": [
            "yarn install",
            "{ set +x; npx jest --runInBand --json --outputFile=/testbed/jest-0.json > /dev/null 2>&1 || true; (python3 -m json.tool /testbed/jest-0.json 2>/dev/null || cat /testbed/jest-0.json 2>/dev/null); set -x; } 2>/dev/null",
        ],
        "docker_specs": {
            "node_version": "21.6.2"
        }
    } for k in [
        '1.7', '2.0', '2.3', '2.6', '2.7',
        '2.11', '2.13', '2.14', '2.15', '2.16', '2.17', '2.18', '2.19',
        '2.20', '2.21', '2.22', '2.25', '2.26', '2.27', '2.29',
        '2.31', '2.33', '2.34'
    ]}
}
