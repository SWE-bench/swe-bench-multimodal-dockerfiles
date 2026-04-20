"""Grommet spec."""

SPECS_GROMMET = {
    **{k: {
        "pre_install": ["npm i -g yarn"],
        "install": [
            "yarn install"
        ],
        "test_cmd": [
            "yarn install",
            "npx jest --runInBand --json",
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
