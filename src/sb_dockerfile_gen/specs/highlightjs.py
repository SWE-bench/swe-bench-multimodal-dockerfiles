"""highlight.js spec."""

SPECS_HIGHLIGHTJS = {k: {
    "install": [
        "npm install",
        "npm run build"
    ],
    "test_cmd": [
        "npm install",
        "npm run build",
        "./node_modules/.bin/mocha test --reporter json",
    ],
    "docker_specs": {
        "node_version": "21.6.2"
    }
} for k in [
    '10.0', '10.2', '10.3', '10.4', '10.5', '10.6', '11.0', '11.2', '11.3',
    '11.4', '11.5', '11.6', '8.4', '8.9', '9.13', '9.15', '9.16', '9.17', '9.18',
    None
]}
