"""react-pdf spec."""

from sb_dockerfile_gen.common import X11_DEPS


SPECS_REACT_PDF = {
    **{
        k: {
            "apt-pkgs": [
                "pkg-config",
                "build-essential",
                "libpixman-1-0",
                "libpixman-1-dev",
                "libcairo2-dev",
                "libpango1.0-dev",
                "libjpeg-dev",
                "libgif-dev",
                "librsvg2-dev",
            ]
            + X11_DEPS,
            "pre_install": ["npm i -g yarn"],
            "install": ["yarn install"],
            "test_cmd": 'NODE_OPTIONS="--experimental-vm-modules" ./node_modules/.bin/jest --no-color',
            "docker_specs": {"node_version": "18.20.4"},
        }
        for k in ["1.0", "1.1", "1.2", "2.0"]
    }
}
for v in ["1.0", "1.1", "1.2"]:
    SPECS_REACT_PDF[v]["docker_specs"]["node_version"] = "8.17.0"
    SPECS_REACT_PDF[v]["pre_install"] = []  # v1.x uses npm, not yarn
    SPECS_REACT_PDF[v]["install"] = ["npm install", "npm install cheerio@1.0.0-rc.3"]
    SPECS_REACT_PDF[v]["test_cmd"] = "./node_modules/.bin/jest --no-color"


_SPECS_REACT_PDF_STATIC_TEST_CMD = {v: SPECS_REACT_PDF[v]["test_cmd"] for v in SPECS_REACT_PDF}


def _react_pdf_test_cmds(instance: dict) -> list:
    # Run the full test suite (not narrowed to the test_patch's package) so
    # P2P entries in other packages (textkit, image, stylesheet, ...) are
    # actually evaluated. Previously: jest was passed "packages/<name>" which
    # made jest skip the rest of the monorepo.
    return [_SPECS_REACT_PDF_STATIC_TEST_CMD[instance["version"]]]


for v in SPECS_REACT_PDF:
    SPECS_REACT_PDF[v]["test_cmd"] = _react_pdf_test_cmds
