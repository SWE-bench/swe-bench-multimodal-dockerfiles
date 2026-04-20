"""
Public symbols for the multimodal (JavaScript) dockerfile generator.

Shared constants that the rest of the package (and external callers) import
from. Per-repo SPECS_* live under `sb_dockerfile_gen.specs`; shared install
helpers live in `sb_dockerfile_gen.common`.
"""

from sb_dockerfile_gen.specs import MAP_REPO_VERSION_TO_SPECS_JS

CONTAINER_WORKDIR = "/testbed"

REPO_BASE_COMMIT_BRANCH: dict[str, dict[str, str]] = {}

START_TEST_OUTPUT = ">>>>> Start Test Output"
END_TEST_OUTPUT = ">>>>> End Test Output"

FAIL_ONLY_REPOS = {
    "chartjs/Chart.js",
    "processing/p5.js",
    "markedjs/marked",
}

MAP_REPO_TO_PARSER_NAME = {
    "Automattic/wp-calypso": "parse_log_calypso",
    "chartjs/Chart.js": "parse_log_chart_js",
    "markedjs/marked": "parse_log_marked",
    "processing/p5.js": "parse_log_p5js",
    "diegomura/react-pdf": "parse_log_react_pdf",
}

__all__ = [
    "CONTAINER_WORKDIR",
    "END_TEST_OUTPUT",
    "FAIL_ONLY_REPOS",
    "MAP_REPO_TO_PARSER_NAME",
    "MAP_REPO_VERSION_TO_SPECS_JS",
    "REPO_BASE_COMMIT_BRANCH",
    "START_TEST_OUTPUT",
]
