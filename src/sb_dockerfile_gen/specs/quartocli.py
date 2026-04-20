"""Quarto CLI spec."""

import json
import re

from sb_dockerfile_gen.common import (
    INSTALL_JULIA,
    INSTALL_TINYTEX,
    INSTALL_R_PACKAGES,
)


PIP_INSTALLS_QUARTOCLI = [
    "pip3 install --user pipenv",
    "pip3 install nbformat",
    "pip3 install nbclient",
    "pip3 install pandocfilters",
    "pip3 install shiny",
    "pip3 install pyyaml",
    "pip3 install setuptools",
    "pip3 install numpy",
    "pip3 install seaborn",
    "pip3 install matplotlib",
    "pip3 install bokeh",
    "pip3 install bokeh_sampledata",
    "pip3 install ipyleaflet",
    "pip3 install pandas",
    "pip3 install itables",
    "pip3 install pexpect",
    "pip3 install ptyprocess",
    "pip3 install appnope",
    "pip3 install ipykernel",
]
SPECS_QUARTOCLI = {
    None : {
        "apt-pkgs": ["libffi-dev", "zip", "unzip", "python3", "python3-pip", "python3.10-distutils", "r-base-core",
                     "poppler-utils", "libxml2-utils", "cmake"],
        # pre_install runs in its own Docker layer BEFORE git clone, so it's
        # cached and shared across all 24 quarto instances (~7 min saved per image).
        "pre_install": INSTALL_JULIA + INSTALL_TINYTEX + INSTALL_R_PACKAGES + PIP_INSTALLS_QUARTOCLI,
        # install runs AFTER git clone (per-instance layer).
        "install": ["ls .",
                    "[ -f configure.sh ] || ./configure-linux.sh",
                    "[ -f configure-linux.sh ] || ./configure.sh",
                    "cd tests",
                    "sed -i 's/quarto install.*tinytex/true/' configure-test-env.sh 2>/dev/null || true",
                    "./configure-test-env.sh || true",
                    "cd ..",
                    ],
        "test_cmd": [ # test generates files that add future test cases -- run tests fairly
            "cp -r tests/ tests_tmp/",
            "cd tests",
            "QUARTO_TESTS_NO_CONFIG=\"true\" ./run-tests.sh",
            "cd ..",
            "rm -rf tests/",
            "mv tests_tmp/ tests/",
        ],
        "docker_specs": {
            "run_args": {
                "cap_add": ["SYS_ADMIN"],
            }
        }
    }
}


_SPECS_QUARTOCLI_STATIC_TEST_CMD = {v: SPECS_QUARTOCLI[v]["test_cmd"] for v in SPECS_QUARTOCLI}


def _quarto_test_cmds(instance: dict) -> list:
    """Quarto: direct-render for 5292, tufte-pdf removal for all others."""
    if instance["instance_id"] == "quarto-dev__quarto-cli-5292":
        def _render_block(label: str) -> str | None:
            m = re.match(r"\[smoke\] > quarto render (\S+) --to (\S+)", label)
            if not m:
                return None  # [unit] labels handled by the full test suite below
            target = "tests/" + m.group(1)
            fmt = m.group(2)
            # Post-render discriminator for 5286.qmd → latex (F2P): the gold patch
            # removes `\textless{}1\textgreater{}` code-annotation markers. Without
            # this grep, the render succeeds either way and the F2P is non-discriminating.
            # See MULTIMODAL_FIXES.md §2.4.
            if target == "tests/docs/smoke-all/2023/04/24/5286.qmd" and fmt == "latex":
                output = "tests/docs/smoke-all/2023/04/24/5286.tex"
                forbidden = r"\textless{}1\textgreater{}"
                extra = f" && ! grep -Fq '{forbidden}' {output}"
            else:
                extra = ""
            return (
                f"cd /testbed && if timeout 300 quarto render {target} --to {fmt} 2>/dev/null{extra} ; "
                f"then printf '{label} ... \\033[32mok\\033[0m\\n' ; "
                f"else printf '{label} ... \\033[31mFAILED\\033[0m\\n' ; fi"
            )
        f2p_list = instance.get("FAIL_TO_PASS", [])
        if isinstance(f2p_list, str):
            f2p_list = json.loads(f2p_list)
        p2p_list = instance.get("PASS_TO_PASS", [])
        if isinstance(p2p_list, str):
            p2p_list = json.loads(p2p_list)
        parts = ["rm -f tests/docs/page-layout/tufte-pdf.qmd"]
        parts.extend(b for b in (_render_block(t) for t in f2p_list) if b)
        parts.extend(b for b in (_render_block(t) for t in p2p_list) if b)
        return parts

    # All other quarto instances: prepend tufte-pdf removal to standard test_cmd
    test_cmd = _SPECS_QUARTOCLI_STATIC_TEST_CMD[instance.get("version") or None]
    test_cmd = list(test_cmd) if isinstance(test_cmd, list) else [test_cmd]
    return ["rm -f tests/docs/page-layout/tufte-pdf.qmd"] + test_cmd


for v in SPECS_QUARTOCLI:
    SPECS_QUARTOCLI[v]["test_cmd"] = _quarto_test_cmds
