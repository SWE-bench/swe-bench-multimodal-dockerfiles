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

# p5.js v0.6/v0.7 strip the structured JSON reporter (see specs/p5_js.py
# `_REPORTER_INCOMPATIBLE_VERSIONS`); newer versions install it.
_P5JS_REPORTER_INCOMPATIBLE_VERSIONS = {"0.6", "0.7"}


def _pick_p5js_parser(instance: dict) -> str:
    if instance.get("version") in _P5JS_REPORTER_INCOMPATIBLE_VERSIONS:
        return "parse_log_p5js_mocha_spec"
    return "parse_log_p5js_json"


# Values are either a parser-name string (constant for the repo) or a callable
# `(instance) -> name` for repos whose parser depends on the instance.
MAP_REPO_TO_PARSER_NAME = {
    "Automattic/wp-calypso": "parse_log_calypso",
    "chartjs/Chart.js": "parse_log_chart_js",
    "markedjs/marked": "parse_log_marked",
    "processing/p5.js": _pick_p5js_parser,
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
