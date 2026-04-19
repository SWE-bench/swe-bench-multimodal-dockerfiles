"""
Repo-version-to-spec mapping for the SWE-bench Multimodal generator.

The 7 multilingual JS repos (babel, vuejs, docusaurus, immutable-js, three.js,
preact, axios) live in `swe-bench-multilingual-dockerfiles` and are intentionally
omitted here.
"""

from sb_dockerfile_gen.specs.dev_split import (
    SPECS_CALYPSO,
    SPECS_CHART_JS,
    SPECS_MARKED,
    SPECS_P5_JS,
    SPECS_REACT_PDF,
)
from sb_dockerfile_gen.specs.test_split import (
    SPECS_BPMN_JS,
    SPECS_CARBON,
    SPECS_ESLINT,
    SPECS_GROMMET,
    SPECS_HIGHLIGHTJS,
    SPECS_LIGHTHOUSE,
    SPECS_NEXT,
    SPECS_OPENLAYERS,
    SPECS_PRETTIER,
    SPECS_PRISM,
    SPECS_QUARTOCLI,
    SPECS_SCRATCH,
)

MAP_REPO_VERSION_TO_SPECS_JS = {
    # Dev split
    "Automattic/wp-calypso": SPECS_CALYPSO,
    "chartjs/Chart.js": SPECS_CHART_JS,
    "markedjs/marked": SPECS_MARKED,
    "processing/p5.js": SPECS_P5_JS,
    "diegomura/react-pdf": SPECS_REACT_PDF,
    # Test split
    "alibaba-fusion/next": SPECS_NEXT,
    "bpmn-io/bpmn-js": SPECS_BPMN_JS,
    "carbon-design-system/carbon": SPECS_CARBON,
    "eslint/eslint": SPECS_ESLINT,
    "GoogleChrome/lighthouse": SPECS_LIGHTHOUSE,
    "grommet/grommet": SPECS_GROMMET,
    "highlightjs/highlight.js": SPECS_HIGHLIGHTJS,
    "openlayers/openlayers": SPECS_OPENLAYERS,
    "prettier/prettier": SPECS_PRETTIER,
    "PrismJS/prism": SPECS_PRISM,
    "quarto-dev/quarto-cli": SPECS_QUARTOCLI,
    "scratchfoundation/scratch-gui": SPECS_SCRATCH,
}
